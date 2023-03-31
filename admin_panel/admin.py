from django.contrib import admin
from .models import Brands, SubCategory, Slideshow, Profile, Order, Billing, Delivery, Wishlist, Cart, \
    ProductSpecification, LaptopProducts, DesktopsProducts, AppleProducts, ComponentsProducts, EleAccProducts, \
    ProductsImage, LatestProducts

# Register your models here.
admin.site.register(Brands)
admin.site.register(SubCategory)
admin.site.register(LaptopProducts)
admin.site.register(DesktopsProducts)
admin.site.register(AppleProducts)
admin.site.register(ComponentsProducts)
admin.site.register(EleAccProducts)
admin.site.register(ProductsImage)

admin.site.register(Slideshow)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(Billing)
admin.site.register(Delivery)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(ProductSpecification)
admin.site.register(LatestProducts)
