from django.urls import path

from . import views

urlpatterns = [
    

     path('', views.index, name='index_admin'),
     path('admin-login/', views.admin_login, name='admin_login'),
     path('admin-product/',views.admin_product,name='admin_product'),
     path('admin-product-add/<int:id>',views.admin_product_add,name='admin_product_add'),




    #region old Code
    path('login/', views.admin_login, name='admin_login_admin'),
#     path('admin_login_post/', views.admin_login_post, name='admin_login_post_admin'),
#     path('dashboard/', views.index, name='index_admin'),

    path('product/', views.sb_product, name='sb_product_admin'),
    path('sb_product_add_product_post/', views.sb_product_add_product_post, name='sb_product_add_product_post_admin'),
    path('product/add_category', views.sb_add_category_product, name='sb_add_category_product_admin'),
    path('product/edit_product/<str:product_type>/<int:ids>', views.sb_edit_product, name='sb_edit_product_admin'),
    path('sb_edit_product_post/<str:product_type>/<int:ids>', views.sb_edit_product_post,
         name='sb_edit_product_post_admin'),

    path('product/add_subcategory/<str:_categories>', views.sb_add_subcategory_product,
         name='sb_add_subcategory_product_admin'),
    path('sb_add_subcategory_product_post/<str:_categories>', views.sb_add_subcategory_product_post,
         name='sb_add_subcategory_product_post_admin'),
    path('product/add_brand', views.sb_add_brand_product, name='sb_add_brand_product_admin'),
    path('sb_add_brand_product_post/', views.sb_add_brand_product_post, name='sb_add_brand_product_post_admin'),

    path('images/', views.sb_images, name='sb_images_admin'),
    path('images/add_images', views.sb_add_images, name='sb_add_images_admin'),
    path('sb_del_images', views.sb_del_images, name='sb_del_images_admin'),
    path('sb_add_images_post/', views.sb_add_images_post, name='sb_add_images_post_admin'),

    path('images/image_slideshow/', views.image_slideshow, name='image_slideshow_admin'),
    path('image_slideshow_deploy/', views.image_slideshow_deploy, name='image_slideshow_deploy_admin'),

    path('ads/', views.sb_ads, name='sb_ads_admin'),

    path('account/', views.sb_account, name='sb_account_admin'),
    path('account/view_admin_account/<int:ids>', views.sb_view_admin_account, name='sb_view_admin_account_admin'),
    path('sb_view_admin_account_post/<int:ids>', views.sb_view_admin_account_post,
         name='sb_view_admin_account_post_admin'),
    path('account/add_admin_account/', views.sb_add_admin_account, name='sb_add_admin_account_admin'),
    path('sb_add_admin_account_post/', views.sb_add_admin_account_post, name='sb_add_admin_account_post_admin'),
    path('sb_delete_admin_account_post/<int:ids>', views.sb_delete_admin_account_post,
         name='sb_delete_admin_account_post_admin'),

    path('blog/', views.sb_blog, name='sb_blog_admin'),
    path('sb_blog_post/', views.sb_blog_post, name='sb_blog_post_admin'),
    path('sb_blog_edit/<int:ids>', views.sb_blog_edit, name='sb_blog_edit_admin'),
    path('sb_blog_edit_post/<int:ids>', views.sb_blog_edit_post, name='sb_blog_edit_post_admin'),

    path('logged_out/', views.logged_out, name='logged_out_admin'),

    path('del_product/', views.del_product, name='del_product_admin'),
    path('product_selected/', views.product_selected, name='product_selected_admin'),
     #endregion
]
