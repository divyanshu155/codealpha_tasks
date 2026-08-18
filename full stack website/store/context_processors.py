from .models import Product
from decimal import Decimal

def cart_context(request):
    cart_data = request.session.get('cart', {})
    cart_items = []
    cart_count = 0
    subtotal = Decimal('0.00')

    product_ids = [int(pid) for pid in cart_data.keys()]
    products = Product.objects.filter(id__in=product_ids)
    product_dict = {p.id: p for p in products}

    for str_id, item_info in cart_data.items():
        pid = int(str_id)
        if pid in product_dict:
            product = product_dict[pid]
            qty = item_info.get('quantity', 1)
            item_total = product.price * qty
            subtotal += item_total
            cart_count += qty
            cart_items.append({
                'product': product,
                'quantity': qty,
                'total_price': item_total
            })

    tax = subtotal * Decimal('0.08')
    shipping = Decimal('0.00') if subtotal > Decimal('50.00') or subtotal == 0 else Decimal('9.99')
    total = subtotal + tax + shipping

    return {
        'cart_items': cart_items,
        'cart_count': cart_count,
        'cart_subtotal': subtotal,
        'cart_tax': tax,
        'cart_shipping': shipping,
        'cart_total': total
    }
