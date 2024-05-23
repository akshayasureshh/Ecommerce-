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
import razorpay
from django.conf import settings
from django.views import View
from django.db.models import Sum
from . forms import CustomerProfileForm
from django.urls import reverse
import random
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage

# Create your views here.

# def home(request):
#     data = SubCategory.objects.all()
#     parent_categories = Category.objects.all()
#     parent_slider = BackgroundSliders.objects.all()
#     child_slider = ChildSliders.objects.all()
#     products = Product.objects.all()
#     print("iteration problem:",products)
#     newarrival = Product.objects.latest('id')
#     latest_products = Product.objects.order_by('-id')[:4]
#     # product = Product.objects.get(id=id)
#     wishlist = WishList.objects.filter(Q(product=products) & Q(user=request.user.pk))
#     totalitem = 0
#     wishitem = 0
#     if request.user.is_authenticated:
#         totalitem = Cart.objects.filter(user=request.user).count()
#         wishitem = WishList.objects.filter(user=request.user).count()
    
    
    
    
#     # Calculate total quantity count for each category
#     category_quantities = {}
#     for category in parent_categories:
#         category_products = products.filter(categories__parent_category=category)
#         category_total_quantity = category_products.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
#         category_quantities[category.name] = category_total_quantity
    
    
#     context = {
#         'SubCate': data,
#         'Category': parent_categories,
#         'parent_slider': parent_slider,
#         'child_slider': child_slider,
#         'products': products,
#         'totalitem': totalitem,
#         'wishitem': wishitem,
#         'newarrival': newarrival,
#         'category_quantities': category_quantities,  
#         'latest_products': latest_products,
#         'wishlist' : wishlist,
#     }
#     return render(request, 'index2.html', context)


def home(request):
    context = {}
    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()
    parent_slider = BackgroundSliders.objects.all()
    child_slider = ChildSliders.objects.all()
    products = Product.objects.all()
    print("iteration problem:", products)
    newarrival = Product.objects.latest('id')
    latest_products = Product.objects.order_by('-id')[:4]
    most_ordered_products = OrderPlaced.objects.order_by('-order__ordered_date')
    totalitem = 0
    wishitem = 0
    wishlist = {}
    cart = []
    amount2 = 0
    totalamount2 = 0
    
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = WishList.objects.filter(user=request.user).count()
        cart = Cart.objects.filter(user=request.user)
        amount = sum(cart_item.quantity * cart_item.product.price for cart_item in cart)
        amount2 = amount
        totalamount2 = amount + 40
        user = request.user
        
    else:
        totalitem = 0
        wishitem = 0
        user = None
        cart = []
    


       
    for product in products:
        wishlist = WishList.objects.filter(product=product, user=request.user.pk).exists()

    
    # Calculate total quantity count for each category
    category_quantities = {}
    for category in parent_categories:
        category_products = products.filter(categories__parent_category=category)
        category_total_quantity = category_products.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
        category_quantities[category.name] = category_total_quantity
    

    for product in latest_products:
        print("product id : ", product.id)
        avg_rating = Rating.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

        product.avg_rating = round(avg_rating) if avg_rating is not None else 0
        print("this is rating :",product.avg_rating)


    for i in most_ordered_products:
        print("Most ordered product ID:", i.product.id)
        avg_rating2 = Rating.objects.filter(product=i.product).aggregate(Avg('rating'))['rating__avg']
        i.product.avg_rating2 = round(avg_rating2) if avg_rating2 is not None else 0
        print("This is rating:", i.product.avg_rating2)


    
    for product in products:
        print("product idwdsde : ", product.id)
        avg_rating = Rating.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

        product.avg_rating = round(avg_rating) if avg_rating is not None else 0
        print("this is ratingwdadwdw :",product.avg_rating)
    
    # user=request.user
    # cart=Cart.objects.filter(user=user)
    print("the cart item is",cart)
    amount=0
    for p in cart:
        value = p.quantity*p.product.price
        amount= amount + value
        amount2=amount
        
    totalamount=amount+40
    print(totalamount)
    

    for product in products:
        if product.size and product.size[0] != '':
            try:
                size_list = json.loads(product.size[0])
                context['sizes'] = size_list
            except json.JSONDecodeError:
                # Handle the case where size is not a valid JSON string
                pass
    
    most_ordered = (OrderPlaced.objects
                    .values('product')
                    .annotate(total_quantity=Sum('quantity'))
                    .order_by('-total_quantity')
                    .first())
    
    print("Most Ordered:", most_ordered)  # Debugging statement
    
    product = None
    if most_ordered:
        product_id = most_ordered['product']
        product = Product.objects.get(id=product_id)
        product.total_quantity = most_ordered['total_quantity']
        print("Product Found:", product) 

    


    context = {
        'SubCate': data,
        'Category': parent_categories,
        'parent_slider': parent_slider,
        'child_slider': child_slider,
        'products': products,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'newarrival': newarrival,
        'category_quantities': category_quantities,  
        'latest_products': latest_products,
        'wishlist': wishlist,
        # 'sizes': sizes,
        # 'wishlist_products': wishlist_products,
        'cart' : cart,
        'amount2' : amount2,
        'totalamount2' : totalamount,
        'most_ordered_products': most_ordered_products,
        'most_ordered' : product,
        # 'subcategories_with_products': subcategories_with_products,
    }
      # Append each size_list to sizes list

    # Assign the sizes list to the context dictionary outside the loop
    

    return render(request, 'index2.html', context)



