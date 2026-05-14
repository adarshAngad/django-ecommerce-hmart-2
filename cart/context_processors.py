from django.conf import settings


def cart_total_amount(request):
    cart = request.session.get(settings.CART_SESSION_ID) or {}
    total = 0
    for item in cart.values():
        try:
            total += int(item['price']) * int(item['quantity'])
        except (ValueError, TypeError, KeyError):
            continue
    return {'cart_total_amount': total}
