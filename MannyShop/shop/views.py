from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product

def home(request):
    return render(request, 'home.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    invalid_items = []

    for product_id, quantity in list(cart.items()):
        try:
            product = Product.objects.get(id=int(product_id))
        except (Product.DoesNotExist, ValueError):
            invalid_items.append(product_id)
            continue

        subtotal = product.price * quantity
        total += subtotal
        items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    if invalid_items:
        for invalid_id in invalid_items:
            cart.pop(invalid_id, None)
        request.session['cart'] = cart
        messages.warning(request, 'Some unavailable items were removed from your cart.')

    return render(request, 'cart.html', {'items': items, 'total': total})

def checkout(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
        except (Product.DoesNotExist, ValueError):
            continue
        subtotal = product.price * quantity
        total += subtotal
        items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    if request.method == 'POST':
        if items:
            request.session['cart'] = {}
            messages.success(request, 'Order confirmed! Thank you for shopping with RueShop.')
            return redirect('home')
        messages.warning(request, 'Your cart is empty. Add items before confirming your order.')
        return redirect('cart')

    return render(request, 'checkout.html', {'items': items, 'total': total})

def contact(request):
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # In real app, save to model or send email
        return render(request, 'contact.html', {'submitted': True})
    return render(request, 'contact.html')
