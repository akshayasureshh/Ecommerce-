
from django.urls import path
from .import  views
from django.conf import settings
from django.conf.urls.static import static
from . views import product_edit_view
# from .utils import encrypt_value


urlpatterns = [

    path('',views.home,name='home'),
    path('category/',views.categorypage,name='category'),
    path('subcategory/',views.subcategory,name="subcategory"),
    path('productadd/',views.productsAdd,name= 'product_add'),
    path('productedit/<str:encrypted_product_id>/', views.product_edit_view, name='product_edit'),
    path('productlist/',views.Productlist, name='productlist'),
    path('productgrid/',views.Productgrid,name='product_grid'),
    # path('productdetail/<str:encrypted_pk>/', views.ProductDetail, name='productdetail'),
    path('backgroundslider/',views.Backgroundslider,name='backgroundslider'),
    # path('childslider/',views.Childslider,name='childslider'),
    path('review/',views.Review,name='review'),
     
    path('crop-image/', views.upload_and_crop, name='upload_and_crop'),
    path('userlist/',views.userlist,name='userlist'),

    path('neworder/',views.neworder,name= "neworder"),
    path('update_order_status/', views.update_order_status, name='update_order_status'),

    path('neworder2/',views.neworderimage,name= "neworder2"),
    path('update_order_status_two/', views.update_order_status_two, name='update_order_status_two'),



    path('orderdetail/',views.order_detail,name='orderdetail'),
    path('orderdetail2/<int:order_id>/', views.order_detail2, name='orderdetail2'),

    path('orderhistory/',views.orderhistory,name='orderhistory'),

    # path('deletelist/<int:item_id>/',views.delete_item_list,name='deletelist'),
    path('deletelist/<str:encrypted_item_id>/', views.delete_item_list, name='deletelist'),
    path('deletelistreview/<int:item_id>',views.delete_item_review,name='deletelistreview'),
    path('deletelistgrid/<int:item_id>/',views.delete_item_grid,name='deletelistgrid'),
    path('deletelistsub/<int:item_id>/',views.delete_item_sub,name='deletelistsub'),
    path('deletelistcate/<int:item_id>/',views.delete_item_cate,name='deletelistcate'),

    

    

    
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)