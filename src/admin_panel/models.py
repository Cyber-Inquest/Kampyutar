from ckeditor_uploader.fields import RichTextUploadingField

from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User,BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver



from django_mysql.models.fields import SizedTextField
from django.db import models
from datetime import datetime

# class MyAccountManager(BaseUserManager):
#      def create_superuser(self,email,password):
#         user = self.create_user(
#             email = self.normalize_email(email),
#             password = password,
#         )
#         user.fullname = "admin"
#         user.is_job_poster=True
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using = self._db)
#         return user


class Profile(models.Model):
    class Meta:
        db_table = 'Profile'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    contact = models.CharField(max_length=20, default='***')
    photo_img = models.ImageField(blank=True, null=True, upload_to='photos/admin_user', default='default')
    fullname = models.CharField(max_length=20, default='user')
    location = models.CharField(max_length=50, default='***', null=True)
    authorization = models.BooleanField(default=0)

    def __str__(self):
        return self.user.username

 
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    profile_instance = Profile.objects.filter(user=instance)
    if profile_instance:
        pass
    else:
        Profile.objects.create(user=instance,fullname=instance.username,authorization=0)
   


class Brands(models.Model):
    class Meta:
        db_table = 'Brands'

    title = models.CharField(max_length=200)
    date_uploaded = models.DateField(default=datetime.now)
    time_uploaded = models.TimeField(default=datetime.now)
    photo_img = models.ImageField(blank=True, null=True, upload_to='photos/Brands', default='default')
    discount = models.BigIntegerField(default=0)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    class Meta:
        db_table = 'SubCategory'

    title = models.CharField(max_length=200)
    date_uploaded = models.DateField(default=datetime.now)
    time_uploaded = models.TimeField(default=datetime.now)
    photo_img = models.ImageField(blank=True, null=True, upload_to='photos/SubCategory', default='default')
    categories = models.CharField(max_length=200)
    discount = models.BigIntegerField(default=0)

    def __str__(self):
        return self.title


class LatestProducts(models.Model):
    class Meta:
        db_table = 'LatestProducts'

    categories = models.CharField(max_length=200)
    sub_categories = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    stock = models.BigIntegerField(default=0)
    latest_price = models.FloatField(default=0.00)
    old_price = models.FloatField(default=0.00)
    coming_soon = models.BooleanField(default=0, help_text='0:none, 1:comingsoon')
    featured_product = models.BooleanField(default=0, help_text='0:non-featured, 1:featured')
    product_id = models.BigIntegerField(default=1)
    date_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title


class LaptopProducts(models.Model):
    class Meta:
        db_table = 'LaptopProducts'

    categories = models.CharField(max_length=200)
    sub_categories = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    stock = models.BigIntegerField(default=0)
    latest_price = models.FloatField(default=0.00)
    old_price = models.FloatField(default=0.00)
    coming_soon = models.BooleanField(default=0, help_text='0:none, 1:comingsoon')
    featured_product = models.BooleanField(default=0, help_text='0:non-featured, 1:featured')
    date_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title


class DesktopsProducts(models.Model):
    class Meta:
        db_table = 'DesktopsProducts'

    categories = models.CharField(max_length=200)
    sub_categories = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    stock = models.BigIntegerField(default=0)
    latest_price = models.FloatField(default=0.00)
    old_price = models.FloatField(default=0.00)
    coming_soon = models.BooleanField(default=0, help_text='0:none, 1:comingsoon')
    featured_product = models.BooleanField(default=0, help_text='0:non-featured, 1:featured')
    date_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title


class AppleProducts(models.Model):
    class Meta:
        db_table = 'AppleProducts'

    categories = models.CharField(max_length=200)
    sub_categories = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    stock = models.BigIntegerField(default=0)
    latest_price = models.FloatField(default=0.00)
    old_price = models.FloatField(default=0.00)
    coming_soon = models.BooleanField(default=0, help_text='0:none, 1:comingsoon')
    featured_product = models.BooleanField(default=0, help_text='0:non-featured, 1:featured')
    date_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title


