import json
import django_filters
from admin_panel.models import Product, Brand, SubCategory
from django import forms



class SnippetFilterProductList(django_filters.FilterSet):
    CHOICES = (
        ('descending', 'Price High to Low'),
        ('ascending', 'Price Low to High'),
    )
    SHOW_CHOICES = (
        (12, '12'),
        (24, '24'),
        (36, '36'),
    )
   
    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category', None)  # Retrieve the category from the kwargs
        self.total_choices = []
        super().__init__(*args, **kwargs)
        
        # Retrieve the subcategories and brand choices filtered by the category
        if self.category:
            self.total_choices = SubCategory.objects.filter(category=self.category).all()
            sub_categories_CHOICES = [(item.id, item.title) for item in self.total_choices]
            total_brand = Brand.objects.filter(product__categories=self.category).distinct()
            brand_choices = [(item.id, item.title) for item in total_brand]
        else:
            sub_categories_CHOICES = []
            brand_choices = []
        self.filters['brands'].extra['choices'] = brand_choices
        self.filters['sub_categories'].extra['choices'] = sub_categories_CHOICES
        # Create the filter fields
    sort_by = django_filters.ChoiceFilter(choices=CHOICES, method='filter_by_ordering',
                                            widget=forms.Select(attrs={'onchange': 'submit();'}))
    show_by = django_filters.ChoiceFilter(choices=SHOW_CHOICES, method='filter_by_show',
                                        widget=forms.Select(attrs={'onchange': 'submit();'}))
    slider = django_filters.RangeFilter(method='filter_by_slider')
    brands = django_filters.ChoiceFilter(choices=[],
                                        widget=forms.Select(),
                                        empty_label=("All Brands"))

    sub_categories = django_filters.ChoiceFilter(choices=[],
                                                widget=forms.Select(),
                                                empty_label=("All Subcategories"))

    def filter_by_ordering(self, queryset, name, value):
        if value == 'descending':
            return queryset.order_by('-latest_price')
        elif value == 'ascending':
            return queryset.order_by('latest_price')

    def filter_by_slider(self, queryset, name, value):
        if value:
            return queryset.filter(latest_price__gte=value.start, latest_price__lte=value.stop)

    def filter_by_show(self, queryset, name, value):
        if value == '12':
            return queryset
        elif value == '24':
            return queryset
        elif value == '36':
            return queryset
