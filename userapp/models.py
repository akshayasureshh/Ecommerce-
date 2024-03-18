from django.db import models
from django.contrib.auth.models import User
from adminapp .models import Product

# Create your models here.



class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)




class WishList(models.Model):
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   product = models.ForeignKey(Product,on_delete=models.CASCADE)





class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=50,default='Order Placed')
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,default="")