class ComponentsProducts(models.Model):
    class Meta:
        db_table = 'ComponentsProducts'

    categories = models.CharField(max_length=200)
    sub_categories = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    stock = models.BigIntegerField(default=0)
    latest_price = models.FloatField(default=0.00)
    old_price = models.FloatField(default=0.00)
    coming_soon = models.BooleanField(default=0, help_text='0:none, 1:comingsoon')
    featured_product = models.BooleanField(default=0, help_text='0:non-featured, 1:featured')
    date_time = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title


class EleAccProducts(models.Model):
    class Meta:
        db_table = 'EleAccProducts'

    categories = models.CharField(max_length=200)
    sub_categories = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=5000)
    stock = models.BigIntegerField(default=0)
    latest_price = models.FloatField(default=0.00)
    old_price = models.FloatField(default=0.00)
    coming_soon = models.BooleanField(default=0, help_text='0:none, 1:comingsoon')
    featured_product = models.BooleanField(default=0, help_text='0:non-featured, 1:featured')

    def __str__(self):
        return self.title


class ProductSpecification(models.Model):
    class Meta:
        db_table = 'ProductSpecification'

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    products_type = models.CharField(max_length=200, default='***')
    product_id = models.BigIntegerField(default=0, null=False)

    def __str__(self):
        return self.title


class ProductsImage(models.Model):
    class Meta:
        db_table = 'ProductsImage'

    photo_img = models.ImageField(blank=True, null=True, upload_to='photos/Products', default='default')
    products_type = models.CharField(max_length=200, default='***')
    product_id = models.BigIntegerField(default=0, null=False)

    def __str__(self):
        return self.products_type


class Slideshow(models.Model):
    class Meta:
        db_table = 'Slideshow'

    link = models.CharField(max_length=200, default='default')
    photo_img = models.ImageField(blank=True, null=True, upload_to='photos/Slideshow', default='default')
    upload = models.BooleanField(default=0, help_text='0:not_uploaded,1:uploaded')


class Order(models.Model):
    class Meta:
        db_table = 'Order'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    products_type = models.CharField(max_length=200, default='***')
    product_id = models.BigIntegerField(default=0, null=False)
    quantity = models.IntegerField(default=1)
    date_time = models.DateTimeField(default=datetime.now())
    verified = models.BooleanField(default=False)
    delivering = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return self.products_type


class Billing(models.Model):
    class Meta:
        db_table = 'Billing'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="billing")
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


class Delivery(models.Model):
    class Meta:
        db_table = 'Delivery'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="delivery")
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


class Wishlist(models.Model):
    class Meta:
        db_table = 'Wishlist'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    products_type = models.CharField(max_length=200, default='***')
    product_id = models.BigIntegerField(default=0, null=False)

    def __str__(self):
        return self.products_type


class Cart(models.Model):
    class Meta:
        db_table = 'Cart'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    products_type = models.CharField(max_length=200, default='***')
    product_id = models.BigIntegerField(default=0, null=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.products_type


class ProductReview(models.Model):
    class Meta:
        db_table = 'ProductReview'

    rating = models.BigIntegerField(default=0, null=False)
    fullname = models.CharField(max_length=20, default='')
    user_email = models.CharField(max_length=50, default='')
    review = models.CharField(max_length=300, default='')
    categories = models.CharField(max_length=200, default='')
    product_id = models.BigIntegerField(default=0, null=False)

    def __str__(self):
        return self.fullname


class Blogs(models.Model):
    class Meta:
        db_table = 'Blogs'

    title = models.CharField(max_length=200)
    editor_name = models.CharField(max_length=50)
    location = models.CharField(max_length=20)
    photo_img = models.ImageField(blank=True, null=True, upload_to='photos/editor', default='default')
    blog_summary = SizedTextField(size_class=2, null=True)
    description = RichTextUploadingField(default=' ')
    date_uploaded = models.DateField(default=datetime.now)
    time_uploaded = models.TimeField(default=datetime.now)
    date_time_picker = models.DateTimeField(default=datetime.now)
    number_of_views = models.BigIntegerField(default=0)

    def __str__(self):
        return self.title

