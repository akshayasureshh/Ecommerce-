from django.shortcuts import render,redirect
from adminapp.models import *
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from . models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponseBadRequest
# Create your views here.

def  home(request):
     data = SubCategory.objects.all()
     parent_categories = Category.objects.all()
     parent_slider =  BackgroundSliders.objects.all()
     child_slider = ChildSliders.objects.all()
     product = Product.objects.all()
     totalitem = 0
     wishitem = 0
     if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(WishList.objects.filter(user=request.user))

     context ={
          'SubCate':data,
          'Category' : parent_categories,
          'parent_slider':parent_slider,
          'child_slider':child_slider,
          'products':product,
          'totalitem':totalitem,
          'wishitem':wishitem,

     }

     return render(request, 'index2.html',context)



def register(request):
     data = SubCategory.objects.all()
     parent_categories = Category.objects.all()
     context ={
          'SubCate':data,
          'Category' : parent_categories,
          
    }
     return render(request,'register.html',context)




def user_login(request):
    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()
    context ={
          'SubCate':data,
          'Category' : parent_categories,
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)  # Use auth_login instead of login
            return redirect('home')
        else:
            messages.success(request, "There is an error logging in")
            return redirect('login')
    else:
        return render(request, 'login.html',context)



def productdetail(request,categoryID):
    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()

    products = Product.objects.filter(categories=categoryID)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(WishList.objects.filter(user=request.user))

    context = {
        'products': products,
        'SubCate':data,
        'Category' : parent_categories,
        'totalitem':totalitem,
        'wishitem':wishitem,

          

    }

    return render(request,'productdetail.html',context)




def singleproduct(request, id):
    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()
    relatedproduct = Product.objects.all()
    products = Product.objects.get(id=id)
    product = get_object_or_404(Product, pk=id)
    reviews = Rating.objects.filter(product=product)

    wishlist = WishList.objects.filter(Q(product=products) & Q(user=request.user.pk))
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(WishList.objects.filter(user=request.user))   

    context = {
        'wishlist' : wishlist,
        'products': products,
        'SubCate': data,
        'Category': parent_categories,
        'totalitem':totalitem,
        'wishitem':wishitem,
        'relatedproducts': relatedproduct,
        'reviews': reviews,

    }
    
    return render(request, 'singleproduct.html', context)


def review(request, product_pk):
    user_id = request.user.id
    product_id = product_pk
    
    if request.method == 'POST':
        rating = request.POST['items']
        comment = request.POST['your-commemt']
        
        product = get_object_or_404(Product, pk=product_id)
        
        data = Rating.objects.create(
            user_id=user_id,
            product=product,
            rating=rating,
            description=comment
        )

        print("Review saved successfully!")

        return redirect(singleproduct, product_id)
    
    # product = get_object_or_404(Product, pk=product_id)
    
    # reviews = Rating.objects.filter(product=product)

    context = {
        'user_id': user_id,
        'product_id': product_id,
        # 'reviews': reviews,
        # 'products': Product.objects.get(id=product_id)
    }
    return render(request, 'singleproduct.html', context)



# @login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')

    # Check if product_id is provided and not empty
    if not product_id:
        return HttpResponseBadRequest("Product ID is missing")

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseBadRequest("Product does not exist")

    # Create a Cart object for the user and product
    Cart(user=user, product=product).save()

    return redirect(singleproduct, product_id)


# @login_required
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value = p.quantity*p.product.price
        amount= amount + value
        amount2=amount
        
    totalamount=amount+40
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(WishList.objects.filter(user=request.user))
    
    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()

    context = {
        
        'SubCate': data,
        'Category': parent_categories,
        'totalitem':totalitem,
        'wishitem':wishitem,

    }

    return render(request,'cart.html',locals())


# @login_required
def plus_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        print("this is product id",prod_id)
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        amount2=0
        for p in cart:
            value = p.quantity*p.product.price
            amount= amount + value
            amount2=amount

        totalamount=amount+40
        #print(prod_id)
        data={
              'quantity':c.quantity,
              'amount':amount,
              'amount2': amount2,
              'totalamount':totalamount
        }
        return JsonResponse(data)



# @login_required
def minus_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        amount2=0

        for p in cart:
            value = p.quantity*p.product.price
            amount= amount + value
            amount2=amount

        totalamount=amount+40
        #print(prod_id)
        data={
              'quantity':c.quantity,
              'amount':amount,
              'amount2': amount2,
              'totalamount':totalamount
        }
        return JsonResponse(data)


# @login_required
def remove_cart(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        amount2=0
        for p in cart:
            value = p.quantity * p.product.price
            amount= amount + value
            amount2=amount
        totalamount=amount+40
       
        data={
              'quantity':c.quantity,
              'amount':amount,
              'amount2': amount2,
              'totalamount':totalamount,
            
        }
        return JsonResponse(data)






@login_required
def show_wishlist(request):
    user=request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))
    product = WishList.objects.filter(user=user)


    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()


    context = {
        'SubCate': data,
        'Category': parent_categories,
        'totalitem':totalitem,
        'wishitem':wishitem,
        'products': product,

    }
    return render(request,'wishlist.html',context)




def plus_wishlist(request,id):
    
    products=Product.objects.get(id=id)
    print(request.user)
    user=request.user
    WishList.objects.create(user=user,product=products)
    
    return redirect(singleproduct, id)


def minus_wishlist(request,id):
    print("inside minus")
   
    try:
        product=Product.objects.get(id=id)
    except Product.DoesNotExist:
        print("Not exists")
    user=request.user
    WishList.objects.filter(user=user,product=product).delete()
    
    return redirect(singleproduct, id)

