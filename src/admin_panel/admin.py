from django.contrib import admin
from .models import Brand, SubCategory,Product, Profile, Order, Billing, Delivery, Wishlist, Cart, Specification,Slideshow,Category,ProductImage,ProductReview,Blogs

# Register your models here.
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(Billing)
admin.site.register(Delivery)
admin.site.register(ProductReview)
admin.site.register(Blogs)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Slideshow)
admin.site.register(Specification)


