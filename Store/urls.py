from django.urls import path
from .views import ProductListView, ProductDetailView, AddToCartView, CartView, DeleteCartItemView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/delete/', DeleteCartItemView.as_view(), name='delete-cart-item'),
]
