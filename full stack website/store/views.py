from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal

from .models import Category, Product, Order, OrderItem
from .forms import UserRegistrationForm, LoginForm, CheckoutForm

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Search filter
    query = request.GET.get('q', '')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    # Category filter
    category_slug = request.GET.get('category', '')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    # Sort filter
    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    else: # default newest
        products = products.order_by('-created_at')

    featured_products = Product.objects.filter(is_featured=True)[:4]

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'query': query,
        'sort': sort,
        'featured_products': featured_products,
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)

def cart_detail(request):
    return render(request, 'store/cart.html')

def cart_add(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})
        str_id = str(product_id)
        
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1

        if str_id in cart:
            cart[str_id]['quantity'] += quantity
        else:
            cart[str_id] = {'quantity': quantity, 'price': str(product.price)}

        request.session['cart'] = cart
        request.session.modified = True

        # Calculate updated summary
        total_items = sum(item['quantity'] for item in cart.values())

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({
                'success': True,
                'message': f'"{product.name}" added to cart!',
                'cart_count': total_items,
                'product_name': product.name,
                'product_price': str(product.price)
            })

        messages.success(request, f'"{product.name}" added to your cart!')
        return redirect('cart_detail')

    return redirect('product_list')

def cart_update(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        str_id = str(product_id)
        
        try:
            quantity = int(request.POST.get('quantity', 1))
        except ValueError:
            quantity = 1

        if str_id in cart:
            if quantity > 0:
                cart[str_id]['quantity'] = quantity
            else:
                del cart[str_id]
            request.session['cart'] = cart
            request.session.modified = True

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({'success': True})

        return redirect('cart_detail')

    return redirect('cart_detail')

def cart_remove(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        str_id = str(product_id)

        if str_id in cart:
            del cart[str_id]
            request.session['cart'] = cart
            request.session.modified = True

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({'success': True, 'message': 'Item removed from cart.'})

        messages.info(request, 'Item removed from cart.')
        return redirect('cart_detail')

    return redirect('cart_detail')

def cart_clear(request):
    if 'cart' in request.session:
        del request.session['cart']
        request.session.modified = True
    messages.info(request, 'Cart cleared.')
    return redirect('cart_detail')

def checkout(request):
    cart_data = request.session.get('cart', {})
    if not cart_data:
        messages.warning(request, 'Your cart is empty.')
        return redirect('product_list')

    # Calculate cart items and totals
    product_ids = [int(pid) for pid in cart_data.keys()]
    products = Product.objects.filter(id__in=product_ids)
    product_dict = {p.id: p for p in products}

    subtotal = Decimal('0.00')
    cart_items = []
    for str_id, item in cart_data.items():
        pid = int(str_id)
        if pid in product_dict:
            prod = product_dict[pid]
            qty = item['quantity']
            item_total = prod.price * qty
            subtotal += item_total
            cart_items.append({'product': prod, 'quantity': qty, 'total': item_total})

    tax = subtotal * Decimal('0.08')
    shipping = Decimal('0.00') if subtotal > Decimal('50.00') else Decimal('9.99')
    grand_total = subtotal + tax + shipping

    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_amount = grand_total
            order.save()

            # Create OrderItems & update stock
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    price=item['product'].price,
                    quantity=item['quantity']
                )
                # Reduce stock
                item['product'].stock = max(0, item['product'].stock - item['quantity'])
                item['product'].save()

            # Clear session cart
            del request.session['cart']
            request.session.modified = True

            return redirect('order_success', order_number=order.order_number)
    else:
        form = CheckoutForm(initial=initial_data)

    context = {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)

def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'store/order_success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, f'Welcome to CyberStore, {user.username}!')
            return redirect('product_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                next_url = request.GET.get('next', 'product_list')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('product_list')
