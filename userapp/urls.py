from django.urls import path
from .import  views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from . forms import MyPasswordResetForm,MySetPasswordForm
from django.contrib.auth import views as auth_views
from .views import toggle_wishlist,resend_otp



urlpatterns = [

    path('home/',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('logout/', views.user_logout, name='logout'),
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

    path('review/<int:product_pk>/',views.review,name='review'),

    path('imageupload/<int:product_pk>/', views.imageupload, name='imageupload'),

    path('checkout/',views.checkout.as_view(),name='checkout'),

    path('paymentdone/',views.payment_done,name='paymentdone'),

    path('search/',views.search_view,name="search"),
  
   path('profile/',views.ProfileView.as_view(),name='profile'),

   path('address/',views.address,name='address'),

    path('updateAddress/<int:pk>',views.updateAddress.as_view(),name='updateAddress'),

    path('orders/',views.orders,name='orders'),

    path('shopall/',views.shopall,name='shopall'),

    # path('pluswish/<int:id>/',views.pluswish,name='pluswish'),

    # path('minuswish/<int:id>/',views.minuswish,name='minuswish'),

    path('send_otp/', views.send_otp, name='send_otp'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('resend_otp/', resend_otp, name='resend_otp'),
    path('password-reset/',views.PasswordReset,name='password-reset'),
    path('password-reset-complete/',views.pwcomplete,name='password_reset_complete'),

   

    path('add_to_cart_index/', views.add_to_cart_index, name='add_to_cart_index'),
    path('add_to_cart_wishlist/', views.add_to_cart_wishlist, name='add_to_cart_wishlist'),

    
    path('autosuggest/',views.autosuggest,name="autosuggest"),

    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/',views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/<int:product_id>/toggle/', toggle_wishlist, name='toggle_wishlist'),

    path('delete-item/<int:item_id>/',views.delete_item, name='delete_item'),

    path('pluscart2/',views.plus_cart_base,name="plus_cart2"),
    path('minuscart2/',views.minus_cart_base,name="minus_cart2"),
    path('removecart2/',views.remove_cart_base,name="remove_cart2"),

    path('cod_confirmation/',views.cod_confirmation,name="cod_confirmation"),

    path('trackorder/',views.trackorder,name='trackorder'),

    path('invoice/',views.invoice,name='invoice'),
    path('invoice/export/',views. invoice, name='export_invoice'),

    path('userprofile/',views.userprofile,name='userprofile'),

    path('add-to-cart-newarrivals/', views.add_to_cart_newarrival, name='add_to_cart_newarrivals'),
    path('add-to-wishlist-newarrivals/',views.add_to_wishlist_newarrivals,name='add_to_wishlist_newarrivals'),

    

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)