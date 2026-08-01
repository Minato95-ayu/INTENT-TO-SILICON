from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()

class Order(models.Model):
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    total = models.FloatField()
