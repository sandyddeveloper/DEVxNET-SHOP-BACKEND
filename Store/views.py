from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from Store.models import Product, Cart
from Customer.models import Address
from .serializers import ProductSerializer, CartSerializer, AddressSerializer
from decimal import Decimal

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.filter(status="Published")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetailView(APIView):
    def get(self, request, slug):
        product = get_object_or_404(Product, status="Published", slug=slug)
        serializer = ProductSerializer(product)
        related_products = Product.objects.filter(
            category=product.category, status="Published"
        ).exclude(id=product.id)
        related_serializer = ProductSerializer(related_products, many=True)
        return Response({
            'product': serializer.data,
            'related_products': related_serializer.data,
            'stock_range': list(range(1, product.stock + 1))
        })

class AddToCartView(APIView):
    def post(self, request):
        cart_id = request.data.get('cart_id')
        product_id = request.data.get('product_id')
        qty = request.data.get('qty')

        if not cart_id or not product_id or not qty:
            return Response({'error': 'Missing required parameters'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id, status='Published')

        if int(qty) > product.stock:
            return Response({'error': 'Quantity exceeds stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = Cart.objects.get_or_create(
            product=product, cart_id=cart_id,
            defaults={
                'qty': qty,
                'price': product.price,
                'sub_total': Decimal(product.price) * int(qty),
                'shipping': Decimal(product.shipping) * int(qty),
                'total': Decimal(product.price) * int(qty) + Decimal(product.shipping) * int(qty),
                'user': request.user if request.user.is_authenticated else None
            }
        )

        if not created:
            cart_item.qty = int(qty)
            cart_item.sub_total = Decimal(product.price) * int(qty)
            cart_item.shipping = Decimal(product.shipping) * int(qty)
            cart_item.total = cart_item.sub_total + cart_item.shipping
            cart_item.save()

        return Response({'message': 'Cart updated successfully'})

class CartView(APIView):
    def get(self, request):
        cart_id = request.session.get('cart_id')
        if not cart_id:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        items = Cart.objects.filter(cart_id=cart_id)
        serializer = CartSerializer(items, many=True)
        total = items.aggregate(sub_total=Sum('sub_total'))['sub_total'] or 0

        return Response({
            'items': serializer.data,
            'total': f"{total:,.2f}"
        })

class DeleteCartItemView(APIView):
    def delete(self, request):
        item_id = request.data.get('item_id')
        cart_id = request.data.get('cart_id')

        if not item_id or not cart_id:
            return Response({'error': 'Missing required parameters'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = get_object_or_404(Cart, id=item_id, cart_id=cart_id)
        cart_item.delete()

        return Response({'message': 'Item deleted successfully'})
