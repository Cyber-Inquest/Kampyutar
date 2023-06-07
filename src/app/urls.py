from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
     path('', views.index, name='index_app'),
     path ('product-list/<slug:slug>', views.product_list, name='product_list'),
     path('<slug:slug>/<int:id>', views.product_detail, name='product_detail'),
     path('search-product/', views.search_product, name='search_product'),


     path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
     path('updateCart/', views.update_cart, name='updateCart'),
     path('add_wishlist/', views.add_wishlist, name='add_wishlist'),
     path('order_proceed/',views.order_proceed, name='order_proceed'),
     path('product-review', views.product_review, name='product_review'),
     #need to cover
     path('cancel-orderlist/', views.cancel_orderlist, name='cancel_orderlist'),
     path('delete-cart/', views.delete_cart, name='delete_cart'),
     path('delete-wishlist/', views.delete_wishlist, name='delete_wishlist'),
     

     path('client-profile/', views.client_profile, name='client_profile'),
     path('client_sign_in/', views.client_sign_in,
          name='client_sign_in'),
     path('client_sign_up/', views.client_sign_up,
          name='client_sign_up'),
     path('logged_out/', views.logged_out, name='logged_out_app'),



     path('reset_password/',
          auth_views.PasswordResetView.as_view(template_name="client_page/userAccount/forgetPassword.html"),
          name="reset_password"),
     path('reset_password_sent/',
          auth_views.PasswordResetDoneView.as_view(template_name='client_page/userAccount/password_reset_done.html'),
          name="password_reset_done"),
     path('reset/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(template_name='client_page/userAccount/new_pass.html'),
          name="password_reset_confirm"),
     path('reset_password_complete/',
          auth_views.PasswordResetCompleteView.as_view(
               template_name='client_page/userAccount/password_recent_sent.html'),
          name="password_reset_complete"),


]
