from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import date


# Create your models here.

class CaUser(AbstractUser):
    is_admin = models.BooleanField(default=False)

class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.FileField(upload_to='product_img', blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, default="")

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(CaUser, on_delete=models.CASCADE, default="")
    date_created = models.DateField(default=date.today)
    shipping_addr = models.CharField(max_length=500, default="")

class OrderItems(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def price(self):
        return self.product.price * self.quantity

class ShoppingBasket(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(CaUser, on_delete=models.CASCADE)

class ShoppingBasketItems(models.Model):
    id = models.AutoField(primary_key=True)
    basket_id = models.ForeignKey(ShoppingBasket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
