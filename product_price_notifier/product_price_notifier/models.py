from django.db import models

# Create your models here.
class Products(models.Model):
    id= models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    price = models.FloatField(max_length=100)
    link = models.CharField(max_length=100)
    query = models.CharField(max_length=50)
    relevant = models.BooleanField(max_length=50)
    