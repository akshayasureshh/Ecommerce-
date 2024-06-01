from django.shortcuts import render, redirect
from .models import *
from django.views import View
from django.http import JsonResponse
from userapp . models import Rating,User,OrderPlaced,Order
from django.shortcuts import render, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from .forms import ImageUploadForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg
from django.core.files.base import ContentFile
import base64
from django.urls import reverse
from django.http import Http404
from .utils import encrypt
from django.contrib import messages

# from .utils import encode_url, decode_url 

# Create your views here.


def home(request):
    orders = Order.objects.all()
    return render(request,'home.html',{'orders':orders})


def categorypage(request):
    if request.method == 'POST':
        
        # if 'text' in request.POST:
            name = request.POST['text']
            slug = request.POST['slug']
            sort_description = request.POST['sortdescription']
            full_description =  request.POST['fulldescription']
            product_tags = request.POST['group_tag']
            data = Category()
            data.name = name
            data.slug=slug
            data.full_detail = full_description
            data.sort_description = sort_description
            data.product_tag = product_tags
            data.save()

    cate = Category.objects.all()
    sub = SubCategory.objects.all()
    

    product_counts = {}
    for subcategory in sub:
        product_counts[subcategory.id] = Product.objects.filter(categories=subcategory).count()
        print(product_counts)

    
    

    context={
        'cate':cate,
        'subcate' : sub,
        'product_counts': product_counts,
      
    }
    return render(request, 'category.html',context)


    

def subcategory(request):
    parentCategory = Category.objects.all()
    sub = SubCategory.objects.all()

    if request.method=='POST':
        name = request.POST['text']
        slug = request.POST['slug']
        sort_description = request.POST['sortdescription']
        full_description =  request.POST['fulldescription']
        product_tags = request.POST['group_tag']
        id=request.POST['parent-category']
        image= request.FILES['image1']

        id = Category.objects.filter(id = id).first()
        data = SubCategory()
        data.name = name
        data.slug=slug
        data.full_detail = full_description
        data.sort_description = sort_description
        data.product_tag = product_tags
        data.parent_category = id
        data.image = image
        data.save()

    subcategories_with_counts = []

    for subcategory in sub:
        product_count = Product.objects.filter(categories=subcategory).count()
        subcategories_with_counts.append({
            'subcategory': subcategory,
            'product_count': product_count
        })
       
    
    


    context = {

        'parentCategory': parentCategory,
        'subcategory' : sub,
        'subcategories_with_counts': subcategories_with_counts,
      

       

    }

    
    return render(request, 'sub_category.html', context)

def productsAdd(request):
    print("inside productsAdd view")
    
    data = SubCategory.objects.all()
    
    if request.method == 'POST':
        print("inside POST request")
        
        # Safely retrieve files from request.FILES
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')
        image5 = request.FILES.get('image5')
        image6 = request.FILES.get('image6')

        # Retrieve other form data
        product_name = request.POST.get('product_name', '')
        categories_id = request.POST.get('categories', '')
        availability = request.POST.get('availability', '')
        price = request.POST.get('price', '')
        description = request.POST.get('description', '')
        tags = request.POST.get('group_tag', '')
        quantity = request.POST.get('quantity', '')
        full_detail = request.POST.get('fulldetail', '')
        slug = request.POST.get('slug', '')
        custom_size = request.POST.get('customsize', '')
        admin_choice = request.POST.get('admin_choice', '')
        color1 = request.POST.get('color1', '')
        color2 = request.POST.get('color2', '')
        color3 = request.POST.get('color3', '')
        color4 = request.POST.get('color4', '')
        additional_colors = request.POST.getlist('additionalColor')
        selected_sizes = request.POST.getlist('size')

        # Retrieve cropped image data
        cropped_image_data = request.POST.get('cropped_image_data', '')
        
        # Decode base64 data and save it as a file
        format, imgstr = cropped_image_data.split(';base64,') 
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'cropped_image.{ext}')

        categories = SubCategory.objects.get(id=categories_id)

        # Create a new product instance
        product_details = Product(
            product_image=data,
            product_image1=image1,
            product_image2=image2,
            product_image3=image3,
            product_image4=image4,
            product_image5=image5,
            product_image6=image6,
            title=product_name,
            categories=categories,
            availability=availability,
            admin_choice=admin_choice,
            price=price,
            description=description,
            product_tag=tags,
            quantity=quantity,
            full_detail=full_detail,
            slug=slug,
            color1=color1,
            color2=color2,
            color3=color3,
            color4=color4,
            colors=additional_colors,
            custom_size=custom_size,
            size=selected_sizes,
        )

        product_details.save()

        return redirect(productsAdd)
    
    context = {
        'subcategory': data,
        'stock_availability': ['IN STOCK', 'OUT OF STOCK'],
    }

    return render(request, 'productadd2.html', context)


