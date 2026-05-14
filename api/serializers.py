from django.contrib.auth.models import User
from rest_framework import serializers

from app.models import Order, OrderItems, Product


class ProductSerializer(serializers.ModelSerializer):
    """CRUD for products; FKs are IDs to related catalog tables."""

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'condition',
            'stock',
            'status',
            'discount',
            'information',
            'description',
            'image',
            'categories',
            'brand',
            'color',
            'filter_price',
            'created_date',
            'unique_id',
        ]
        read_only_fields = ['created_date', 'unique_id']

    def validate_price(self, value):
        if value is None or str(value).strip() == '':
            raise serializers.ValidationError('Price is required.')
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['id', 'product', 'image', 'quantity', 'price', 'total']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitems_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'firstname',
            'lastname',
            'country',
            'address',
            'city',
            'state',
            'postcode',
            'phone',
            'email',
            'amount',
            'payment_id',
            'paid',
            'status',
            'tracking_id',
            'date',
            'items',
        ]
        read_only_fields = fields


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'email', 'first_name', 'last_name']
