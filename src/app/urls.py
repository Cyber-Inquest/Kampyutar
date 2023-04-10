from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
     path('', views.index, name='index_app'),
     path('pc-builder', views.coming_soonPC, name='comingSoon_app'),

     path('blog_page/', views.blog_page, name='blog_page_app'),
     path('per_blog_page/<int:ids>', views.per_blog_page, name='per_blog_page_app'),
     path('blog_search', views.blog_search, name='blog_search_app'),

     #old created app 
     # path('list_page/<str:_product>', views.list_page, name='list_page_app'),
     # path('per_page/<str:_product>/<int:ids>', views.per_page, name='per_page_app'),
     #replace by 
     path ('product-list/<slug:slug>', views.product_list, name='product_list'),
     path('per_page/<slug:slug>/<int:id>', views.product_detail, name='product_detail'),
     path('update_wishlist/', views.update_wishlist, name='update_wishlist_app'),
     path('add_wishlist/', views.add_wishlist, name='add_wishlist_app'),



     path('updateCart/', views.update_cart, name='updateCart_app'),

     path('shopping_cart/', views.shopping_cart, name='shopping_cart_app'),

     path('update_orderlist/', views.update_orderlist, name='update_orderlist_app'),
     path('update_cartlist/', views.update_cartlist, name='update_cartlist_app'),

     path('logged_out/', views.logged_out, name='logged_out_app'),

     path('authenticate/', views.client_authentication, name='client_authentication_app'),
     path('client_authentication_sign_in/', views.client_authentication_sign_in,
          name='client_authentication_sign_in_app'),
     path('client_authentication_sign_up/', views.client_authentication_sign_up,
          name='client_authentication_sign_up_app'),

     path('checkout_order_save/', views.checkout_order_save,
          name='checkout_order_save_app'),
     path('client_information_billing_post/<int:ids>', views.client_information_billing_post,
          name='client_information_billing_post_app'),
     path('client_information_account_post/<int:ids>', views.client_information_account_post,
          name='client_information_account_post_app'),

     path('search_btns_post', views.search_btns_post, name='search_btns_post_app'),
     path('product_review/<str:_product>/<int:ids>', views.product_review, name='product_review_app'),

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
