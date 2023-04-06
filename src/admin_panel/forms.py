from datetime import datetime

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import ProductSpecification, ProductsImage, LaptopProducts, SubCategory, Blogs

CATEGORIES_CHOICES = (
    ('', 'Select Category'),
    ('Laptops', 'Laptop'),
    ('Desktops', 'Desktops'),
    ('Apple', 'Apple'),
    ('Components', 'Components'),
)

total_choices = SubCategory.objects.filter(categories='Desktops').all()
sub_categories_CHOICES = []
for item in total_choices:
    sub_categories_CHOICES.append((item.id, item.title))


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)


class AddBrands(forms.Form):
    photo_img = forms.ImageField(label='Upload Image', required=False, initial='default')
    title = forms.CharField(label='TITLE', max_length=200,
                            widget=forms.TextInput(attrs={'placeholder': "Enter Name."}))
    discount = forms.IntegerField(label='Discount', initial=0)


class AddSlideshow(forms.Form):
    link = forms.CharField(label='link', max_length=200,
                           widget=forms.TextInput(attrs={'placeholder': "Enter Link."}))
    photo_img = forms.ImageField(label='Upload Image', required=False, initial='default')


class AddProducts(forms.ModelForm):
    categories = forms.ChoiceField(choices=CATEGORIES_CHOICES)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 10, "cols": 79}))
    featured_product = forms.BooleanField(required=False)
    coming_soon = forms.BooleanField(required=False)

    class Meta:
        model = LaptopProducts
        exclude = ('categories', 'date_time')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_categories'].queryset = SubCategory.objects.none()

        if 'categories' in self.data:

            try:
                categories_text = str(self.data.get('categories'))
                self.fields['sub_categories'].queryset = SubCategory.objects.filter(categories=categories_text)
            except (ValueError, TypeError):
                pass
        elif self.instance:
            print(self.instance.categories)
            self.initial['categories'] = self.instance.categories
            self.fields['sub_categories'].queryset = SubCategory.objects.filter(categories=self.instance.categories)


class AddProductsImage(forms.ModelForm):
    class Meta:
        model = ProductsImage
        fields = ('photo_img',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['photo_img'].widget.attrs.update({'multiple': True})


class AddProductsDescription(ModelForm):
    class Meta:
        model = ProductSpecification
        fields = ('title', 'description',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({'placeholder': "Enter Specification."})
        self.fields['description'].widget.attrs.update({'placeholder': "Enter Description."})


class AddBlog(forms.ModelForm):
    title = forms.CharField(label='TITLE', max_length=200,
                            widget=forms.TextInput(attrs={'placeholder': "Your Title..."}))
    editor_name = forms.CharField(label='AUTHOR NAME', max_length=50,
                                  widget=forms.TextInput(attrs={'placeholder': "Author Name..."}))
    location = forms.CharField(label='AUTHOR LOCATION', max_length=20,
                               widget=forms.TextInput(attrs={'placeholder': "Author Location..."}))
    photo_img = forms.ImageField(label='SELECT IMAGE', required=False, initial='default')
    description = forms.CharField(widget=CKEditorUploadingWidget(), required=False, initial=' ')

    class Meta:
        model = Blogs
        fields = ('blog_summary',)


class EditBlog(forms.ModelForm):

    description = forms.CharField(widget=CKEditorUploadingWidget(), required=False, initial=' ')

    class Meta:
        model = Blogs
        exclude = ['number_of_views', 'date_time_picker', 'date_uploaded', 'time_uploaded', ]
