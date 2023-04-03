from vendor.models import VendorProductSpecification, VendorProductsImage, VendorLaptopProducts

from .models import VendorSubCategory

from django import forms
from django.forms import ModelForm


CATEGORIES_CHOICES = (
    ('Laptops', 'Laptop'),
    ('Desktops', 'Desktops'),
    ('Apple', 'Apple'),
    ('Components', 'Components'),
)


class AddVendorBrands(forms.Form):
    photo_img = forms.ImageField(label='Upload Image', required=False, initial='default')
    title = forms.CharField(label='TITLE', max_length=200,
                            widget=forms.TextInput(attrs={'placeholder': "Enter Name."}))
    discount = forms.IntegerField(label='Discount', initial=0)


class AddVendorProducts(forms.ModelForm):
    categories = forms.ChoiceField(choices=CATEGORIES_CHOICES)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 10, "cols": 79}))
    condition = forms.BooleanField(required=False)
    price_drop = forms.BooleanField(required=False)
    just_launched = forms.BooleanField(required=False)

    class Meta:
        model = VendorLaptopProducts
        exclude = ('categories', 'date_time')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_categories'].queryset = VendorSubCategory.objects.none()

        if 'categories' in self.data:

            try:
                categories_text = str(self.data.get('categories'))
                self.fields['sub_categories'].queryset = VendorSubCategory.objects.filter(categories=categories_text)
            except (ValueError, TypeError):
                pass
        elif self.instance:
            print(self.instance.categories)
            self.initial['categories'] = self.instance.categories
            self.fields['sub_categories'].queryset = VendorSubCategory.objects.filter(categories=self.instance.categories)


class AddVendorProductsImage(forms.ModelForm):
    class Meta:
        model = VendorProductsImage
        fields = ('photo_img',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['photo_img'].widget.attrs.update({'multiple': True})


class AddVendorProductsDescription(ModelForm):
    class Meta:
        model = VendorProductSpecification
        fields = ('title', 'description',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({'placeholder': "Enter Specification."})
        self.fields['description'].widget.attrs.update({'placeholder': "Enter Description."})