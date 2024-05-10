from django.shortcuts import render
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
    return render(request, 'category.html')



def subcategory(request):
    parentCategory = Category.objects.all()
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
    return render(request, 'sub_category.html', {'parentCategory': parentCategory})



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

    return render(request,'productlist.html',{'ProductsDisplay':products})
    


def Productgrid(request):
    products = Product.objects.all()
    return render(request,'productgrid.html',{'ProductsDisplay':products})




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
        print("this is rating :",review.avg_rating)

    return render(request, 'reviews.html', { 'reviews': reviews})




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
    data = OrderPlaced.objects.all()
    datas = Order.objects.all()

    
    # Paginate the products
    paginator = Paginator(datas, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    try:
        datas = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        datas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        datas = paginator.page(paginator.num_pages)
        
    context = {
        'data': data,
        'datas': datas,
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


def ProductDetail(request):
    print("inside fun")
    latest_product = Product.objects.order_by('id').first()  
    print(latest_product)

    return render(request, 'productdetailadmin.html', {'latest_product': latest_product})



def product_edit_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    data = SubCategory.objects.all()
    
    
    if product_id:
        product = get_object_or_404(Product, id=product_id)
    
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

            if product:
                # Update existing product attributes
                product.product_image = data
                product.product_image1 = image1
                product.product_image2 = image2
                product.product_image3 = image3
                product.product_image4 = image4
                product.product_image5 = image5
                product.product_image6 = image6
                product.title = product_name
                product.categories = categories
                product.availability = availability
                product.admin_choice = admin_choice
                product.price = price
                product.description = description
                product.product_tag = tags
                product.quantity = quantity
                product.full_detail = full_detail
                product.slug = slug
                product.color1 = color1
                product.color2 = color2
                product.color3 = color3
                product.color4 = color4
                product.colors = additional_colors
                product.custom_size = custom_size
                product.size = selected_sizes

                product.save()
            else:
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
        
        context = {
            'subcategory': data,
            'product': product,
            'stock_availability': ['IN STOCK', 'OUT OF STOCK'],
            'product_id': product_id  # Pass the product ID to the template
        }

    return render(request, 'productadd3.html', context)


from django.shortcuts import render,redirect
def delete_item_list(request, item_id):
    if request.method == 'POST':
        
        try:
            item = Product.objects.get(id=item_id)
            item.delete()
        except Product.DoesNotExist:
            # Handle the case where the item doesn't exist
            pass
    
        return redirect(Productlist)  
    return render(request, 'productlist.html')
