from tkinter import CASCADE
from django.db import models

# Create your models here.
from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to="food/images", default="")
    

    def __str__(self):
        return self.product_name

class OrderPost(models.Model):
    order_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.name


class PersonDetails(models.Model):
    person_id = models.AutoField(primary_key=True)
    person_name= models.CharField(max_length=50)
    phone = models.IntegerField(default=0)
    address = models.CharField(max_length=200)
    postal = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    is_paid=models.BooleanField(default=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.person_name

class PaymentDetail(models.Model):
    payid = models.CharField(max_length=200)
    payuser = models.CharField(max_length=200)
    payemail = models.CharField(max_length=200)
    payaccount = models.CharField(max_length=200)

    def __str__(self):
        return "Payment by "+ self.payaccount +"(" + self.payuser+")"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    forgot_password_token = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