def add_to_wishlist(request, product_id):
    product = Product.objects.get(pk=product_id)
    wishlist, created = WishList.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect('home')

def remove_from_wishlist(request, product_id):
    product = Product.objects.get(pk=product_id)
    wishlist = WishList.objects.get(user=request.user)
    wishlist.products.remove(product)
    return redirect('home')

def toggle_wishlist(request, product_id):
    if request.method == 'POST' and request.is_ajax():
        product = get_object_or_404(Product, pk=product_id)
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        if 'active' in request.POST and request.POST['active'] == 'true':
            wishlist.products.remove(product)
            return JsonResponse({'success': True})
        else:
            wishlist.products.add(product)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# def pluswish(request, id):
#     products = Product.objects.get(id=id)
#     user = request.user
#     WishList.objects.create(user=user, product=products)
    
#     return redirect('home')


# def minuswish(request, id):
#     print("inside minus")
   
#     try:
#         product = Product.objects.get(id=id)
#     except Product.DoesNotExist:
#         print("Not exists")
    
#     user = request.user
#     WishList.objects.filter(user=user, product=product).delete()
    
#     return redirect('home')



def register(request):
     data = SubCategory.objects.all()
     parent_categories = Category.objects.all()
     context ={
          'SubCate':data,
          'Category' : parent_categories,
          
    }
     
     if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Perform basic form validation
        if password1 != password2:
            error_message = "Passwords do not match."
            return render(request, 'register.html', {'error_message': error_message})

        # Create the user
        user = User.objects.create_user(username=name, email=email, password=password1)
        # Optionally, you can log the user in after registration
        # login(request, user)
        return redirect('login')  # Redirect to the login page after successful registration

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


def user_logout(request):
    logout(request)
    return redirect('login')



def productdetail(request,categoryID):
    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()

    products = Product.objects.filter(categories=categoryID)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(WishList.objects.filter(user=request.user))

    else:
        totalitem = 0
        wishitem = 0

    # Fetch sizes
    for product in products:
        product_size = product.size
        print(product_size)

    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    for product in products:
        print("product id : ", product.id)
        avg_rating = Rating.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

        product.avg_rating = round(avg_rating) if avg_rating is not None else 0
        print(product.avg_rating)

    context = {
        'products': products,
        'SubCate':data,
        'Category' : parent_categories,
        'totalitem':totalitem,
        'wishitem':wishitem,
        'page_obj': page_obj,
        'product_sizes': product_size,

          

    }

    return render(request,'productdetail.html',context)

@require_POST
def add_to_cart_productdetail(request):
    # Extract product ID and quantity from the POST data
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    try:
        # Retrieve the product from the database
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # If the product does not exist, return an error response
        return JsonResponse({'error': 'Product does not exist'}, status=400)

    if request.user.is_authenticated:
        # If the user is authenticated, associate the product with the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user, product=product)
    else:
        # For anonymous users, you might handle carts differently
        # For example, using session-based carts
        return JsonResponse({'error': 'Authentication required'}, status=403)

    # Update the quantity of the product in the cart
    cart.quantity += quantity
    cart.save()

    # Return a success response
    return JsonResponse({'message': 'Product added to cart successfully'})


@require_POST
def add_to_wishlist_productdetail(request):
    # Extract product ID from the POST data
    product_id = request.POST.get('product_id')

    try:
        # Retrieve the product from the database
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # If the product does not exist, return an error response
        return JsonResponse({'error': 'Product does not exist'}, status=400)

    if request.user.is_authenticated:
        # If the user is authenticated, add the product to the user's wishlist
        wishlist, created = WishList.objects.get_or_create(user=request.user, product=product)
        if created:
            return JsonResponse({'message': 'Product added to wishlist successfully'})
        else:
            return JsonResponse({'message': 'Product is already in wishlist'})
    else:
        # For anonymous users, you might handle adding to wishlist differently
        # For example, you could prompt them to log in
        return JsonResponse({'error': 'Authentication required'}, status=403)


from django.http import Http404
def singleproduct(request, id):
    context = {}
    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()
    relatedproduct = Product.objects.all()
    product = Product.objects.get(id=id)
    most_ordered_products = OrderPlaced.objects.order_by('-order__ordered_date')

    admin_choice = product.admin_choice
    # if product.size[0] != '':        
    #     size_list = json.loads(product.size[0])        
    #     print(size_list)
    #     context['sizes'] = size_list
    if product.size:
        context['sizes'] = product.size
    reviews = Rating.objects.filter(product=product)
    colors = [product.color1, product.color2, product.color3, product.color4]
    colors = [color.replace("('", "") for color in colors if color]
    print("lala colors",colors)

    wishlist = WishList.objects.filter(Q(product=product) & Q(user=request.user.pk))
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem=len(WishList.objects.filter(user=request.user))   

    if product:
        avg_rating = Rating.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

        product.avg_rating = round(avg_rating) if avg_rating is not None else 0
        print(product.avg_rating)

    for i in most_ordered_products:
        print("Most ordered product ID:", i.product.id)
        avg_rating2 = Rating.objects.filter(product=i.product).aggregate(Avg('rating'))['rating__avg']
        i.product.avg_rating2 = round(avg_rating2) if avg_rating2 is not None else 0
        print("This is rating:", i.product.avg_rating2)


    # for product in relatedproduct:
    #     print("product id : ", product.id)
    #     avg_rating = Rating.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
    #     product.avg_rating = round(avg_rating) if avg_rating is not None else 0
    #     print(product.avg_rating)
       
    context.update({
        'wishlist' : wishlist,
        'product': product,
        'SubCate': data,
        'Category': parent_categories,
        'totalitem':totalitem,
        'wishitem':wishitem,
        'relatedproducts': relatedproduct,
        'reviews': reviews,
        'admin_choice': admin_choice,
        'colors': colors,
        'avg_rating': avg_rating,
        'most_ordered_products': most_ordered_products,
    

    })
    

    return render(request, 'singleproduct.html', context)

