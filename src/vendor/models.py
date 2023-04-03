from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models

from vendor_admin_panel.models import VendorBrands, VendorSubCategory
# Create your models here.


class VendorLatestProducts(models.Model):
    class Meta:
        db_table = 'VendorLatestProducts'

    categories = models.CharField(max_length=200)
    sub_categories = models.ForeignKey(VendorSubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(VendorBrands, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    stock = models.BigIntegerField(default=0)
    latest_price = models.FloatField(default=0.00)
    old_price = models.FloatField(default=0.00)
    condition = models.BooleanField(default=0, help_text='0:New, 1:Refurbished')
    price_drop = models.BooleanField(default=0, help_text='0:no price drop, 1:price drop')
    just_launched = models.BooleanField(default=0, help_text='0:just launched, 1:previous products')
    product_id = models.BigIntegerField(default=1)

    def __str__(self):
        return self.title


class VendorLaptopProducts(models.Model):
    class Meta:
        db_table = 'VendorLaptopProducts'

    categories = models.CharField(max_length=200)
    sub_categories = models.ForeignKey(VendorSubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(VendorBrands, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    stock = models.BigIntegerField(default=0)
    latest_price = models.FloatField(default=0.00)
    old_price = models.FloatField(default=0.00)
    condition = models.BooleanField(default=0, help_text='0:New, 1:Refurbished')
    price_drop = models.BooleanField(default=0, help_text='0:no price drop, 1:price drop')
    just_launched = models.BooleanField(default=0, help_text='0:just launched, 1:previous products')
    date_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title


class VendorDesktopsProducts(models.Model):
    class Meta:
        db_table = 'VendorDesktopsProducts'

    categories = models.CharField(max_length=200)
    sub_categories = models.ForeignKey(VendorSubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(VendorBrands, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    stock = models.BigIntegerField(default=0)
    latest_price = models.FloatField(default=0.00)
    old_price = models.FloatField(default=0.00)
    condition = models.BooleanField(default=0, help_text='0:New, 1:Refurbished')
    price_drop = models.BooleanField(default=0, help_text='0:no price drop, 1:price drop')
    just_launched = models.BooleanField(default=0, help_text='0:just launched, 1:previous products')
    date_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title


class VendorAppleProducts(models.Model):
    class Meta:
        db_table = 'VendorAppleProducts'

    categories = models.CharField(max_length=200)
    sub_categories = models.ForeignKey(VendorSubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(VendorBrands, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    stock = models.BigIntegerField(default=0)
    latest_price = models.FloatField(default=0.00)
    old_price = models.FloatField(default=0.00)
    condition = models.BooleanField(default=0, help_text='0:New, 1:Refurbished')
    price_drop = models.BooleanField(default=0, help_text='0:no price drop, 1:price drop')
    just_launched = models.BooleanField(default=0, help_text='0:just launched, 1:previous products')
    date_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title


class VendorComponentsProducts(models.Model):
    class Meta:
        db_table = 'VendorComponentsProducts'

    categories = models.CharField(max_length=200)
    sub_categories = models.ForeignKey(VendorSubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(VendorBrands, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    stock = models.BigIntegerField(default=0)
    latest_price = models.FloatField(default=0.00)
    old_price = models.FloatField(default=0.00)
    condition = models.BooleanField(default=0, help_text='0:New, 1:Refurbished')
    price_drop = models.BooleanField(default=0, help_text='0:no price drop, 1:price drop')
    just_launched = models.BooleanField(default=0, help_text='0:just launched, 1:previous products')
    date_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title


class VendorProductSpecification(models.Model):
    class Meta:
        db_table = 'VendorProductSpecification'

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    products_type = models.CharField(max_length=200, default='***')
    product_id = models.BigIntegerField(default=0, null=False)

    def __str__(self):
        return self.title


class VendorProductsImage(models.Model):
    class Meta:
        db_table = 'VendorProductsImage'

    photo_img = models.ImageField(blank=True, null=True, upload_to='photos/VendorProducts', default='default')
    products_type = models.CharField(max_length=200, default='***')
    product_id = models.BigIntegerField(default=0, null=False)

    def __str__(self):
        return self.products_type


class VendorCart(models.Model):
    class Meta:
        db_table = 'VendorCart'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vendorcart")
    products_type = models.CharField(max_length=200, default='***')
    product_id = models.BigIntegerField(default=0, null=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.products_type


class VendorSold(models.Model):
    class Meta:
        db_table = 'VendorSold'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="VendorSold")
    products_type = models.CharField(max_length=200, default='***')
    product_id = models.BigIntegerField(default=0, null=False)
    quantity = models.IntegerField(default=1)
    date_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.products_type


class VendorOrder(models.Model):
    class Meta:
        db_table = 'VendorOrder'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="VendorOrder")
    products_type = models.CharField(max_length=200, default='***')
    product_id = models.BigIntegerField(default=0, null=False)
    quantity = models.IntegerField(default=1)
    date_time = models.DateTimeField(default=datetime.now())
    verified = models.BooleanField(default=False)
    delivering = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.products_type


class VendorBilling(models.Model):
    class Meta:
        db_table = 'VendorBilling'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor_billing")
    first_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=20, default='')
    company_name = models.CharField(max_length=50, default='')
    street_address = models.CharField(max_length=50, default='')
    town_city = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50, default='')
    zip = models.IntegerField(default='')
    contact = models.CharField(max_length=11, validators=[MinLengthValidator(7)], default='')

    def __str__(self):
        return self.user


class VendorDelivery(models.Model):
    class Meta:
        db_table = 'VendorDelivery'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor_delivery")
    first_name = models.CharField(max_length=20, default='')
    last_name = models.CharField(max_length=20, default='')
    company_name = models.CharField(max_length=50, default='')
    street_address = models.CharField(max_length=50, default='')
    town_city = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50, default='')
    zip = models.IntegerField(default='')
    contact = models.CharField(max_length=11, validators=[MinLengthValidator(7)], default='')

    def __str__(self):
        return self.user

