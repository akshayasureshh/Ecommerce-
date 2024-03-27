from django.shortcuts import render
from .models import *
from django.views import View
from django.http import JsonResponse
from userapp . models import Rating
from django.shortcuts import render, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.


def home(request):
    return render(request,'home.html')


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

        id = Category.objects.filter(id = id).first()
        data = SubCategory()
        data.name = name
        data.slug=slug
        data.full_detail = full_description
        data.sort_description = sort_description
        data.product_tag = product_tags
        data.parent_category = id
        data.save()
    return render(request, 'sub_category.html', {'parentCategory': parentCategory})



# def productsAdd(request):
#     data = SubCategory.objects.all()
#     # stock = Product.objects.all()
#     if request.method=='POST':
        
#         product_image = request.FILES['product_image']
#         image1 = request.FILES['image1']
#         image2 = request.FILES['image2']
#         image3 = request.FILES['image3']
#         image4 = request.FILES['image4']
#         image5 = request.FILES['image5']
#         image6 = request.FILES['image6']
#         product_name = request.POST['product_name']
#         categories = request.POST['categories']
#         availability = request.POST['availability']
#         size = request.POST['size']
#         price = request.POST['price']
#         description = request.POST['description']
#         tags = request.POST['group_tag']
#         color1 = request.POST.get('color1', '#ff6191')
#         color2 = request.POST.get('color2', '#33317d')
#         color3 = request.POST.get('color3', '#56d4b7')
#         color4 = request.POST.get('color4', '#009688')

#         quantity = request.POST['quantity']
#         full_detail = request.POST['fulldetail']
#         slug = request.POST['slug']

#         categories = SubCategory.objects.filter(id = categories).first()
        

#         product_details = Product()

        
#         product_details.product_image = product_image
#         product_details.product_image1 = image1
#         product_details.product_image2 = image2
#         product_details.product_image3 = image3
#         product_details.product_image4 = image4
#         product_details.product_image5 = image5
#         product_details.product_image6 = image6
#         product_details.title= product_name
#         product_details.categories = categories
#         product_details.availability = availability
#         product_details.size = size
#         product_details.price = price
#         product_details.description = description
#         product_details.product_tag = tags 
#         product_details.color1 = color1
#         product_details.color2 = color2
#         product_details.color3 = color3
#         product_details.color4 = color4
#         product_details.quantity = quantity
#         product_details.full_detail = full_detail
#         product_details.slug = slug
#         product_details.save()


#     context= {
#             'subcategory' : data,
#             # 'stock_availability' : stock,
#             'stock_availability' : ['IN STOCK','OUT OF STOCK'],
            
#         }

#     return render(request,'productadd.html',context)



# def productsAdd(request):
#     data = SubCategory.objects.all()
#     print("im ready to get inside the if")
#     if request.method == 'POST':
#         print("im inside the if:")
        
#         product_image = request.FILES['product_image']
#         image1 = request.FILES['image1']
#         image2 = request.FILES['image2']
#         image3 = request.FILES['image3']
#         image4 = request.FILES['image4']
#         image5 = request.FILES['image5']
#         image6 = request.FILES['image6']
#         product_name = request.POST['product_name']
#         categories_id = request.POST['categories']
#         availability = request.POST['availability']
    
#         price = request.POST['price']
#         description = request.POST['description']
#         tags = request.POST['group_tag']
#         quantity = request.POST['quantity']
#         full_detail = request.POST['fulldetail']
#         slug = request.POST['slug']
#         custom_size =request.POST['customsize']
#         admin_choice = request.POST['admin_choice']
#         color1= request.POST.get('color1'),
#         color2= request.POST.get('color2'),
#         color3= request.POST.get('color3'),
#         color4= request.POST.get('color4'),
#         additional_colors = request.POST.getlist('additionalColor')
        
        
#         # Handle checkboxes for sizes
#         selected_sizes = request.POST.getlist('selectedSizes', [])
#         # Convert the list of selected sizes to a JSON-friendly format (e.g., list)
#         selected_sizes_json = selected_sizes

        
        
#         # Get the category based on the provided ID
#         categories = SubCategory.objects.filter(id=categories_id).first()
#                 # Create a new product instance
#         product_details = Product(
#         product_image=product_image,
#         product_image1=image1,
#         product_image2=image2,
#         product_image3=image3,
#         product_image4=image4,
#         product_image5=image5,
#         product_image6=image6,
#         title=product_name,
#         categories=categories,
#         availability=availability,
#         admin_choice=admin_choice,
#         price=price,
#         description=description,
#         product_tag=tags,
#         quantity=quantity,
#         full_detail=full_detail,
#         slug=slug,
#         color1=color1,
#         color2=color2,  
#         color3=color3,  
#         color4=color4,
#         colors=additional_colors,
#         custom_size=custom_size,
#         size=selected_sizes_json,
        
#         )
    
#         product_details.save()
                    

#     context = {
#             'subcategory': data,
#             'stock_availability': ['IN STOCK', 'OUT OF STOCK'],
#         }

#     return render(request, 'productadd.html', context)



def productsAdd(request):
    data = SubCategory.objects.all()
    if request.method == 'POST':
        try:
            product_image = request.FILES['product_image']
            # Check if other images are uploaded
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')
            image4 = request.FILES.get('image4')
            image5 = request.FILES.get('image5')
            image6 = request.FILES.get('image6')
        except MultiValueDictKeyError:
            # Handle missing files here, or you can ignore this error
            pass

        # Your other form data retrieval code here
        product_name = request.POST['product_name']
        categories_id = request.POST['categories']
        availability = request.POST['availability']
    
        price = request.POST['price']
        description = request.POST['description']
        tags = request.POST['group_tag']
        quantity = request.POST['quantity']
        full_detail = request.POST['fulldetail']
        slug = request.POST['slug']
        custom_size =request.POST['customsize']
        admin_choice = request.POST['admin_choice']
        color1= request.POST.get('color1'),
        color2= request.POST.get('color2'),
        color3= request.POST.get('color3'),
        color4= request.POST.get('color4'),
        additional_colors = request.POST.getlist('additionalColor')

        
#         # Handle checkboxes for sizes
        selected_sizes = request.POST.getlist('selectedSizes', [])
        # Convert the list of selected sizes to a JSON-friendly format (e.g., list)
        selected_sizes_json = selected_sizes

        categories = SubCategory.objects.filter(id=categories_id).first()
        # Create a new product instance
        product_details = Product(
            product_image=product_image,
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
            size=selected_sizes_json,
        )

        product_details.save()

    context = {
        'subcategory': data,
        'stock_availability': ['IN STOCK', 'OUT OF STOCK'],
    }

    return render(request, 'productadd.html', context)





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

    return render(request, 'reviews.html', { 'reviews': reviews})