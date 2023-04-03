from datetime import datetime

from django.db import models

# Create your models here.


class VendorBrands(models.Model):
    class Meta:
        db_table = 'VendorBrands'

    title = models.CharField(max_length=200)
    date_uploaded = models.DateField(default=datetime.now)
    time_uploaded = models.TimeField(default=datetime.now)
    photo_img = models.ImageField(blank=True, null=True, upload_to='photos/VendorBrands', default='default')
    discount = models.BigIntegerField(default=0)

    def __str__(self):
        return self.title


class VendorSubCategory(models.Model):
    class Meta:
        db_table = 'VendorSubCategory'

    title = models.CharField(max_length=200)
    date_uploaded = models.DateField(default=datetime.now)
    time_uploaded = models.TimeField(default=datetime.now)
    photo_img = models.ImageField(blank=True, null=True, upload_to='photos/VendorSubCategory', default='default')
    categories = models.CharField(max_length=200)
    discount = models.BigIntegerField(default=0)

    def __str__(self):
        return self.title

