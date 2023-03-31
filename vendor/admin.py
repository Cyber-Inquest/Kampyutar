from django.contrib import admin
from .models import VendorLatestProducts, VendorLaptopProducts, VendorDesktopsProducts, VendorAppleProducts, \
    VendorComponentsProducts, VendorProductSpecification, VendorProductsImage

# Register your models here.

admin.site.register(VendorLatestProducts)
admin.site.register(VendorLaptopProducts)
admin.site.register(VendorDesktopsProducts)
admin.site.register(VendorAppleProducts)
admin.site.register(VendorComponentsProducts)
admin.site.register(VendorProductSpecification)
admin.site.register(VendorProductsImage)
