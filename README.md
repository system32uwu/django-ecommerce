# Features

- Register
- Log In
- Log Out
- Update user data (Name, Surname, email)
- List products
- Add products to cart
- View product details
- Increase / decrease product quantity in the cart
- Checkout
- View orders history
- Guest user's cart is persisted in cookies, when checking out gets asked to register an account in order to proceed with payment
- Show errors in forms
- Paypal integration (pending)
- Star rating system (pending)

Most of what's in the project was done following [Dennis Ivy's Django Ecommerce Website series](https://www.youtube.com/watch?v=_ELCMngbM0E&list=PL-51WBLyFTg0omnamUjL1TCVov7yDTRng), I added some more functionality that he didn't include (authentication, account section, orders history, update user data, refresh cart items without reloading the page, and many more enhancements).

# Ecom Showcase

## Home

![](https://raw.githubusercontent.com/system32uwu/django-ecommerce/main/screenshots/Store.png)

### Adding products to order

![](https://raw.githubusercontent.com/system32uwu/django-ecommerce/main/screenshots/StoreAddToCartGuest.png)

## Product Details

![](https://raw.githubusercontent.com/system32uwu/django-ecommerce/main/screenshots/ProductDetails.png)

## Cart

![](https://raw.githubusercontent.com/system32uwu/django-ecommerce/main/screenshots/Cart.png)

## Checkout

![](https://raw.githubusercontent.com/system32uwu/django-ecommerce/main/screenshots/PayPalCheckout.png)

## PayPal Integration

![](https://raw.githubusercontent.com/system32uwu/django-ecommerce/main/screenshots/PayPalCheckout2.png)

## Login

![](https://raw.githubusercontent.com/system32uwu/django-ecommerce/main/screenshots/Login.png)

## Register

![](https://raw.githubusercontent.com/system32uwu/django-ecommerce/main/screenshots/Register.png)

## Account

![](https://raw.githubusercontent.com/system32uwu/django-ecommerce/main/screenshots/Account.png)

# Run It

## Requirements

- Python >= 3.9.2
- Django >= 3.1.7 (I recommend setting up a virtual environment).

## Additional notes

- You'll need to input products with the GUI in /admin

- There's no need to setup any DB configuration since this was done using sqlite.