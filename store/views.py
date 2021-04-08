from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import json
import uuid
from .utils import *
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse


def store(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    products = Product.objects.all()
    context = {"products": products, "cartItems": cartItems, "order": order}
    return render(request, "store/store.html", context)


def cart(request):
    data = cartData(request)

    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/cart.html", context)


def checkout(request):
    data = cartData(request)

    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    print(data)
    productId = data["productId"]
    action = data["action"]

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add" or action == "buyNow":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1

    orderItem.save()

    total = order.get_cart_items
    totalValue = float(orderItem.get_total)
    quantity = orderItem.quantity

    orderTotalValue = float(order.get_cart_total)

    if orderItem.quantity <= 0:
        orderItem.delete()
        totalValue = 0
        quantity = 0

    data = {
        "cartTotal": total,
        "productQuantity": quantity,
        "orderItemTotalValue": totalValue,
        "orderTotalValue": orderTotalValue,
    }
    
    return JsonResponse(
        data=data,
        safe=False,
    )


def processOrder(request):
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        uname = data["form"]["username"]
        email = data["form"]["email"]
        password = data["form"]["password"]

        errors = []
        if User.objects.filter(username=uname).exists():
            errors.append("Username already exists.")
        if User.objects.filter(email=email).exists():
            errors.append("Email is already in use.")

        errCount = len(errors)

        if errCount > 0:
            return JsonResponse({"errors": errors}, safe=False)

        customer, order = guestOrder(request, data)

        if customer.user is not None:
            login(request, customer.user)
        else:
            print("is none")

    total = float(data["form"]["total"])

    if total != float(order.get_cart_total):
        err = [{"err": "Your order total value does not match."}]
        return JsonResponse({"errors": [err]}, safe=False)

    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"],
        )

    return JsonResponse({"id": order.id}, safe=False)


def confirmPayment(request):
    # TODO: confirm the transaction with paypal, check if both fields (order.paypalTxId == request.order.paypalTxId) are equal
    # then mark order as completed
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        transaction_id = str(uuid.uuid4())
        order.transaction_id = transaction_id
        order.complete = True
        order.save()

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


def _logout(request):
    logout(request)
    return redirect("store")


def _login(request):  # /login
    data = cartData(request)

    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/login.html", context)


def _loginEndPoint(request):  # /auth
    data = json.loads(request.body)
    username = data["userFormData"]["username"]
    password = data["userFormData"]["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(status=209)
    else:
        return JsonResponse(
            {"errors": ["Your login credentials are incorrect."]}, status=403
        )


def register(request):  # /register
    data = cartData(request)

    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/register.html", context)


def _registerEndPoint(request):  # /save_user
    data = json.loads(request.body)
    username = data["userFormData"]["username"]
    email = data["userFormData"]["email"]
    password = data["userFormData"]["password"]

    errors = []
    if User.objects.filter(username=username).exists():
        errors.append("Username already exists.")
    if User.objects.filter(email=email).exists():
        errors.append("Email is already in use.")

    errCount = len(errors)

    if errCount > 0:
        return JsonResponse({"errors": errors}, status=403, safe=False)

    return _loginEndPoint(request)


def profile(request):  # /profile
    data = cartData(request)

    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]
    user = request.user

    context = {"items": items, "order": order, "cartItems": cartItems, "user": user}
    return render(request, "store/profile.html", context)


def updPersonalInfo(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        fName = data["fName"]
        lName = data["lName"]
        user = User.objects.get(username=request.user.username)
        user.first_name = fName
        user.last_name = lName
        user.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


def updEmail(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        email = data["email"]
        user = User.objects.get(username=request.user.username)
        customer = Customer.objects.get(user=user)
        user.email = email
        customer.email = email
        user.save()
        customer.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


def _product(request, productId):
    data = cartData(request)

    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]
    product = Product.objects.get(id=productId)

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "product": product,
    }
    return render(request, "store/product.html", context)