def imageupload(request,product_pk):
    user_id = request.user.id
    product_id = product_pk
    if request.method=='POST':
        text=request.POST['your-text']
        image = request.FILES['upload-image']
        product = get_object_or_404(Product, pk=product_id)
        data = ImageUpload.objects.create(
            user_id=user_id,
            product=product,
            text=text,
            image=image,
        )

    return redirect(singleproduct, product_id)



def review(request, product_pk):
    user_id = request.user.id
    product_id = product_pk
    
    if request.method == 'POST':
        rating = request.POST['rating']
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
    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()
    user=request.user
    cart=Cart.objects.filter(user=user)
    latest_products = Product.objects.order_by('-id')[:4]
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
    
    for product in latest_products:
        print("product id : ", product.id)
        avg_rating = Rating.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

        product.avg_rating = round(avg_rating) if avg_rating is not None else 0
        print("this is rating :",product.avg_rating)


    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()
    context = {
        
        'SubCate': data,
        'Category': parent_categories,
        'totalitem':totalitem,
        'wishitem':wishitem,
        'latest_products': latest_products,
        'cart' : cart,
        'totalamount' :  totalamount,
        'amount' : amount,
    }
    return render(request,'cart2.html',context)




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
        # amount2=0
        for p in cart:
            value = p.quantity*p.product.price
            amount= amount + value
            # amount2=amount

        totalamount=amount+40
        #print(prod_id)
        data={
              'quantity':c.quantity,
              'amount':amount,
            #   'amount2': amount2,
              'totalamount':totalamount,
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
        # amount2=0

        for p in cart:
            value = p.quantity*p.product.price
            amount= amount + value
            # amount2=amount

        totalamount=amount+40
        #print(prod_id)
        data={
              'quantity':c.quantity,
              'amount':amount,
            #   'amount2': amount2,
              'totalamount':totalamount,
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
        # amount2=0
        for p in cart:
            value = p.quantity * p.product.price
            amount= amount + value
            # amount2=amount
        totalamount=amount+40
       
        data={
              'quantity':c.quantity,
              'amount':amount,
            #   'amount2': amount2,
              'totalamount':totalamount,
            
        }
        return JsonResponse(data)






# @login_required
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

    user=request.user
    cart=Cart.objects.filter(user=user)
    print("the cart item is",cart)
    amount=0
    for p in cart:
        value = p.quantity*p.product.price
        amount= amount + value
        amount2=amount
        
    totalamount=amount+40
    print(totalamount)
    
    context = {
        'SubCate': data,
        'Category': parent_categories,
        'totalitem':totalitem,
        'wishitem':wishitem,
        'products': product,
        'cart' : cart,
        'amount2' : amount2,
        'totalamount2' : totalamount,

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





# class checkout(View):
#     def get(self, request):
#         # if 'paid' in request.POST:
#             totalitem = 0
#             wishitem = 0
#             if request.user.is_authenticated:
#                 totalitem = len(Cart.objects.filter(user=request.user))
#                 wishitem = len(WishList.objects.filter(user=request.user))

#             user = request.user
#             add = Customer.objects.filter(user=user)
#             cart_items = Cart.objects.filter(user=user)

#             famount = 0
#             for p in cart_items:
#                 value = p.quantity * p.product.price
#                 famount = famount + value
#             totalamount = famount + 40
#             razoramount = int(totalamount * 100)
#             client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#             data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
#             payment_response = client.order.create(data=data)
#             order_id = payment_response['id']
#             order_status = payment_response['status']
#             if order_status == 'created':
#                 payment = Payment(
#                     user=user,
#                     amount=totalamount,
#                     razorpay_order_id=order_id,
#                     razorpay_payment_status=order_status
#                 )
#                 payment.save()
     

#             return render(request, 'checkout.html', locals())

#     def post(self, request):
#         if 'cod' in request.POST:
#             # Handle Cash on Delivery logic
#             # Retrieve form data
#             user_id = request.user.id  # Assuming you have a logged-in user
#             cust_id = request.POST.get('custid')
#             tot_amount = request.POST.get('totamount')

#             # Get product IDs and quantities from the submitted form data
#             product_ids = request.POST.getlist('product_ids[]')
#             quantities = request.POST.getlist('quantities[]')

#             # Create OrderPlaced objects for each item in the cart
#             for product_id, quantity in zip(product_ids, quantities):
#                 Order.objects.create(
#                     user_id=user_id,
#                     customer_id=cust_id,
#                     product_id=product_id,
#                     quantity=quantity,
#                     payment_method='COD',
#                     amount=tot_amount,
#                 )

#             # Redirect to COD confirmation page or display success message
#             return redirect('cod_confirmation')
#         else:
#             # Handle online payment logic (Razorpay or any other payment gateway)
#             pass

#         return render(request, 'checkout.html', locals())


from django.shortcuts import redirect

class checkout(View):
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user)
        data = SubCategory.objects.all()
        parent_categories = Category.objects.all()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))

        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)

        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()

        context = {
            'user': user,
            'cart': cart,
            'data': data,
            'parent_categories': parent_categories,
            'totalitem': totalitem,
            'wishitem': wishitem,
            'add': add,
            'cart_items': cart_items,
            'famount': famount,
            'totalamount': totalamount,
            'razoramount': razoramount,
            'order_id': order_id,
            'order_status': order_status
        }

        return render(request, 'checkout.html', context)

    def post(self, request):
        if 'cod' in request.POST:
            user = request.user
            cust_id = request.POST.get('custid')
            tot_amount = request.POST.get('totamount')

            # Retrieve the selected address ID from the form data
            address_id = request.POST.get('cust')

            # Create a single order for all products in the cart
            order = Order.objects.create(
                user=user,
                customer_id=cust_id,
                amount=tot_amount,
                payment_method='COD',
                address_id=address_id  # Save the selected address ID with the order
            )

            # Get product IDs and quantities from the submitted form data
            product_ids = request.POST.getlist('product_ids[]')
            quantities = request.POST.getlist('quantities[]')

            # Create OrderPlaced objects for each item in the cart
            for product_id, quantity in zip(product_ids, quantities):
                OrderPlaced.objects.create(
                    order=order,
                    product_id=product_id,
                    quantity=quantity
                )

            # Redirect to COD confirmation page or display success message
            return redirect('cod_confirmation')
        else:
            # Handle online payment logic (Razorpay or any other payment gateway)
            pass

        return render(request, 'checkout.html', locals())