def Productlist(request):
    products = Product.objects.all()
    paginator = Paginator(products, 10)  # Show 10 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Encrypt product IDs
    for product in page_obj:
        product.encrypted_id = encrypt(str(product.id))

    context = {
        'ProductsDisplay': page_obj,
        'page_obj': page_obj,
    }

    return render(request, 'productlist.html', context)

def Productgrid(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)  # Show 12 products per page or adjust as needed

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'productgrid.html', {'page_obj': page_obj})


def Backgroundslider(request):
    if request.method == 'POST':
        product_image = request.FILES['image']
        heading1 =  request.POST['head1']
        heading2 =  request.POST['head2']
        description = request.POST['description']

        data = BackgroundSliders()
        data.image =  product_image
        data.heading1 = heading1
        data.heading2 = heading2
        data.description = description
        data.save()
    return render(request,'addparentslider.html')



def Childslider(request):
    if request.method == 'POST':
        name = request.POST['name']
        product_image = request.FILES['image']
        data = ChildSliders()
        data.name = name
        data.image =  product_image
        data.save()
    return render(request,'addchildsider.html')


def Review(request):
    reviews = Rating.objects.all()
    
    for review in reviews:
        avg_rating = Rating.objects.filter(product=review.product).aggregate(Avg('rating'))['rating__avg']
        review.avg_rating = round(avg_rating) if avg_rating is not None else 0
        print("this is rating :", review.avg_rating)
    
    paginator = Paginator(reviews, 5)  # Show 10 reviews per page or adjust as needed
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'reviews.html', { 'page_obj': page_obj })



def upload_and_crop(request):
    form = ImageUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'works'})
    context = {'form': form}
    return render(request, 'imagecrop.html', context)


def userlist(request):
    data=User.objects.all()
    return render(request, "users-list.html",{ 'data': data })

def neworder(request):
    order_placed_list = OrderPlaced.objects.all().order_by('-id')
    order_list = Order.objects.exclude(status='delivered').order_by('-id')



    # paginator_order_placed = Paginator(order_placed_list, 10)  # Show 10 OrderPlaced per page
    # paginator_orders = Paginator(order_list, 10)  # Show 10 Orders per page

    # page_number_order_placed = request.GET.get('page_order_placed')
    # page_number_orders = request.GET.get('page_orders')

    # page_obj_order_placed = paginator_order_placed.get_page(page_number_order_placed)
    # page_obj_orders = paginator_orders.get_page(page_number_orders)
    
    context = {
        # 'page_obj_order_placed': page_obj_order_placed,
        # 'page_obj_orders': page_obj_orders,
        'orders' : order_placed_list,
        'ordered_list' : order_list,
    }

    return render(request, "new_order.html", context)


import logging
logger = logging.getLogger(__name__)

def update_order_status(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        delivery_date = request.POST.get('delivery_date')  # Extract delivery date from POST data

        try:
            order = Order.objects.get(order_id=order_id)
            order.status = new_status
            order.delivery_expected_date = delivery_date  # Update delivery date
            order.save()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})

def order_detail(request):
    detail = Order.objects.latest('id')
    details = OrderPlaced.objects.all()

    context={
          'detail': detail,
          'details': details,


    }
    return render(request, 'order_detail.html',context)

def orderhistory(request):
    data = Order.objects.all()
    return render(request,'order_history.html',{'data' : data})


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product
from .utils import decrypt

def ProductDetail(request, encrypted_pk):
    try:
        pk = decrypt(encrypted_pk)
        latest_product = get_object_or_404(Product, pk=pk)
    except Exception as e:
        return HttpResponse("Invalid URL", status=400)

    return render(request, 'productdetailadmin.html', {'latest_product': latest_product})


