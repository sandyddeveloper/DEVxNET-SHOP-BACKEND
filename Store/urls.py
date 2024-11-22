from django.urls import path
from . import views

app_name = 'Store'
urlpatterns = [
    path('', views.index),
    path('detail/<slug>/', views.product_details),
]
