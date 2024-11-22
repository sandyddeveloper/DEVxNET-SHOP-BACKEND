from django.shortcuts import render
from Store import models as store_models

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
    
    context = {
        'product': product,
        'related_product':related_product,
    }
    return render(request, 'product_details.html', context)