var updateBtns = document.getElementsByClassName("update-cart");
var cartTotal = document.getElementById("cart-total");

for (i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var productPrice = this.dataset.price;
    var action = this.dataset.action;
    console.log("productId:", productId, "Action:", action);
    console.log("USER:", user);

    if (user == "AnonymousUser") {
      addCookieItem({
        id: productId,
        price: productPrice
      }, action);
    } else {
      updateUserOrder(product, productPrice, action);
    }
  });
}

const updateUserOrder = (productId, action) => {
  var url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      productId: productId,
      action: action,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      cartTotal.innerHTML = data.cartTotal;
      var row = document.getElementById(`row${productId}`);
      if (row) {
        if (data.productQuantity <= 0) {
          row.remove();
        } else {
          var cartItemQuantity = document.getElementById(`q${productId}`);
          var cartItemTotalPrice = document.getElementById(`t${productId}`);
          var totalItems = document.getElementById(`totalItems`);
          var totalValue = document.getElementById(`totalValue`);

          totalItems.innerHTML = data.cartTotal;
          totalValue.innerHTML = `$${data.orderTotalValue.toFixed(2)}`;

          cartItemQuantity.innerHTML = data.productQuantity;
          cartItemTotalPrice.innerHTML = `$${data.orderItemTotalValue.toFixed(
            2
          )}`;
        }
      }
    });
};

function addCookieItem(product,action) {

  if (action == "add") {
    if (cart[product.id] == undefined) {
      cart[product.id] = { quantity: 1, price: product.price };
    } else {
      cart[product.id]["quantity"] += 1;
    }
  }

  if (action == "remove") {
    cart[product.id]["quantity"] -= 1;

    if (cart[product.id]["quantity"] <= 0) {
      console.log("Item should be deleted");
      delete cart[product.id];
      row.remove();
    }
  }
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";

  totalItems = 0;
  totalValue = 0;

  Object.keys(cart).forEach((k) => {
    totalItems += cart[k]["quantity"];
    totalValue += parseFloat(cart[k]["price"]) * cart[k]["quantity"];
  });
  cartTotal.innerHTML = totalItems;

  var row = document.getElementById(`row${product.id}`);
  if (row) {
    var cartItemQuantity = document.getElementById(`q${product.id}`);
    var cartItemTotalPrice = document.getElementById(`t${product.id}`);
    var totalItemsE = document.getElementById(`totalItems`);
    var totalValueE = document.getElementById(`totalValue`);

    totalItemsE.innerHTML = totalItems;
    totalValueE.innerHTML = `$${totalValue.toFixed(2)}`;

    cartItemQuantity.innerHTML = cart[product.id]["quantity"];
    cartItemTotalPrice.innerHTML = `$${(product.price * parseFloat(cart[product.id]["quantity"])).toFixed(2)}`;
  }
}
