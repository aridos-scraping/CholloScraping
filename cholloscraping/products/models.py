from django.db import models
from datetime import datetime
from .choices import *

class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=100)
    brand = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=2, choices = CAT_CHOICES, default = LAPTOPS)
    
    def __str__(self):
        return self.name

class Price(models.Model):

    originalPrice = models.IntegerField()
    currentPrice = models.IntegerField()
    
    timestamp = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey('Product', on_delete=models.CASCADE)