def cod_confirmation(request):
    return render(request,'cod_orderplaced.html')


# @login_required
def payment_done(request):
    user = request.user
    # print(request.user)
    if user.is_authenticated:
        
     order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    #print("payment_done :oid=",order_id,"pid=",payment_id,"cid=",cust_id)
    user=request.user
    #return redirect("orders")
    customer=User.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id=payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    cart.save()
    for c in cart:
        print(c)
    OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
    #c.delete()
    Cart.objects.filter(user=request.user).delete()
    return redirect("home")



def search_view(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')
        product = Product.objects.filter(title__icontains=search_query) 

        data = SubCategory.objects.all()
        parent_categories = Category.objects.all()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
            wishitem = WishList.objects.filter(user=request.user).count()
        
        context = {
        
        'SubCate': data,
        'Category': parent_categories,
        'totalitem':totalitem,
        'wishitem':wishitem,
        'product': product,
    }

        return render(request, 'search.html', context)
    return render(request, 'index2.html')




# @method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        totalitem = 0
        wishitem=0

        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
           wishitem=len(WishList.objects.filter(user=request.user))

        data = SubCategory.objects.all()
        parent_categories = Category.objects.all()
        context = {
        'SubCate': data,
        'Category': parent_categories,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'form' : form,
    }

        return render(request,'user-profile.html',context)
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']


            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations ! Profile saved successfully")
        else:
            messages.success(request,"Invalid input data")

        return render(request,'user-profile.html',locals())
            

# @login_required        
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) 
        wishitem = len(WishList.objects.filter(user=request.user))

    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()
    context = {
        'SubCate': data,
        'Category': parent_categories,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'add' : add,
    }

    return render(request, 'address.html', context)


# @method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
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
            'totalitem': totalitem,
            'wishitem': wishitem,
            'form': form,
     }

    

        return render(request,'updateaddress.html',context)

    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
            
        return redirect("address")


# @login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    order_placed = []

    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = WishList.objects.filter(user=request.user).count()   
        
    order_placed = OrderPlaced.objects.filter(user=request.user)
    
    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()
         

    context = {
        'totalitem': totalitem,
        'wishitem': wishitem,
        'order_placed': order_placed,
        'SubCate': data,
        'Category': parent_categories,
    }
    return render(request, 'order.html', context)




from django.db.models import Avg
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def shopall(request):
    print("inside  shop all")
    products = Product.objects.all()

    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()

    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = WishList.objects.filter(user=request.user).count() 

    for product in products:
        print("product id : ", product.id)
        avg_rating = Rating.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']

        product.avg_rating = round(avg_rating) if avg_rating is not None else 0
        print(product.avg_rating)
   
    # Paginate the products
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)


    context = {
        'products': products,
        'SubCate': data,
        'Category': parent_categories,
        'totalitem': totalitem,
        'wishitem': wishitem,
    }
    return render(request, 'shopall.html', context)




# @login_required
def send_otp_email(user_email):
    
    otp = str(random.randint(100000, 999999))
    send_mail(
       'Password Reset OTP',
        f'Your OTP for password reset is: {otp}',
        'your_email@example.com',  
        [user_email],
        fail_silently=False,
    )
    return otp

