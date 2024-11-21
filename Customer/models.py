from django.db import models
from UserAuth.models import User 
from Store.models import Product
# Create your models here.

TYPE = (
    ("New Order", "New Order"),
    ("Item Shipped", "Item Shipped"),
    ("Item Delivered", "Item Delivered"),
)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="Wishlist")
    
    class Meta:
        verbose_name_plural = "Wishlist"
        
    def __str__(self):
        if self.product.name:
            return self.product.name
        else:
            return "Wishlist"
        
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="addresses")
    full_name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)  
    email = models.EmailField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)  
    zip_code = models.CharField(max_length=10, null=True, blank=True)  
    
    class Meta:
        verbose_name_plural = 'Customer Address'

    def __str__(self):
        return self.full_name

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=100, choices=TYPE, default=None)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Notification'
        
    def __str__(self):
        return self.type
    
    