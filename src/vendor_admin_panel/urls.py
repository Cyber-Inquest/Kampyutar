from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index_vendor_admin_page'),

    path('product/', views.sb_product, name='sb_product_vendor_admin_page'),

    path('product/add_brand', views.sb_add_brand_product, name='sb_add_brand_product_vendor_admin_page'),
    path('sb_add_brand_product_post', views.sb_add_brand_product_post,
         name='sb_add_brand_product_post_vendor_admin_page'),

    path('product/add_subcategory/<str:_categories>', views.sb_add_subcategory_product,
         name='sb_add_subcategory_product_vendor_admin_page'),
    path('sb_add_subcategory_product_post/<str:_categories>', views.sb_add_subcategory_product_post,
         name='sb_add_subcategory_product_post_vendor_admin_page'),

    path('product_selected/', views.product_selected,

         name='product_selected_vendor_admin_page'),
    path('sb_product_add_product_post/', views.sb_product_add_product_post,
         name='sb_product_add_product_post_vendor_admin_page'),
    path('product/edit_product/<str:product_type>/<int:ids>', views.sb_edit_product,
         name='sb_edit_product_vendor_admin_page'),
    path('sb_edit_product_post/<str:product_type>/<int:ids>', views.sb_edit_product_post,
         name='sb_edit_product_post_vendor_admin_page'),

    path('order/', views.sb_order, name='sb_order_vendor_admin_page'),

    path('order/per_vendor_account/<int:ids>', views.sb_per_vendor_account,
         name='sb_per_vendor_account_vendor_admin_page'),

    path('vendor_account/', views.sb_vendor_account, name='sb_vendor_account_vendor_admin_page'),
    path('vendor_account/view_vendor_account/<int:ids>', views.sb_view_vendor_account,
         name='sb_view_vendor_account_vendor_admin_page'),
    path('sb_view_vendor_account_post/<int:ids>', views.sb_view_vendor_account_post,
         name='sb_view_vendor_account_post_vendor_admin_page'),
    path('sb_delete_vendor_account_post/<int:ids>', views.sb_delete_vendor_account_post,
         name='sb_delete_vendor_account_post_vendor_admin_page'),
    path('vendor_account/add_admin_account/', views.sb_add_vendor_account,
         name='sb_add_vendor_account_vendor_admin_page'),
    path('sb_add_vendor_account_post/', views.sb_add_vendor_account_post,
         name='sb_add_vendor_account_post_vendor_admin_page'),

    path('order_status/', views.order_status,
         name='order_status_vendor_admin_page'),
    path('del_order/', views.del_order,
         name='del_order_vendor_admin_page'),
]
