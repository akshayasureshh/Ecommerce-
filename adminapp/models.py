from django.db import models
from django.utils.text import slugify
import uuid
from django.db.models import JSONField
import json
from PIL import Image
# Create your models here.





class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    sort_description = models.TextField(null=True, blank=True)
    full_detail = models.TextField(null=True, blank=True)
    product_tag = models.CharField(max_length=200,null=True)


    def __str__(self):        
        return self.name
    
    # @property
    # def generate_slug(self):
    #     return slugify(self.name)

    def save(self, *args, **kwargs):
        print("Save method is being called!")
        # If title is empty, generate a unique identifier as a fallback
        if not self.name:
            self.name = str(uuid.uuid4().hex)[:10]

        # Generate and save the slug
        self.slug = slugify(self.name)

        # Ensure the slug is unique by appending a unique identifier
        counter = 1
        original_slug = self.slug

        while Category.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        # If, after all these attempts, the slug is still empty, set a default value
        if not self.slug:
            self.slug = str(uuid.uuid4().hex)[:10]

        super(Category, self).save(*args, **kwargs)





class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    sort_description = models.TextField(null=True, blank=True)
    full_detail = models.TextField(null=True, blank=True)
    product_tag = models.CharField(max_length=200,null=True)
    


    def __str__(self):
        return self.name
    
    def generate_slug(self):
        return slugify(self.name)
    
    def save(self, *args, **kwargs):
        # If title is empty, generate a unique identifier as a fallback
        if not self.name:
            self.name = str(uuid.uuid4().hex)[:10]

        # Generate and save the slug using the method
        self.slug = self.generate_slug()

        # Ensure the slug is unique by appending a unique identifier
        counter = 1
        original_slug = self.slug

        while SubCategory.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        # If, after all these attempts, the slug is still empty, set a default value
        if not self.slug:
            self.slug = str(uuid.uuid4().hex)[:10]

        super(SubCategory, self).save(*args, **kwargs)


        

class Product(models.Model):

    Availability_CHOICES=(
    ('IN STOCK','IN STOCK'),
    ('OUT OF STOCK','OUT OF STOCK'),

)


    title = models.CharField(max_length=200)
    availability = models.CharField(choices=Availability_CHOICES,max_length=100)
    product_type = models.CharField(max_length=200)
    categories = models.ForeignKey(SubCategory,on_delete=models.CASCADE,null=True, blank=True)
    price = models.FloatField()
    size = models.JSONField(blank=True, null=True,default=list)
    description = models.TextField()
    product_tag = models.CharField(max_length=200,null=True)
    product_image=models.ImageField(upload_to='product',null=True)
    product_image1=models.ImageField(upload_to='product',null=True)
    product_image2=models.ImageField(upload_to='product',null=True)
    product_image3=models.ImageField(upload_to='product',null=True)
    product_image4=models.ImageField(upload_to='product',null=True)
    product_image5=models.ImageField(upload_to='product',null=True)
    product_image6=models.ImageField(upload_to='product',null=True)
    quantity = models.IntegerField(null=True)
    full_detail = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    color1 = models.CharField(max_length=7, default='#ff6191')  
    color2 = models.CharField(max_length=7, default='#33317d')  
    color3 = models.CharField(max_length=7, default='#56d4b7')  
    color4 = models.CharField(max_length=7, default='#009688') 
    colors = JSONField(default=list,blank=True, null=True)
    custom_size = models.TextField(null = True,blank = True)
    admin_choice = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')],null=True)


    def __str__(self):
        return self.title
    

    def get_json_data(self):
        return json.dumps(self.size)
    
    def  save(self, *args,**kwargs):
        super().save(*args,**kwargs)
        img=Image.open(self.product_image.path)


        if img.height!=850 or img.width!=765:
            output_size = (850,765)
            img.thumbnail(output_size)
            img.save(self.product_image.path)
     

    
    def save(self, *args, **kwargs):
        # If title is empty, generate a unique identifier as a fallback
        if not self.title:
            self.title = str(uuid.uuid4().hex)[:10]  # Adjust the length as needed

        # Generate and save the slug
        self.slug = slugify(self.title)

        # Ensure the slug is unique by appending a unique identifier
        counter = 1
        original_slug = self.slug

        while Product.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        # If, after all these attempts, the slug is still empty, set a default value
        if not self.slug:
            self.slug = str(uuid.uuid4().hex)[:10]  # Adjust the length as needed

        super(Product, self).save(*args, **kwargs)



class BackgroundSliders(models.Model):
    heading1 = models.CharField(max_length=255,null=True)
    heading2 = models.CharField(max_length=255,null=True)
    description = models.TextField(null=True)
    image = models.ImageField(
        upload_to='carousel_images/')
    


class ChildSliders(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(
        upload_to='child_slider_images/'
    )
    



class CroppedImage(models.Model):
    file = models.ImageField(upload_to='images')
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)
    
    def  save(self, *args,**kwargs):
        super().save(*args,**kwargs)
        img=Image.open(self.file.path)


        if img.height>850 or img.width>765:
            output_size = (850,765)
            img.thumbnail(output_size)
            img.save(self.file.path)