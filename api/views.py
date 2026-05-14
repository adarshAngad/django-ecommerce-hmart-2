import random

from django.conf import settings
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from app.models import Order, OrderItems, Product

from .serializers import OrderSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    RESTful product CRUD.
    - list / retrieve: public
    - create / update / destroy: admin (staff) only
    """

    queryset = (
        Product.objects.select_related('categories', 'brand', 'color', 'filter_price')
        .all()
        .order_by('id')
    )
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def simulate_checkout(request):
    """
    Take-home: checkout without real payment — records an order from the session cart.
    """
    cart = request.session.get(settings.CART_SESSION_ID) or {}
    if not cart:
        return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    body = request.data if isinstance(request.data, dict) else {}
    firstname = body.get('firstname') or (user.first_name or user.username)
    lastname = body.get('lastname') or (user.last_name or '')
    country = body.get('country') or 'N/A'
    address = body.get('address') or 'N/A'
    city = body.get('city') or 'N/A'
    state = body.get('state') or 'N/A'
    try:
        postcode = int(body.get('postcode') or 0)
    except (TypeError, ValueError):
        postcode = 0
    try:
        phone = int(body.get('phone') or 0)
    except (TypeError, ValueError):
        phone = 0
    email = body.get('email') or user.email or 'noreply@localhost'
    additional_info = body.get('additional_info') or ''

    total_rupees = 0
    for _key, line in cart.items():
        try:
            total_rupees += int(line['price']) * int(line['quantity'])
        except (KeyError, TypeError, ValueError):
            continue

    order = Order(
        user=user,
        firstname=firstname,
        lastname=lastname,
        country=country,
        address=address,
        city=city,
        state=state,
        postcode=postcode,
        phone=phone,
        email=email,
        additional_info=additional_info,
        payment_id='SIMULATION',
        amount=str(total_rupees),
        paid=True,
    )
    order.tracking_id = str(random.randint(10**9, 10**10 - 1))
    order.save()

    for _key, line in cart.items():
        try:
            a = int(line['price'])
            b = int(line['quantity'])
        except (KeyError, TypeError, ValueError):
            continue
        total = a * b
        OrderItems.objects.create(
            user=user,
            order=order,
            product=line.get('name', 'Item'),
            image=line.get('image', '') or '',
            quantity=str(line.get('quantity', b)),
            price=str(line.get('price', a)),
            total=str(total),
        )

    request.session[settings.CART_SESSION_ID] = {}
    request.session.modified = True

    return Response(
        {
            'detail': 'Order placed (simulated checkout, no payment processor).',
            'order': OrderSerializer(order).data,
        },
        status=status.HTTP_201_CREATED,
    )
