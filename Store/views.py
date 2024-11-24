from django.shortcuts import render
from Store import models as store_models
from django.http import JsonResponse
from django.db.models import Q, Avg, Sum
# Create your views here.
def index(request):
    # Fetch products with the status "Published"
    products = store_models.Product.objects.filter(status="Published")
    context = {
        {'products': products}
    }
    # Render the products to the template
    return render(request, 'index.html', context)


def product_details(request, slug):
    product = store_models.Product.objects.get(status='Published', slug=slug)
    related_product = store_models.Product.objects.filter(category=product.category, status="Published").exclude(id=product.id)
    product_stock_range = (1, product.stock + 1)
    context = {
        'product': product,
        'related_product':related_product,
        'product_stock_range':product_stock_range,
    }
    return render(request, 'product_details.html', context)

def add_to_cart(request):
    product_id = request.GET.get('id')
    quantity = request.GET.get('qty')
    color = request.GET.get('color')
    size = request.GET.get('size')
    cart_id = request.GET.get('cart_id')
    request.session['cart_id'] = cart_id
    
    if not id or not qty or not cart_id:
        return JsonResponese({'error': 'No id, qty or cart_id'}, status=400)
    
    try:
        product = store_models.Product.objects.get(status='Published', id=id)
        
    except store_models.Product.DoesNotExist:
        return JsonResponese({'error': 'Product not found'}, status=400)
    
    existing_cart_items = store_models.Cart.objects.filter().first()
    if int(qty) > product.stock:
        return JsonResponse({'error': 'Qty excced current stock amount'}, status=400)
    
    if not existing_cart_items:
        cart = store_models.Cart()
        cart.product = product
        cart.qty = qty
        cart.price = product.price
        cart.color = color
        cart.size = size
        cart.sub_total = Decimal(product.price) * Decimal(qty)
        cart.shipping = Decimal(product.shipping) * Decimal(qty)
        cart.total = cart.sub_total + cart.shipping
        cart.user = request.user if request.user.is_authenticated else None
        cart.cart_id = cart_id
        
        message = "Item added to cart"
    else:
        existing_cart_items.product = product
        existing_cart_items.qty = qty
        existing_cart_items.price = product.price
        existing_cart_items.color = color
        existing_cart_items.size = size
        existing_cart_items.sub_total = Decimal(product.price) * Decimal(qty)
        existing_cart_items.shipping = Decimal(product.shipping) * Decimal(qty)
        existing_cart_items.total = existing_cart_items.sub_total + existing_cart_items.shipping
        existing_cart_items.user = request.user if request.user.is_authenticated else None
        existing_cart_items.cart_id = cart_id
        existing_cart_items.save()
        
        message = "Cart updated"
        
    total_cart_items = store_models.Cart.objects,filter(Q(cart_id=cart_id) | Q(cart_id=cart_id))
    cart_sub_total = store_models.Cart.objects.filter(cart_id=cart_id).aggregate(sub_total=Sum('sub_total'))['sub_total']
        
    return JsonResponse({
        'message':message,
        'total_cart_items':total_cart_items.count(),
        'cart_sub_total':'{:,.2f}'.format(cart_sub_total),
        'total_cart_items':"{:,.2f}".format(existing_cart_items.sub_total) if existing_cart_items else "{:,.2f}".format(cart.cart_sub_total)
        })

        
    return render(request, 'cart.html', context)

 