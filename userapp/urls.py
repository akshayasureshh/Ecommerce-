from django.urls import path
from .import  views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from . forms import MyPasswordResetForm,MySetPasswordForm
from django.contrib.auth import views as auth_views



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

    path('pluswish/<int:id>/',views.pluswish,name='pluswish'),

    path('minuswish/<int:id>/',views.minuswish,name='minuswish'),

    path('send_otp/', views.send_otp, name='send_otp'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('password-reset/',views.password_reset,name='password_reset'),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',views.pwcomplete,name='password_reset_complete'),

    # path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    # path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    # path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),

    
    # path('password_reset/', auth_views.PasswordResetView.as_view(form_class=MyPasswordResetForm), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



    

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)