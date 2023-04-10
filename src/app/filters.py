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
   
        # Create the filter fields
        self.filters['sort_by'] = django_filters.ChoiceFilter(choices=self.CHOICES, method='filter_by_ordering',
                                            widget=forms.Select(attrs={'onchange': 'submit();'}))
        self.filters['show_by'] = django_filters.ChoiceFilter(choices=self.SHOW_CHOICES, method='filter_by_show',
                                            widget=forms.Select(attrs={'onchange': 'submit();'}))
        self.filters['slider'] = django_filters.RangeFilter(method='filter_by_slider')
        
        self.filters['sub_categories'] = django_filters.ChoiceFilter(choices=sub_categories_CHOICES,
                                                    widget=forms.Select(),
                                                    empty_label=None)
        self.filters['brand'] = django_filters.ChoiceFilter(choices=brand_choices,
                                        widget=forms.Select(),
                                        empty_label=None)

    def filter_by_ordering(self, queryset, name, value):
        if value == 'descending':
            return queryset.order_by('-latest_price')
        elif value == 'ascending':
            return queryset.order_by('latest_price')

    def filter_by_slider(self, queryset, name, value):
        print('----------------------------------')
        if value:
            return queryset.filter(latest_price__gte=value.start, latest_price__lte=value.stop)

    def filter_by_show(self, queryset, name, value):
        if value == '12':
            return queryset
        elif value == '24':
            return queryset
        elif value == '36':
            return queryset

# class SnippetFilterLaptop(django_filters.FilterSet):
#     CHOICES = (
#         ('descending', 'Price High to Low'),
#         ('ascending', 'Price Low to High'),
#     )

#     SHOW_CHOICES = (
#         (12, '12'),
#         (24, '24'),
#         (36, '36'),
#     )
    
#     total_choices = SubCategory.objects.filter(categories='Laptops').all()
#     sub_categories_CHOICES = []
#     for item in total_choices:
#         sub_categories_CHOICES.append((item.id, item.title))

#     total_brand = Brand.objects.all()
#     brand_choices = []
#     for item in total_brand:
#         brand_choices.append((item.id, item.title))

#     sort_by = django_filters.ChoiceFilter(choices=CHOICES, method='filter_by_ordering',
#                                           widget=forms.Select(attrs={'onchange': 'submit();'}))
#     show_by = django_filters.ChoiceFilter(choices=SHOW_CHOICES, method='filter_by_show',
#                                           widget=forms.Select(attrs={'onchange': 'submit();'}))
#     slider = django_filters.RangeFilter(method='filter_by_slider')

#     sub_categories = django_filters.ChoiceFilter(choices=sub_categories_CHOICES,
#                                                  widget=forms.Select(),
#                                                  empty_label=None)

#     brand = django_filters.ChoiceFilter(choices=brand_choices,
#                                         widget=forms.Select(),
#                                         empty_label=None)

#     def filter_by_ordering(self, queryset, name, value):
#         if value == 'descending':
#             return queryset.order_by('-latest_price')
#         elif value == 'ascending':
#             return queryset.order_by('latest_price')

#     def filter_by_slider(self, queryset, name, value):
#         if value:
#             return queryset.filter(latest_price__gte=value.start, latest_price__lte=value.stop)

#     def filter_by_show(self, queryset, name, value):
#         if value == '12':
#             return queryset
#         elif value == '24':
#             return queryset
#         elif value == '36':
#             return queryset


# class SnippetFilterDesktop(django_filters.FilterSet):
#     CHOICES = (
#         ('descending', 'Price High to Low'),
#         ('ascending', 'Price Low to High'),
#     )

#     SHOW_CHOICES = (
#         (12, '12'),
#         (24, '24'),
#         (36, '36'),
#     )

#     total_choices = SubCategory.objects.filter(categories='Desktops').all()
#     sub_categories_CHOICES = []
#     for item in total_choices:
#         sub_categories_CHOICES.append((item.id, item.title))

#     total_brand = Brand.objects.all()
#     brand_choices = []
#     for item in total_brand:
#         brand_choices.append((item.id, item.title))

#     sort_by = django_filters.ChoiceFilter(choices=CHOICES, method='filter_by_ordering',
#                                           widget=forms.Select(attrs={'onchange': 'submit();'}))
#     show_by = django_filters.ChoiceFilter(choices=SHOW_CHOICES, method='filter_by_show',
#                                           widget=forms.Select(attrs={'onchange': 'submit();'}))
#     slider = django_filters.RangeFilter(method='filter_by_slider')

#     sub_categories = django_filters.ChoiceFilter(choices=sub_categories_CHOICES,
#                                                  widget=forms.Select(),
#                                                  empty_label=None)

#     brand = django_filters.ChoiceFilter(choices=brand_choices,
#                                         widget=forms.Select(),
#                                         empty_label=None)