# View for sending OTP
# @login_required
# def send_otp(request):
#     data = SubCategory.objects.all()
#     parent_categories = Category.objects.all()
#     totalitem = Cart.objects.filter(user=request.user).count()
#     wishitem = WishList.objects.filter(user=request.user).count() 


#     if request.method == 'POST':
#         user_email = request.POST.get('email')
        
#         if user_email:
#             otp = send_otp_email(user_email)
#             request.session['otp'] = otp  
#             return redirect('otp_verification')  
#         else:
#             messages.error(request, 'Please enter a valid email address.')

    
    

#     context = {
        
#         'SubCate': data,
#         'Category': parent_categories,
#         'totalitem': totalitem,
#         'wishitem': wishitem,
#     }

#     return render(request, 'send_otp.html',context) 


def send_otp(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        
        if user_email:
            # Generate OTP
            otp = generate_otp()

            # Send OTP to the provided email address
            send_mail(
                'Your OTP',
                f'Your OTP is: {otp}',
                'sender@example.com',  # Update with your email address
                [user_email],
                fail_silently=False,
            )

            # Store OTP in session
            request.session['otp'] = otp  

            # Redirect to OTP verification page
            return redirect('otp_verification')  
        else:
            messages.error(request, 'Please enter a valid email address.')
    
    # If not a POST request or email is not provided, render the send OTP page
    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()

    totalitem = 0
    wishitem = 0

    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = WishList.objects.filter(user=request.user).count()

    else:
        totalitem = 0
        wishitem = 0

    context = {
        'SubCate': data,
        'Category': parent_categories,
        'totalitem': totalitem,
        'wishitem': wishitem,
    }

    return render(request, 'send_otp.html', context)

def generate_otp():
    # Generate a 6-digit OTP
    return ''.join(random.choices('0123456789', k=6))



@csrf_exempt
def resend_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_email = data.get('email')

        if user_email:
            try:
                # Generate new OTP
                new_otp = generate_otp()

                # Send new OTP to the provided email address
                send_mail(
                    'Your New OTP',
                    f'Your new OTP is: {new_otp}',
                    'sender@example.com',  # Replace with your email address
                    [user_email],
                    fail_silently=False,
                )

                # Update session with the new OTP
                request.session['otp'] = new_otp  

                # Return a success response
                return JsonResponse({'success': True})
            except Exception as e:
                # Return an error response if email sending fails
                return JsonResponse({'error': str(e)}, status=500)
        else:
            # Return an error response if email is not provided
            return JsonResponse({'error': 'Please provide a valid email address.'}, status=400)
    else:
        # Return a method not allowed response if request method is not POST
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)
    
# View for OTP verification
#@login_required
def otp_verification(request):
    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()
    
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        
        # Check if OTP has expired
        if 'otp_generated_time' in request.session:
            otp_generated_time = request.session['otp_generated_time']
            if timezone.now() > otp_generated_time + timedelta(seconds=60):
                request.session.flush()
                messages.error(request, 'OTP has expired. Please request a new one.')
                # return redirect('send_otp')

        if entered_otp == stored_otp:
            return render(request, 'password-reset.html')  
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    # Calculate the remaining time for OTP expiration
    remaining_time = 0
    if 'otp_generated_time' in request.session:
        otp_generated_time = request.session['otp_generated_time']
        remaining_time = max(0, 60 - (timezone.now() - otp_generated_time).total_seconds())

    totalitem = 0
    wishitem = 0

    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = WishList.objects.filter(user=request.user).count()

    else:
        totalitem = 0
        wishitem = 0

    context = {
        'SubCate': data,
        'Category': parent_categories,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'remaining_time': remaining_time,  # Pass remaining time to template
    }

    return render(request, 'otp_verification.html', context)

# #@login_required
# def password_reset(request):
#     if request.method == 'POST':
#         user=request.user
#         # Reset the user's password and clear the OTP session
#         new_password = request.POST.get('new_password')
#         # Set the new password for the user
#         # You can use Django's built-in password reset functionality or your custom logic
#         # For example, using Django's built-in functionality:
#         user.set_password(new_password)
#         user.save()
        
#         del request.session['otp']  # Clear the stored OTP from the session
#         messages.success(request, 'Password reset successful. You can now log in with your new password.')
#         return redirect('password_reset_complete')  

#     return render(request, 'password_reset.html')  


    
def PasswordReset(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            user = request.user
            if user.is_authenticated:
                # If user is authenticated, update their password
                user.set_password(new_password)
                user.save()
                
                # Clear the stored OTP from the session if it exists
                if 'otp' in request.session:
                    del request.session['otp']
                    
                # messages.success(request, 'Password reset successful. You can now log in with your new password.')
                return redirect('login')
            else:
                # If user is not authenticated, get their username or email
                username_or_email = request.POST.get('username_or_email')
                user = None
                try:
                    # Check if the username or email provided exists in the database
                    user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))
                except User.DoesNotExist:
                    messages.error(request, 'User not found.')
                if user:
                    # Set the new password for the user and save
                    user.set_password(new_password)
                    user.save()
                    
                    # Clear the stored OTP from the session if it exists
                    if 'otp' in request.session:
                        del request.session['otp']
                    
                    # messages.success(request, 'Password reset successful. You can now log in with your new password.')
                    return redirect('login')
                else:
                    messages.error(request, 'User not found.')
        else:
            messages.error(request, 'Passwords do not match.')
    
    return render(request, 'password-reset.html')



