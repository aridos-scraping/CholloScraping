from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 
from .choices import *

class Rating(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return 'Rating del usuario \'' + str(self.user) + '\' al producto \'' + self.product.name + '\''


class Product(models.Model):
    sku = models.CharField(primary_key=True, max_length=255)
    brand = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    averageRating = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.name

class Price(models.Model):

    #Price without discount
    originalPrice = models.FloatField()
    #Price with discount
    currentPrice = models.FloatField()
    
    timestamp = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return 'Precio de ' + self.product.name + " = " + str(self.originalPrice) + "-" + str(self.currentPrice)