#     def filter_by_ordering(self, queryset, name, value):
#         if value == 'descending':
#             return queryset.order_by('-latest_price')
#         elif value == 'ascending':
#             return queryset.order_by('latest_price')

#     def filter_by_slider(self, queryset, name, value):
#         if value:
#             return queryset.filter(latest_price__gte=value.start, latest_price__lte=value.stop)

#     def filter_by_show(self, queryset, name, value):
#         if value == '12':
#             return queryset
#         elif value == '24':
#             return queryset
#         elif value == '36':
#             return queryset


# class SnippetFilterApple(django_filters.FilterSet):
#     CHOICES = (
#         ('descending', 'Price High to Low'),
#         ('ascending', 'Price Low to High'),
#     )

#     SHOW_CHOICES = (
#         (12, '12'),
#         (24, '24'),
#         (36, '36'),
#     )

#     total_choices = SubCategory.objects.filter(categories='Apple').all()
#     sub_categories_CHOICES = []
#     for item in total_choices:
#         sub_categories_CHOICES.append((item.id, item.title))

#     total_brand = Brand.objects.all()
#     brand_choices = []
#     for item in total_brand:
#         brand_choices.append((item.id, item.title))

#     sort_by = django_filters.ChoiceFilter(choices=CHOICES, method='filter_by_ordering',
#                                           widget=forms.Select(attrs={'onchange': 'submit();'}))
#     show_by = django_filters.ChoiceFilter(choices=SHOW_CHOICES, method='filter_by_show',
#                                           widget=forms.Select(attrs={'onchange': 'submit();'}))
#     slider = django_filters.RangeFilter(method='filter_by_slider')

#     sub_categories = django_filters.ChoiceFilter(choices=sub_categories_CHOICES,
#                                                  widget=forms.Select(),
#                                                  empty_label=None)

#     brand = django_filters.ChoiceFilter(choices=brand_choices,
#                                         widget=forms.Select(),
#                                         empty_label=None)

#     def filter_by_ordering(self, queryset, name, value):
#         if value == 'descending':
#             return queryset.order_by('-latest_price')
#         elif value == 'ascending':
#             return queryset.order_by('latest_price')

#     def filter_by_slider(self, queryset, name, value):
#         if value:
#             return queryset.filter(latest_price__gte=value.start, latest_price__lte=value.stop)

#     def filter_by_show(self, queryset, name, value):
#         if value == '12':
#             return queryset
#         elif value == '24':
#             return queryset
#         elif value == '36':
#             return queryset


# class SnippetFilterComponents(django_filters.FilterSet):
#     CHOICES = (
#         ('descending', 'Price High to Low'),
#         ('ascending', 'Price Low to High'),
#     )

#     SHOW_CHOICES = (
#         (12, '12'),
#         (24, '24'),
#         (36, '36'),
#     )

#     total_choices = SubCategory.objects.filter(categories='Components').all()
#     sub_categories_CHOICES = []
#     for item in total_choices:
#         sub_categories_CHOICES.append((item.id, item.title))

#     total_brand = Brand.objects.all()
#     brand_choices = []
#     for item in total_brand:
#         brand_choices.append((item.id, item.title))

#     sort_by = django_filters.ChoiceFilter(choices=CHOICES, method='filter_by_ordering',
#                                           widget=forms.Select(attrs={'onchange': 'submit();'}))
#     show_by = django_filters.ChoiceFilter(choices=SHOW_CHOICES, method='filter_by_show',
#                                           widget=forms.Select(attrs={'onchange': 'submit();'}))
#     slider = django_filters.RangeFilter(method='filter_by_slider')

#     sub_categories = django_filters.ChoiceFilter(choices=sub_categories_CHOICES,
#                                                  widget=forms.Select(),
#                                                  empty_label=None)

#     brand = django_filters.ChoiceFilter(choices=brand_choices,
#                                         widget=forms.Select(),
#                                         empty_label=None)

#     def filter_by_ordering(self, queryset, name, value):
#         if value == 'descending':
#             return queryset.order_by('-latest_price')
#         elif value == 'ascending':
#             return queryset.order_by('latest_price')

#     def filter_by_slider(self, queryset, name, value):
#         if value:
#             return queryset.filter(latest_price__gte=value.start, latest_price__lte=value.stop)

#     def filter_by_show(self, queryset, name, value):
#         if value == '12':
#             return queryset
#         elif value == '24':
#             return queryset
#         elif value == '36':
#             return queryset


# class SnippetFilterVendor(django_filters.FilterSet):

#     total_brand = Brand.objects.all()
#     brand_choices = []
#     for item in total_brand:
#         brand_choices.append((item.id, item.title))

#     brand = django_filters.ChoiceFilter(choices=brand_choices,
#                                         widget=forms.Select(),
#                                         empty_label=None)

#     class Meta:
#         model = Product
#         fields = ('categories',)
