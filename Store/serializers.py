from rest_framework import serializers
from Store.models import Product, Cart
from Customer.models import Address

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'stock', 'status', 'category', 'shipping']

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'product', 'qty', 'price', 'sub_total', 'shipping', 'total', 'cart_id']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'address_line', 'city', 'state', 'postal_code', 'country']
