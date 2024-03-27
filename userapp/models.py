from django.db import models
from django.contrib.auth.models import User
from adminapp .models import Product

# Create your models here.

class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='customers')
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    state=models.CharField(max_length=100)
    def __str__(self):
        return self.name




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
    # user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=50,default='Order Placed')
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,default="")


class Rating(models.Model):
    ONE_STAR = 1
    TWO_STARS = 2
    THREE_STARS = 3
    FOUR_STARS = 4
    FIVE_STARS = 5

    RATING_CHOICES = [
        (ONE_STAR, '1 star'),
        (TWO_STARS, '2 stars'),
        (THREE_STARS, '3 stars'),
        (FOUR_STARS, '4 stars'),
        (FIVE_STARS, '5 stars'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ratings')
    description = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is being created (not updated)
            user_id = kwargs.pop('user_id', None)
            product_id = kwargs.pop('product_id', None)

            # Ensure both user_id and product_id are provided
            if user_id is not None and product_id is not None:
                self.user_id = user_id
                self.product_id = product_id

        super().save(*args, **kwargs)



class ImageUpload(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_imageupload',null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_imageuplaod',null=True)
    text = models.TextField(max_length=1000)
    image =  models.ImageField(upload_to="user-images/")