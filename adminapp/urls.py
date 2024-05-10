
from django.urls import path
from .import  views
from django.conf import settings
from django.conf.urls.static import static
from . views import product_edit_view


urlpatterns = [

    path('',views.home,name='home'),
    path('category/',views.categorypage,name='category'),
    path('subcategory/',views.subcategory,name="subcategory"),
    path('productadd/',views.productsAdd,name= 'product_add'),
    path('productedit/<int:product_id>/', product_edit_view, name='product_edit'),
    path('productlist/',views.Productlist, name='productlist'),
    path('productgrid/',views.Productgrid,name='product-grid'),
    path('productdetail/',views.ProductDetail,name='productdetail'),
    path('backgroundslider/',views.Backgroundslider,name='backgroundslider'),
    path('childslider/',views.Childslider,name='childslider'),
    path('review/',views.Review,name='review'),
     
    path('crop-image/', views.upload_and_crop, name='upload_and_crop'),
    path('userlist/',views.userlist,name='userlist'),

    path('neworder/',views.neworder,name= "neworder"),
    path('update_order_status/', views.update_order_status, name='update_order_status'),

    path('orderdetail/',views.order_detail,name='orderdetail'),

    path('orderhistory/',views.orderhistory,name='orderhistory'),

    path('deletelist/<int:item_id>/',views.delete_item_list,name='deletelist'),
    
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)