from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .forms import CustomUserCreationForm, OrderForm
from django.conf import settings
import os

def debug_info(request):
    """Debug view to check database and media state"""
    products = Product.objects.all()
    categories = Category.objects.all()
    
    media_path = settings.MEDIA_ROOT
    media_files = []
    if os.path.exists(media_path):
        for root, dirs, files in os.walk(media_path):
            for file in files:
                media_files.append(os.path.join(root, file))

    # Get detailed product information
    product_details = []
    for product in products:
        product_details.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'available': product.available,
            'stock': product.stock,
            'image_name': str(product.image) if product.image else None,
            'category': product.category.name if product.category else None,
        })

    debug_info = {
        'Product Count': products.count(),
        'Category Count': categories.count(),
        'Products': product_details,
        'Categories': [{'id': c.id, 'name': c.name, 'slug': c.slug} for c in categories],
        'Media Files': media_files,
        'Media Root': settings.MEDIA_ROOT,
        'Database Engine': settings.DATABASES['default']['ENGINE'],
        'Database Config': {
            k: v for k, v in settings.DATABASES['default'].items()
            if k not in ('PASSWORD',)
        },
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
        'BASE_DIR': str(settings.BASE_DIR),
    }
    
    return JsonResponse(debug_info, json_dumps_params={'indent': 2})
import json


def home(request):
    """Home page with featured products"""
    # Get most efficient/popular products that users are likely to buy
    # Prioritize: daily essentials, high-demand items (low stock = high sales)
    efficient_product_names = [
        'Premium Coffee Beans',      # Daily essential, consumable
        'Greek Yogurt',             # Healthy daily essential
        'Wireless Headphones',       # Popular tech, good value
        'Organic Apples',           # Fresh, healthy, affordable
        'Fitness Tracker',          # Popular wellness item
        'Whole Grain Bread',        # Daily staple
        'Smartphone Pro',           # High-demand tech
        'Bluetooth Speaker',        # Popular entertainment item
    ]

    # Get products by name priority
    featured_products = []
    for name in efficient_product_names:
        try:
            product = Product.objects.get(name=name, available=True)
            featured_products.append(product)
        except Product.DoesNotExist:
            continue

    # If we don't have enough featured products, add high-demand items (low stock indicates popularity)
    if len(featured_products) < 8:
        additional_products = Product.objects.filter(
            available=True,
            stock__lte=20  # Low stock indicates high demand/popularity
        ).exclude(
            id__in=[p.id for p in featured_products]
        ).order_by('stock', 'price')[:8-len(featured_products)]
        featured_products.extend(additional_products)

    # Final fallback: affordable items
    if len(featured_products) < 8:
        fallback_products = Product.objects.filter(
            available=True,
            price__lte=30.00
        ).exclude(
            id__in=[p.id for p in featured_products]
        ).order_by('price')[:8-len(featured_products)]
        featured_products.extend(fallback_products)

    categories = Category.objects.all()
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


def product_list(request, category_slug=None):
    """Display all products or products by category"""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # Add debugging information to the response
    print(f"Total products: {products.count()}")
    print(f"Available categories: {[c.name for c in categories]}")

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """Display product details"""
    product = get_object_or_404(Product, slug=slug, available=True)
    context = {
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            # Create a cart for the new user
            Cart.objects.create(user=user)
            return redirect('store:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def cart_detail(request):
    """Display cart contents"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
    }
    return render(request, 'store/cart_detail.html', context)


@login_required
@require_POST
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'{product.name} added to cart!')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.get_total_items(),
            'message': f'{product.name} added to cart!'
        })

    return redirect('store:product_detail', slug=product.slug)


@login_required
@require_POST
def remove_from_cart(request, product_id):
    """Remove product from cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        messages.success(request, f'{product.name} removed from cart!')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in cart!')

    return redirect('store:cart_detail')


@login_required
@require_POST
def update_cart(request, product_id):
    """Update cart item quantity"""
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity = quantity
            cart_item.save()
    else:
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass

    return redirect('store:cart_detail')


@login_required
def checkout(request):
    """Checkout process"""
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('store:cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    price=cart_item.product.price,
                    quantity=cart_item.quantity
                )
                # Update product stock
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()

            # Clear the cart
            cart.items.all().delete()

            messages.success(request, f'Order #{order.id} has been placed successfully!')
            return redirect('store:order_detail', order_id=order.id)
    else:
        # Pre-fill form with user data
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = OrderForm(initial=initial_data)

    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'store/order_detail.html', context)


@login_required
def order_history(request):
    """Display user's order history"""
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
    }
    return render(request, 'store/order_history.html', context)