def product_edit_view(request, encrypted_product_id):
    try:
        # Decrypt the product_id
        product_id = decrypt(encrypted_product_id)
        product = get_object_or_404(Product, id=product_id)
    except Exception as e:
        # Handle decryption error or invalid ID
        return HttpResponse("Invalid URL", status=400)

    data = SubCategory.objects.all()

    if request.method == 'POST':
        try:
            print("inside POST request")
            
            # Safely retrieve files from request.FILES
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')
            image4 = request.FILES.get('image4')
            image5 = request.FILES.get('image5')
            image6 = request.FILES.get('image6')

            # Retrieve other form data
            product_name = request.POST.get('product_name', '')
            categories_id = request.POST.get('categories', '')
            availability = request.POST.get('availability', '')
            price = request.POST.get('price', '')
            description = request.POST.get('description', '')
            tags = request.POST.get('group_tag', '')
            quantity = request.POST.get('quantity', '')
            full_detail = request.POST.get('fulldetail', '')
            slug = request.POST.get('slug', '')
            custom_size = request.POST.get('customsize', '')
            admin_choice = request.POST.get('admin_choice', '')
            color1 = request.POST.get('color1', '')
            color2 = request.POST.get('color2', '')
            color3 = request.POST.get('color3', '')
            color4 = request.POST.get('color4', '')
            additional_colors = request.POST.getlist('additionalColor')
            selected_sizes = request.POST.getlist('size')

            # Retrieve cropped image data
            cropped_image_data = request.POST.get('cropped_image_data', '')
            
            # Decode base64 data and save it as a file
            if cropped_image_data:
                format, imgstr = cropped_image_data.split(';base64,') 
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f'cropped_image.{ext}')

            categories = SubCategory.objects.get(id=categories_id)

            

            if product_name:
                product.title = product_name
            if data:
                product.product_image = data
            if image1:
                product.product_image1 = image1
            if image2:
                product.product_image2 = image2
            if image3:
                product.product_image3 = image3
            if image4:
                product.product_image4 = image4
            if image5:
                product.product_image5 = image5
            if image6:
                product.product_image6 = image6
            if categories:
                product.categories = categories
            if availability:
                product.availability = availability
            if admin_choice:
                product.admin_choice = admin_choice
            if price:
                product.price = price
            if description:
                product.description = description
            if tags:
                product.product_tag = tags
            if quantity:
                product.quantity = quantity
            if full_detail:
                product.full_detail = full_detail
            if slug:
                product.slug = slug
            if color1:
                product.color1 = color1
            if color2:
                product.color2 = color2
            if color3:
                product.color3 = color3
            if color4:
                product.color4 = color4
            if additional_colors:
                product.colors = additional_colors
            if custom_size:
                product.custom_size = custom_size
            if selected_sizes:
                product.size = selected_sizes
            

            product.save()
            messages.success(request, 'Product updated successfully')
            return redirect('product_edit', encrypted_product_id=encrypted_product_id)

        except Exception as e:
            messages.error(request, "An error occurred while updating the product")
            return redirect('product_edit', encrypted_product_id=encrypted_product_id)
        

            

    context = {
        'subcategory': data,
        'product': product,
        'stock_availability': ['IN STOCK', 'OUT OF STOCK'],
        'product_id': encrypted_product_id,  # Pass the encrypted product ID to the template
        'selected_sizes': product.size if product.size else []
    }

    return render(request, 'productadd3.html', context)



def delete_item_list(request, encrypted_item_id):
    try:
        item_id = decrypt(encrypted_item_id)
        item = Product.objects.get(id=item_id)
        item.delete()
    except Exception as e:
        # Handle decryption error or item does not exist
        pass
    
    return redirect('productlist')


def delete_item_review(request, item_id):
    if request.method == 'POST':
        
        try:
            item = Rating.objects.get(id=item_id)
            item.delete()
        except Rating.DoesNotExist:
            # Handle the case where the item doesn't exist
            pass
    
        return redirect(Review)  
    return render(request, 'review.html')



def delete_item_grid(request, item_id):
    if request.method == 'POST':
        
        try:
            item = Product.objects.get(id=item_id)
            item.delete()
        except Product.DoesNotExist:
            # Handle the case where the item doesn't exist
            pass
    
        return redirect(Productgrid)  
    return render(request, 'productgrid.html')


def delete_item_sub(request, item_id):
    if request.method == 'POST':
        
        try:
            item = SubCategory.objects.get(id=item_id)
            item.delete()
        except SubCategory.DoesNotExist:
            # Handle the case where the item doesn't exist
            pass
    
        return redirect(subcategory)  
    return render(request, 'sub_category.html')



def delete_item_cate(request, item_id):
    if request.method == 'POST':
        
        try:
            item = Category.objects.get(id=item_id)
            item.delete()
        except Category.DoesNotExist:
            # Handle the case where the item doesn't exist
            pass
    
        return redirect(subcategory)  
    return render(request, 'category.html')

