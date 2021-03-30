from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import uuid
from .utils import *
from django.contrib.auth.models import User


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

    productId = data["productId"]
    action = data["action"]

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1

    orderItem.save()

    total = order.get_cart_items
    totalValue = orderItem.get_total
    quantity = orderItem.quantity

    orderTotalValue = float(order.get_cart_total)

    if orderItem.quantity <= 0:
        orderItem.delete()
        total = 0
        totalValue = 0
        quantity = 0

    return JsonResponse(
        {
            "cartTotal": total,
            "productQuantity": quantity,
            "orderItemTotalValue": totalValue,
            "orderTotalValue": orderTotalValue,
        },
        safe=False,
    )


def processOrder(request):
    transaction_id = str(uuid.uuid4())

    data = json.loads(request.body)
    print(data)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        uname = data["form"]["username"]
        email = data["form"]["email"]
        print(uname, email)
        errors = []
        if User.objects.filter(username=uname).exists():
            errors.append({"err": "Username already exists."})
        if User.objects.filter(email=email).exists():
            errors.append({"err": "Email is already in use."})

        errCount = len(errors)

        print("Number of errors: ", errCount)
        if errCount > 0:
            return JsonResponse({"errors": errors}, safe=False)

        customer, order = guestOrder(request, data)

    total = float(data["form"]["total"])
    order.transaction_id = transaction_id

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

    return JsonResponse(
        {"id": order.id, "transactionId": order.transaction_id}, safe=False
    )


def confirmPayment(request):
    # TODO: confirm the transaction with paypal, check if both fields (order.paypalTxId == request.order.paypalTxId) are equal
    # then mark order as completed
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order.complete = True
    order.save()
    return JsonResponse(
        {
            "id": order.id,
            "transactionId": order.transaction_id,
            "completed": order.complete,
        },
        safe=False,
    )