def pwcomplete(request):
    return render(request,"password_reset_complete.html")



def autosuggest(request):
    print("autosuggest",request.GET)
    query_original = request.GET.get('term')
    queryset = Product.objects.filter(title__icontains=query_original) 
    mylist = []
    mylist += [x.title for x in queryset]
    return JsonResponse(mylist, safe=False)


def delete_item(request, item_id):
    if request.method == 'POST':
        
        try:
            item = WishList.objects.get(id=item_id)
            item.delete()
        except WishList.DoesNotExist:
            # Handle the case where the item doesn't exist
            pass
    
        return redirect('wishlist')  
    return render(request, 'wishlist.html')




# @login_required
def add_to_cart_wishlist(request):
    user = request.user
    print("lalala",user)
    product_id = request.GET.get('prod_id')
    print(product_id)
    # Check if product_id is provided and not empty
    if not product_id:
        return HttpResponseBadRequest("Product ID is missing")

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseBadRequest("Product does not exist")

    # Create a Cart object for the user and product
    Cart(user=user, product=product).save()

    return redirect(reverse('wishlist'))




# # @login_required
# def show_cart(request):
#     user=request.user
#     cart=Cart.objects.filter(user=user)
#     amount=0
#     for p in cart:
#         value = p.quantity*p.product.price
#         amount= amount + value
#         amount2=amount
        
#     totalamount=amount+40
#     totalitem = 0
#     wishitem = 0
#     if request.user.is_authenticated:
#         totalitem = len(Cart.objects.filter(user=request.user))
#         wishitem=len(WishList.objects.filter(user=request.user))
    
#     context = {
#         'totalitem':totalitem,
#         'wishitem':wishitem,
#     }
#     return render(request,'index2.html',locals())




