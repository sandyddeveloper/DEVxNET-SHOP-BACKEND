from django.urls import path
from . import views

app_name = 'Store'
urlpatterns = [
    path('', views.index),
    path('detail/<slug>/', views.product_details),
    path('add_to_cart/', views.add_to_cart),
]
