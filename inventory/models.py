from django.db import models
from django.contrib.auth.models import User


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True) 
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def _str_(self):
        return self.name
    
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):  
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class SalesRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    sold_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity_sold} of {self.product.name} sold on {self.sold_at}'
    
    

class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