# @login_required
def plus_cart_base(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        print("this is product id",prod_id)
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount2=0
        # amount2=0
        for p in cart:
            value = p.quantity*p.product.price
            amount2= amount2 + value
            # amount2=amount

        totalamount2=amount2+40
        #print(prod_id)
        data={
              'quantity':c.quantity,
              'amount':amount2,
            #   'amount2': amount2,
              'totalamount2':totalamount2,
        }
        return JsonResponse(data)



# @login_required
def minus_cart_base(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount2=0
        # amount2=0

        for p in cart:
            value = p.quantity*p.product.price
            amount2= amount2 + value
            # amount2=amount

        totalamount2=amount2+40
        #print(prod_id)
        data={
              'quantity':c.quantity,
              'amount2':amount2,
            #   'amount2': amount2,
              'totalamount2':totalamount2,
        }
        return JsonResponse(data)


# @login_required
def remove_cart_base(request):
    if request.method=="GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        # amount2=0
        for p in cart:
            value = p.quantity * p.product.price
            amount= amount + value
            # amount2=amount
        totalamount=amount+40
       
        data={
              'quantity':c.quantity,
              'amount':amount,
            #   'amount2': amount2,
              'totalamount':totalamount,
            
        }
        return JsonResponse(data)


def trackorder(request):
    orders = Order.objects.filter(user=request.user)
    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()
    totalitem = Cart.objects.filter(user=request.user).count()
    wishitem = WishList.objects.filter(user=request.user).count()

    context = {
        
        'SubCate': data,
        'Category': parent_categories,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'orders': orders
    }

    return render(request, 'track_order.html', context)

def invoice(request):
    # Retrieve the latest order for the user, if any
    try:
        order = Order.objects.filter(user=request.user).latest('ordered_date')
    except Order.DoesNotExist:
        order = None

    # Retrieve all order items
    orders = OrderPlaced.objects.all()

    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()
    totalitem = Cart.objects.filter(user=request.user).count()
    wishitem = WishList.objects.filter(user=request.user).count()

    subtotal = 0
    if order:
        # Iterate through each order item and calculate the subtotal
        for order_item in orders:
            if order_item.order_id == order.id:
                subtotal += order_item.quantity * order_item.product.price

    # Calculate total amount including taxes or other charges
    totalamount = subtotal + 352

    context = {
        'order': order,
        'orders': orders,
        'subtotal': subtotal,
        'totalamount': totalamount,
        'SubCate': data,
        'Category': parent_categories,
        'totalitem': totalitem,
        'wishitem': wishitem,
    }

    # Check if export request
    if 'export' in request.GET and order:
        # Generate PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        
        # Create PDF document
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        
        # Create PDF table
        data = [['Product', 'Quantity', 'Price', 'Amount']]
        for order_item in orders:
            if order_item.order_id == order.id:
                data.append([order_item.product.title, order_item.quantity, order_item.product.price, order_item.amount])
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        elements.append(table)
        
        # Build PDF document
        doc.build(elements)
        return response

    return render(request, 'invoice.html', context)

def userprofile(request):
    # Retrieve the Customer object for the current user
    registered_user = User.objects.all()
    data = SubCategory.objects.all()
    parent_categories = Category.objects.all()
    
    # Define default background image URL
    default_background_image = "{% static '/images/banner/8.jpg' %}"

    if request.method == 'POST':
        # Retrieve data from the form
        image1 = request.POST.get('image1')
        image2 = request.POST.get('image2')
        name = request.POST.get('name')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        address3 = request.POST.get('address3')
        email1 = request.POST.get('email1')
        email2 = request.POST.get('email2')
        phone1 = request.POST.get('phone1')
        phone2 = request.POST.get('phone2')

        if customer:
            # Update only the fields that were submitted in the form
            if name:
                customer.name = name
            if address1:
                customer.address1 = address1
            if address2:
                customer.address2 = address2
            if address3:
                customer.address3 = address3
            if email1:
                customer.email1 = email1
            if email2:
                customer.email2 = email2
            if phone1:
                customer.mobile = phone1
            if phone2:
                customer.mobile2 = phone2
            if image1:
                customer.image1 = image1
            if image2:
                customer.image2 = image2
            customer.save()
            messages.success(request, "Congratulations! Profile updated successfully.")
        else:
            # Create a new Customer object and save it
            customer = Customer(
                user=request.user,
                name=name,
                address1=address1,
                address2=address2,
                address3=address3,
                email1=email1,
                email2=email2,
                mobile2=phone2,
                mobile=phone1,
                image1=image1,
                image2=image2,
            )
            customer.save()
            messages.success(request, "Congratulations! Profile created successfully.")

        # If customer has an image, get its URL
        background_image_url = customer.image1.url if customer and customer.image1 else default_background_image

    else:
        # If it's a GET request, just set default background image URL
        background_image_url = default_background_image

    totalitem = 0
    wishitem = 0
    customer = {}

    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = WishList.objects.filter(user=request.user).count()
        customer = Customer.objects.filter(user=request.user).first()


    else:
        totalitem = 0
        wishitem = 0

    context = {
        'customer': customer,
        'background_image_url': background_image_url,
        'SubCate': data,
        'Category': parent_categories,
        'totalitem': totalitem,
        'wishitem': wishitem,
        'registered_user' : registered_user,
        
    }

    
    # Render the form with existing user details
    return render(request, 'userprofile2.html', context)


def add_to_cart_newarrival(request):
    user = request.user
    product_id = request.GET.get('prod_id')

    # Check if product_id is provided and not empty
    if not product_id:
        return HttpResponseBadRequest("Product ID is missing")

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponseBadRequest("Product does not exist")

    # Check if the product is already in the user's cart
    try:
        cart_item = Cart.objects.get(user=user, product=product)
        # If the item is already in the cart, add a message
        messages.info(request, 'Item already exists in the cart.')
    except Cart.DoesNotExist:
        # If the item is not in the cart, create a new Cart object for the user and product
        Cart(user=user, product=product).save()
        # Add a success message indicating that the item was successfully added to the cart
        messages.success(request, 'Item added to cart.')

    # Redirect back to the home page
    return redirect(reverse('home'))

# @login_required
def add_to_cart_tabmen(request):
    # Extract product ID and quantity from the POST data
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    try:
        # Retrieve the product from the database
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # If the product does not exist, return an error response
        return JsonResponse({'error': 'Product does not exist'}, status=400)

    if request.user.is_authenticated:
        # If the user is authenticated, associate the product with the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user, product=product)
    else:
        # For anonymous users, you might handle carts differently
        # For example, using session-based carts
        return JsonResponse({'error': 'Authentication required'}, status=403)

    # Update the quantity of the product in the cart
    cart.quantity += quantity
    cart.save()

    # Return a success response
    return JsonResponse({'message': 'Product added to cart successfully'})

# @login_required
def add_to_wishlist_tabmen(request):
    # Extract product ID from the POST data
    product_id = request.POST.get('product_id')

    try:
        # Retrieve the product from the database
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # If the product does not exist, return an error response
        return JsonResponse({'error': 'Product does not exist'}, status=400)

    if request.user.is_authenticated:
        # If the user is authenticated, add the product to the user's wishlist
        wishlist, created = WishList.objects.get_or_create(user=request.user, product=product)
        if created:
            return JsonResponse({'message': 'Product added to wishlist successfully'})
        else:
            return JsonResponse({'message': 'Product is already in wishlist'})
    else:
        # For anonymous users, you might handle adding to wishlist differently
        # For example, you could prompt them to log in
        return JsonResponse({'error': 'Authentication required'}, status=403)




# @login_required
def add_to_cart_tabwomen(request):
    # Extract product ID and quantity from the POST data
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    try:
        # Retrieve the product from the database
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # If the product does not exist, return an error response
        return JsonResponse({'error': 'Product does not exist'}, status=400)

    if request.user.is_authenticated:
        # If the user is authenticated, associate the product with the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user, product=product)
    else:
        # For anonymous users, you might handle carts differently
        # For example, using session-based carts
        return JsonResponse({'error': 'Authentication required'}, status=403)

    # Update the quantity of the product in the cart
    cart.quantity += quantity
    cart.save()

    # Return a success response
    return JsonResponse({'message': 'Product added to cart successfully'})

# @login_required
def add_to_wishlist_tabwomen(request):
    # Extract product ID from the POST data
    product_id = request.POST.get('product_id')

    try:
        # Retrieve the product from the database
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # If the product does not exist, return an error response
        return JsonResponse({'error': 'Product does not exist'}, status=400)

    if request.user.is_authenticated:
        # If the user is authenticated, add the product to the user's wishlist
        wishlist, created = WishList.objects.get_or_create(user=request.user, product=product)
        if created:
            return JsonResponse({'message': 'Product added to wishlist successfully'})
        else:
            return JsonResponse({'message': 'Product is already in wishlist'})
    else:
        # For anonymous users, you might handle adding to wishlist differently
        # For example, you could prompt them to log in
        return JsonResponse({'error': 'Authentication required'}, status=403)







# @login_required
def add_to_cart_tabchild(request):
    # Extract product ID and quantity from the POST data
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    try:
        # Retrieve the product from the database
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # If the product does not exist, return an error response
        return JsonResponse({'error': 'Product does not exist'}, status=400)

    if request.user.is_authenticated:
        # If the user is authenticated, associate the product with the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user, product=product)
    else:
        # For anonymous users, you might handle carts differently
        # For example, using session-based carts
        return JsonResponse({'error': 'Authentication required'}, status=403)

    # Update the quantity of the product in the cart
    cart.quantity += quantity
    cart.save()

    # Return a success response
    return JsonResponse({'message': 'Product added to cart successfully'})

# @login_required
def add_to_wishlist_tabchild(request):
    # Extract product ID from the POST data
    product_id = request.POST.get('product_id')

    try:
        # Retrieve the product from the database
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # If the product does not exist, return an error response
        return JsonResponse({'error': 'Product does not exist'}, status=400)

    if request.user.is_authenticated:
        # If the user is authenticated, add the product to the user's wishlist
        wishlist, created = WishList.objects.get_or_create(user=request.user, product=product)
        if created:
            return JsonResponse({'message': 'Product added to wishlist successfully'})
        else:
            return JsonResponse({'message': 'Product is already in wishlist'})
    else:
        # For anonymous users, you might handle adding to wishlist differently
        # For example, you could prompt them to log in
        return JsonResponse({'error': 'Authentication required'}, status=403)





# @login_required
def add_to_cart_taball(request):
    # Extract product ID and quantity from the POST data
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    try:
        # Retrieve the product from the database
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # If the product does not exist, return an error response
        return JsonResponse({'error': 'Product does not exist'}, status=400)

    if request.user.is_authenticated:
        # If the user is authenticated, associate the product with the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user, product=product)
    else:
        # For anonymous users, you might handle carts differently
        # For example, using session-based carts
        return JsonResponse({'error': 'Authentication required'}, status=403)

    # Update the quantity of the product in the cart
    cart.quantity += quantity
    cart.save()

    # Return a success response
    return JsonResponse({'message': 'Product added to cart successfully'})

# @login_required
def add_to_wishlist_taball(request):
    # Extract product ID from the POST data
    product_id = request.POST.get('product_id')

    try:
        # Retrieve the product from the database
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # If the product does not exist, return an error response
        return JsonResponse({'error': 'Product does not exist'}, status=400)

    if request.user.is_authenticated:
        # If the user is authenticated, add the product to the user's wishlist
        wishlist, created = WishList.objects.get_or_create(user=request.user, product=product)
        if created:
            return JsonResponse({'message': 'Product added to wishlist successfully'})
        else:
            return JsonResponse({'message': 'Product is already in wishlist'})
    else:
        # For anonymous users, you might handle adding to wishlist differently
        # For example, you could prompt them to log in
        return JsonResponse({'error': 'Authentication required'}, status=403)


# @login_required
# @require_POST
def add_to_wishlist_newarrivals(request):
    product_id = request.POST.get('product_id')

    if not product_id:
        return JsonResponse({'error': 'No product ID provided'}, status=400)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product does not exist'}, status=400)

    wishlist, created = WishList.objects.get_or_create(user=request.user, product=product)
    if created:
        return JsonResponse({'message': 'Product added to wishlist successfully'})
    else:
        return JsonResponse({'message': 'Product is already in wishlist'})



# @login_required
# @require_POST
def add_to_cart_shopall(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')

    if not product_id:
        print("No product ID provided")  # Debug: Check if product ID is missing
        return JsonResponse({'error': 'No product ID provided'}, status=400)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product does not exist'}, status=400)

    # Assuming you have a Cart model and user is authenticated
    cart, created = Cart.objects.get_or_create(user=request.user, product=product, defaults={'quantity': quantity})
    if not created:
        cart.quantity += int(quantity)
        cart.save()

    return JsonResponse({'message': 'Product added to cart successfully'})

# @login_required
# @require_POST
def add_to_wishlist_shopall(request):
    product_id = request.POST.get('product_id')

    if not product_id:
        print("No product ID provided")  # Debug: Check if product ID is missing
        return JsonResponse({'error': 'No product ID provided'}, status=400)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product does not exist'}, status=400)

    wishlist, created = WishList.objects.get_or_create(user=request.user, product=product)
    if created:
        return JsonResponse({'message': 'Product added to wishlist successfully'})
    else:
        return JsonResponse({'message': 'Product is already in wishlist'})