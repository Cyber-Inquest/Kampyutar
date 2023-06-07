from django.urls import path

from . import views

urlpatterns = [
    

     path('', views.index, name='index_admin'),
     path('admin-login/', views.admin_login, name='admin_login'),
     path('admin-product/',views.admin_product,name='admin_product'),
     path('admin-product-add/<int:id>',views.admin_product_add,name='admin_product_add'),
     path('admin-product-detail/<int:id>',views.admin_product_detail,name='admin_product_details'),
     path('admin-product-edit/<int:id>',views.admin_product_edit,name='admin_product_edit'),
     path('admin-sets/',views.admin_sets,name='admin_sets'),
     path('admin-sets-add-category/',views.admin_category_add,name='admin_category_add'),
     path('admin-sets-add-subcategory/<int:id>',views.admin_subcategory_add,name='admin_subcategory_add'),
     path('admin-sets-add-brand/',views.admin_brand_add,name='admin_brand_add'),
     path('admin-user-account/',views.admin_user_account,name='admin_user_account'),
     path('admin-staff-add/',views.admin_staff_add,name='admin_staff_add'),
     path('admin-staff-edit/<int:id>',views.admin_staff_edit,name='admin_staff_edit'),
     path('admin-category-edit/<int:id>',views.admin_category_edit,name='admin_category_edit'),
     path('admin-subcategory-edit/<int:id>',views.admin_subcategory_edit,name='admin_subcategory_edit'),
     path('admin-brand-edit/<int:id>',views.admin_brand_edit,name='admin_brand_edit'),
     path('logged_out/', views.logged_out, name='logged_out_admin'),
     


]
