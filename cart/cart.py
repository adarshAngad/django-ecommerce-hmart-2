from django.conf import settings


class Cart:
    def __init__(self, request):
        self.session = request.session
        session_id = settings.CART_SESSION_ID
        cart = self.session.get(session_id)
        if cart is None:
            cart = self.session[session_id] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'product_id': product.id,
                'name': product.name,
                'image': product.image.url if product.image else '',
                'price': str(product.price),
                'quantity': quantity,
            }
        else:
            self.cart[product_id]['quantity'] = self.cart[product_id]['quantity'] + quantity
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def decrement(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            return
        self.cart[product_id]['quantity'] -= 1
        if self.cart[product_id]['quantity'] <= 0:
            del self.cart[product_id]
        self.session.modified = True

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.cart = self.session[settings.CART_SESSION_ID]
        self.session.modified = True
