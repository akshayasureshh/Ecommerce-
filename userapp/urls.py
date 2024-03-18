from django.urls import path
from .import  views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path('home/',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('product-detail/<int:categoryID>/',views.productdetail,name='product-detail'),
    path('singleproduct/<int:id>/', views.singleproduct, name='singleproduct'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('pluscart/',views.plus_cart,name="plus_cart"),
    path('minuscart/',views.minus_cart,name="minus_cart"),
    path('removecart/',views.remove_cart,name="remove_cart"),

    path('wishlist/',views.show_wishlist,name='wishlist'),
    path('pluswishlist/<int:id>',views.plus_wishlist,name="plus_wishlist"),
    path('minuswishlist/<int:id>/',views.minus_wishlist,name="minus_wishlist"),
    # path('update_wishlist/<int:product_id>/', views.update_wishlist, name='update_wishlist'),


  
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)