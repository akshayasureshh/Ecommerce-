
from django.urls import path
from .import  views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',views.home,name='home'),
    path('category/',views.categorypage,name='category'),
    path('subcategory/',views.subcategory,name="subcategory"),
    path('productadd/',views.productsAdd,name= 'product_add'),
    path('productlist/',views.Productlist, name='product-list'),
    path('productgrid/',views.Productgrid,name='product-grid'),
    path('backgroundslider/',views.Backgroundslider,name='backgroundslider'),
    path('childslider/',views.Childslider,name='childslider'),
    path('review/',views.Review,name='review'),
     
    path('crop-image/', views.upload_and_crop, name='upload_and_crop'),
    path('userlist/',views.userlist,name='userlist'),
    
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)