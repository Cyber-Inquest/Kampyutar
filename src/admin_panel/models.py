from ckeditor_uploader.fields import RichTextUploadingField

from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.template.defaultfilters import slugify
from django.urls import reverse


from django_mysql.models.fields import SizedTextField
from django.db import models
from datetime import datetime


class Category(models.Model):
    class Meta:
        db_table = 'Category'
    title                   = models.CharField(max_length=200)
    slug                    = models.SlugField(max_length=200, unique=True,editable=False)
    image                   = models.ImageField(upload_to='photos/categories', blank=True)
    is_shown                = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
    class Meta:
        db_table = 'SubCategory'
    category                = models.ForeignKey(Category, on_delete=models.CASCADE)
    title                   = models.CharField(max_length=200)
    slug                    = models.SlugField(max_length=200, editable=False)
    image                   = models.ImageField(upload_to='photos/subcategories', blank=True)
    is_shown                = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def absolute_url(self):
        return reverse('subcategory_detail', kwargs={'slug': self.slug})

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(SubCategory, self).save(*args, **kwargs)


class Brand(models.Model):
    class Meta:
        db_table = 'Brand'
    title                   = models.CharField(max_length=200)
    slug                    = models.SlugField(max_length=200, unique=True,editable=False)
    image                   = models.ImageField(upload_to='photos/brand', blank=True)
    is_shown                = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def absolute_url(self):
        return reverse('brand_detail', kwargs={'slug': self.slug})
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Brand, self).save(*args, **kwargs)


class Product(models.Model):
    class Meta:
        db_table = 'Product'
    categories              = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_categories          = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brands                  = models.ForeignKey(Brand, on_delete=models.CASCADE)
    title                   = models.CharField(max_length=200)
    slug                    = models.SlugField(max_length=200, unique=True,editable=False)
    short_description       = models.CharField(max_length=200)
    description             = RichTextUploadingField()
    keywords                = models.CharField(max_length=500)
    model_number            = models.CharField(max_length=200)
    stock                   = models.IntegerField()
    latest_price            = models.FloatField()
    previous_price          = models.FloatField()
    is_featured             = models.BooleanField(default=False)
    is_comming_soon         = models.BooleanField(default=False)
    is_shown                = models.BooleanField(default=True)
    date_time               = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)


class Specification(models.Model):
    class Meta :
        db_table = 'specification'
    product                 = models.ForeignKey(Product, on_delete=models.CASCADE)
    title                   = models.CharField(max_length=200)
    description             = models.CharField(max_length=200)



class ProductImage(models.Model):
    class Meta:
        db_table = 'ProductImage'
    product                 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image                   = models.ImageField(upload_to='photos/product', blank=True)
    is_shown                = models.BooleanField(default=True)



class Profile(models.Model):
    class Meta:
        db_table = 'Profile'

    user                    = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    contact                 = models.CharField(max_length=20, default='***')
    photo_img               = models.ImageField(blank=True, null=True, upload_to='photos/admin_user', default='default')
    fullname                = models.CharField(max_length=20, default='user')
    location                = models.CharField(max_length=50, default='***', null=True)
    authorization           = models.BooleanField(default=0)

    def __str__(self):
        return self.user.username

class Address(models.Model):
    class Meta:
        db_table = 'Address'

    user                    = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_address")
    first_name              = models.CharField(max_length=20, default='')
    last_name               = models.CharField(max_length=20, default='')
    company_name            = models.CharField(max_length=50, default='')
    street_address          = models.CharField(max_length=50, default='')
    town_city               = models.CharField(max_length=50, default='')
    state                   = models.CharField(max_length=50, default='')
    zip                     = models.IntegerField(default='')
    contact                 = models.CharField(max_length=15, validators=[MinLengthValidator(7)], default='')

    def __str__(self):
        return self.user

 
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    profile_instance = Profile.objects.filter(user=instance)
    if profile_instance:
        pass
    else:
        Profile.objects.create(user=instance,fullname=instance.username,authorization=0)


class Order(models.Model):
    class Meta:
        db_table = 'Order'

    user                    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_user")
    product                 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_product")
    quantity                = models.IntegerField(default=1)
    batch                   = models.IntegerField(default=0)
    date_time               = models.DateTimeField(auto_now_add=True)
    verified                = models.BooleanField(default=False)
    delivering              = models.BooleanField(default=False)
    delivered               = models.BooleanField(default=False)

    def __str__(self):
        return str(self.batch)



class Billing(models.Model):
    class Meta:
        db_table = 'Billing'

    user                    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_billing")
    first_name              = models.CharField(max_length=20, default='')
    last_name               = models.CharField(max_length=20, default='')
    company_name            = models.CharField(max_length=50, default='')
    street_address          = models.CharField(max_length=50, default='')
    town_city               = models.CharField(max_length=50, default='')
    state                   = models.CharField(max_length=50, default='')
    zip                     = models.IntegerField(default='')
    contact                 = models.CharField(max_length=11, validators=[MinLengthValidator(7)], default='')
    batch                   = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class Delivery(models.Model):
    class Meta:
        db_table = 'Delivery'

    user                    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_delivery")
    first_name              = models.CharField(max_length=20, default='')
    last_name               = models.CharField(max_length=20, default='')
    company_name            = models.CharField(max_length=50, default='')
    street_address          = models.CharField(max_length=50, default='')
    town_city               = models.CharField(max_length=50, default='')
    state                   = models.CharField(max_length=50, default='')
    zip                     = models.IntegerField(default='')
    contact                 = models.CharField(max_length=11, validators=[MinLengthValidator(7)], default='')
    batch                   = models.IntegerField(default=0)


    def __str__(self):
        return self.user
    

class Wishlist(models.Model):
    class Meta:
        db_table = 'Wishlist'

    user                    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_wishlist")
    product                 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_product")
    date_time               = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product.title


class Cart(models.Model):
    class Meta:
        db_table = 'Cart'

    user                    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cart")
    product                 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_cart")
    datetime                = models.DateTimeField(auto_now_add=True)
    quantity                = models.IntegerField(default=1)

    def __str__(self):
        return self.product.title


class ProductReview(models.Model):
    class Meta:
        db_table = 'ProductReview'
    user                    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_review")
    product                 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_review")
    rating                  = models.BigIntegerField(default=0, null=False)
    fullname                = models.CharField(max_length=20, default='')
    review                  = models.CharField(max_length=300, default='')
    is_verified             = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'product')

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



class Slideshow(models.Model):
    class Meta:
        db_table = 'Slideshow'

    link = models.CharField(max_length=200, default='default')
    photo_img = models.ImageField(blank=True, null=True, upload_to='photos/Slideshow', default='default')
    upload = models.BooleanField(default=0, help_text='0:not_uploaded,1:uploaded')


