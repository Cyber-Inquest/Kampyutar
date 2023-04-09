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

    total_choices = SubCategory.objects.all()
    print(total_choices)
    sub_categories_CHOICES = []
    for item in total_choices:
        sub_categories_CHOICES.append((item.id, item.title))
    

    total_brand = Brand.objects.all()
    print(total_brand)
    brand_choices = []
    for item in total_brand:
        brand_choices.append((item.id, item.title))
    print(brand_choices)
    sort_by = django_filters.ChoiceFilter(choices=CHOICES, method='filter_by_ordering',
                                          widget=forms.Select(attrs={'onchange': 'submit();'}))
    show_by = django_filters.ChoiceFilter(choices=SHOW_CHOICES, method='filter_by_show',
                                          widget=forms.Select(attrs={'onchange': 'submit();'}))
    slider = django_filters.RangeFilter(method='filter_by_slider')

    sub_categories = django_filters.ChoiceFilter(choices=sub_categories_CHOICES,
                                                 widget=forms.Select(),
                                                 empty_label=None)

    brand = django_filters.ChoiceFilter(choices=brand_choices,
                                        widget=forms.Select(),
                                        empty_label=None)
    print(brand)
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
