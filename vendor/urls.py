from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_login, name='vendor_login_vendor'),
    path('vendor_authentication_sign_in_post/', views.vendor_authentication_sign_in_post,
         name='vendor_authentication_sign_in_post_vendor'),

    path('dashboard/', views.vendor_page, name='vendor_page_vendor'),
    path('update_cart/', views.update_cart, name='update_cart_vendor'),
    path('checkout/', views.checkout_page, name='checkout_page_vendor'),

    path('price_drop/', views.price_drop_page, name='price_drop_page_vendor'),
    path('just_launch/', views.just_launch_page, name='just_launch_page_vendor'),
    path('just_sold/', views.just_sold_page, name='just_sold_page_vendor'),

    path('vendor_ajax_today_deals/', views.vendor_ajax_today_deals, name='vendor_ajax_today_deals_vendor'),
    path('vendor_ajax_price_drop/', views.vendor_ajax_price_drop, name='vendor_ajax_price_drop_vendor'),
    path('vendor_ajax_just_launched/', views.vendor_ajax_just_launched, name='vendor_ajax_just_launched_vendor'),

    path('vendor_profile/', views.vendor_authentication, name='vendor_authentication_vendor'),
    path('checkout_order_save/', views.checkout_order_save, name='checkout_order_save_vendor'),
    path('vendor_address_post/<int:ids>', views.vendor_address_post, name='vendor_address_post_vendor'),
    path('vendor_information_account_post/<int:ids>', views.vendor_information_account_post,
         name='vendor_information_account_post_vendor'),
    path('update_order/', views.update_order, name='update_order_vendor'),
]
