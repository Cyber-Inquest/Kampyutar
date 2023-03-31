import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.forms import modelformset_factory

from .models import VendorBrands, VendorSubCategory

from admin_panel.decorators import admin_only
from vendor.models import VendorLaptopProducts, VendorDesktopsProducts, VendorAppleProducts, VendorComponentsProducts, \
    VendorProductsImage, VendorProductSpecification, VendorLatestProducts, VendorOrder
from vendor_admin_panel.forms import AddVendorProducts, AddVendorProductsImage, AddVendorProductsDescription, \
    AddVendorBrands
from admin_panel.models import Profile


def distinct_image(image_object, product_type):
    list_product_id = []
    per_product_image = []
    for item in image_object:
        list_product_id.append(item.product_id)

    if product_type == 'Laptops':
        for items in set(list_product_id):
            per_product_image.append(
                VendorProductsImage.objects.filter(product_id=items, products_type=product_type).last())

    elif product_type == 'Desktops':
        for items in set(list_product_id):
            per_product_image.append(
                VendorProductsImage.objects.filter(product_id=items, products_type=product_type).last())

    elif product_type == 'Apple':
        for items in set(list_product_id):
            per_product_image.append(
                VendorProductsImage.objects.filter(product_id=items, products_type=product_type).last())

    elif product_type == 'Components':
        for items in set(list_product_id):
            per_product_image.append(
                VendorProductsImage.objects.filter(product_id=items, products_type=product_type).last())

    return per_product_image


@admin_only
@login_required(login_url='admin_login_admin')
def index(request):
    return render(request, 'vendor_admin_page/index.html')


@admin_only
@login_required(login_url='admin_login_admin')
def sb_product(request):
    brands_list = VendorBrands.objects.all()
    sub_category_list = VendorSubCategory.objects.all()

    sub_category_laptop = VendorSubCategory.objects.filter(categories='Laptops').order_by('categories')
    sub_category_desktop = VendorSubCategory.objects.filter(categories='Desktops').order_by('categories')
    sub_category_apple = VendorSubCategory.objects.filter(categories='Apple').order_by('categories')
    sub_category_components = VendorSubCategory.objects.filter(categories='Components').order_by('categories')

    laptop_list = VendorLaptopProducts.objects.all()
    product_images_laptop = VendorProductsImage.objects.filter(products_type='Laptops').order_by(
        'product_id').distinct()
    laptop_image = distinct_image(product_images_laptop, 'Laptops')

    desktop_list = VendorDesktopsProducts.objects.all()
    product_images_desktop = VendorProductsImage.objects.filter(products_type='Desktops').order_by(
        'product_id').distinct()
    desktop_image = distinct_image(product_images_desktop, 'Desktops')

    apple_list = VendorAppleProducts.objects.all()
    product_images_apple = VendorProductsImage.objects.filter(products_type='Apple').order_by('product_id').distinct()
    apple_image = distinct_image(product_images_apple, 'Apple')

    components_list = VendorComponentsProducts.objects.all()
    product_images_components = VendorProductsImage.objects.filter(products_type='Components').order_by(
        'product_id').distinct()
    components_image = distinct_image(product_images_components, 'Components')

    product_specification_list = VendorProductSpecification.objects.all()
    product_image_form = AddVendorProductsImage()
    category_list = ['Laptops', 'Desktops', 'Apple', 'Components']

    form_1 = AddVendorProducts()

    productdescriptionformset = modelformset_factory(VendorProductSpecification, form=AddVendorProductsDescription,
                                                     extra=0)
    formset = productdescriptionformset(queryset=VendorProductSpecification.objects.none())

    context = {'brands_list': brands_list, 'sub_category_laptop': sub_category_laptop,
               'product_specification_list': product_specification_list, 'form_1': form_1, 'formset': formset,
               'product_image_form': product_image_form, 'category_list': category_list, 'laptop_list': laptop_list,
               'product_images_laptop': laptop_image, 'sub_category_desktop': sub_category_desktop,
               'desktop_list': desktop_list, 'product_images_desktop': desktop_image, 'apple_list': apple_list,
               'apple_image': apple_image, 'sub_category_apple': sub_category_apple,
               'product_images_apple': apple_image, 'sub_category_list': sub_category_list,
               'components_list': components_list, 'product_images_components': components_image,
               'sub_category_components': sub_category_components}
    return render(request, 'vendor_admin_page/products.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_brand_product(request):
    brand_add_form = AddVendorBrands()
    context = {'brand_add_form': brand_add_form}
    return render(request, 'vendor_admin_page/products/add_brand.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_brand_product_post(request):
    if request.method == 'POST':
        form = AddVendorBrands(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data.get("title")
            image = form.cleaned_data.get("photo_img")
            discount = form.cleaned_data.get("discount")

            new_brand = VendorBrands(title=title, photo_img=image, discount=discount)
            new_brand.save()

            messages.success(request, 'Brand added!')
            return redirect('sb_product_vendor_admin_page')


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_subcategory_product(request, _categories):
    brand_add_form = AddVendorBrands()
    context = {'brand_add_form': brand_add_form, 'categories': _categories}
    return render(request, 'vendor_admin_page/products/add_subcategory.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_subcategory_product_post(request, _categories):
    if request.method == 'POST':
        form = AddVendorBrands(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data.get("title")
            image = form.cleaned_data.get("photo_img")
            discount = form.cleaned_data.get("discount")

            new_subcategory = VendorSubCategory(title=title, photo_img=image, discount=discount, categories=_categories)
            new_subcategory.save()

            messages.success(request, 'SubCategory added!')
            return redirect('sb_product_vendor_admin_page')


@admin_only
@login_required(login_url='admin_login_admin')
def product_selected(request):
    producttype = request.GET.get('producttype')

    if producttype == 'Laptops':
        desktop_sub_category_list = VendorSubCategory.objects.filter(categories='Laptops')
        return JsonResponse(list(desktop_sub_category_list.values('id', 'title', 'categories')), safe=False)

    elif producttype == 'Desktops':
        desktop_sub_category_list = VendorSubCategory.objects.filter(categories='Desktops')
        return JsonResponse(list(desktop_sub_category_list.values('id', 'title', 'categories')), safe=False)

    elif producttype == 'Apple':
        desktop_sub_category_list = VendorSubCategory.objects.filter(categories='Apple')
        return JsonResponse(list(desktop_sub_category_list.values('id', 'title', 'categories')), safe=False)

    elif producttype == 'Components':
        desktop_sub_category_list = VendorSubCategory.objects.filter(categories='Components')
        return JsonResponse(list(desktop_sub_category_list.values('id', 'title', 'categories')), safe=False)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_product_add_product_post(request):
    if request.method == 'POST':
        form_1 = AddVendorProducts(request.POST, request.FILES)
        productdescriptionformset = modelformset_factory(VendorProductSpecification, form=AddVendorProductsDescription,
                                                         extra=0)
        formset = productdescriptionformset(request.POST)

        if all([form_1.is_valid(), formset.is_valid]):
            categories = form_1.cleaned_data.get("categories")
            sub_categories = form_1.cleaned_data.get("sub_categories")
            brand = form_1.cleaned_data.get("brand")
            title = form_1.cleaned_data.get("title")
            description = form_1.cleaned_data.get("description")
            stock = form_1.cleaned_data.get("stock")
            latest_price = form_1.cleaned_data.get("latest_price")
            old_price = form_1.cleaned_data.get("old_price")
            condition = form_1.cleaned_data.get("condition")
            price_drop = form_1.cleaned_data.get("price_drop")
            just_launched = form_1.cleaned_data.get("just_launched")

            photo_img = request.FILES.getlist("photo_img")

            title_list = request.POST.getlist('form-__prefix__-title')
            description_list = request.POST.getlist('form-__prefix__-description')

            total_ = zip(title_list, description_list)

            if categories == 'Laptops':
                new_product = VendorLaptopProducts.objects.create(categories=categories, sub_categories=sub_categories,
                                                                  brand=brand, title=title, condition=condition,
                                                                  price_drop=price_drop, just_launched=just_launched,
                                                                  description=description, stock=stock,
                                                                  latest_price=latest_price,
                                                                  old_price=old_price)

                for item in photo_img:
                    VendorProductsImage.objects.create(photo_img=item, product_id=new_product.id,
                                                       products_type=categories)

                for item in total_:
                    if item[0] == '':
                        pass
                    else:
                        VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                  product_id=new_product.id,
                                                                  products_type=categories)

                VendorLatestProducts.objects.create(categories=categories, sub_categories=sub_categories,
                                                    brand=brand, title=title, description=description,
                                                    condition=condition,
                                                    price_drop=price_drop, just_launched=just_launched,
                                                    stock=stock, latest_price=latest_price,
                                                    old_price=old_price, product_id=new_product.id)

                messages.success(request, 'Product Added!')
                return redirect('/admin_vendor/product/')

            elif categories == 'Desktops':
                new_product = VendorDesktopsProducts.objects.create(categories=categories,
                                                                    sub_categories=sub_categories,
                                                                    brand=brand,
                                                                    title=title, condition=condition,
                                                                    price_drop=price_drop, just_launched=just_launched,
                                                                    description=description,
                                                                    stock=stock, latest_price=latest_price,
                                                                    old_price=old_price)
                new_product.save()

                for item in photo_img:
                    new_product_image = VendorProductsImage.objects.create(photo_img=item, product_id=new_product.id,
                                                                           products_type=categories)
                    new_product_image.save()

                for item in total_:
                    if item[0] == '':
                        pass
                    else:
                        VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                  product_id=new_product.id,
                                                                  products_type=categories)

                VendorLatestProducts.objects.create(categories=categories, sub_categories=sub_categories,
                                                    brand=brand, title=title, description=description,
                                                    stock=stock, latest_price=latest_price, condition=condition,
                                                    price_drop=price_drop, just_launched=just_launched,
                                                    old_price=old_price, product_id=new_product.id)

                messages.success(request, 'Product Added!')
                return redirect('/admin_vendor/product/')

            elif categories == 'Apple':
                new_product = VendorAppleProducts.objects.create(categories=categories, sub_categories=sub_categories,
                                                                 brand=brand, condition=condition,
                                                                 price_drop=price_drop, just_launched=just_launched,
                                                                 title=title,
                                                                 description=description,
                                                                 stock=stock, latest_price=latest_price,
                                                                 old_price=old_price)
                new_product.save()

                for item in photo_img:
                    new_product_image = VendorProductsImage.objects.create(photo_img=item, product_id=new_product.id,
                                                                           products_type=categories)
                    new_product_image.save()

                for item in total_:
                    if item[0] == '':
                        pass
                    else:
                        VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                  product_id=new_product.id,
                                                                  products_type=categories)

                VendorLatestProducts.objects.create(categories=categories, sub_categories=sub_categories,
                                                    brand=brand, title=title, description=description,
                                                    stock=stock, latest_price=latest_price, condition=condition,
                                                    price_drop=price_drop, just_launched=just_launched,
                                                    old_price=old_price, product_id=new_product.id)

                messages.success(request, 'Product Added!')
                return redirect('/admin_vendor/product/')

            elif categories == 'Components':
                new_product = VendorComponentsProducts.objects.create(categories=categories,
                                                                      sub_categories=sub_categories,
                                                                      brand=brand, condition=condition,
                                                                      price_drop=price_drop,
                                                                      just_launched=just_launched,
                                                                      title=title,
                                                                      description=description,
                                                                      stock=stock, latest_price=latest_price,
                                                                      old_price=old_price)
                new_product.save()

                for item in photo_img:
                    new_product_image = VendorProductsImage.objects.create(photo_img=item, product_id=new_product.id,
                                                                           products_type=categories)
                    new_product_image.save()

                for item in total_:
                    if item[0] == '':
                        pass
                    else:
                        VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                  product_id=new_product.id,
                                                                  products_type=categories)

                VendorLatestProducts.objects.create(categories=categories, sub_categories=sub_categories,
                                                    brand=brand, title=title, description=description,
                                                    stock=stock, latest_price=latest_price, condition=condition,
                                                    price_drop=price_drop, just_launched=just_launched,
                                                    old_price=old_price, product_id=new_product.id)

                messages.success(request, 'Product Added!')
                return redirect('/admin_vendor/product/')


@admin_only
@login_required(login_url='admin_login_admin')
def sb_edit_product(request, product_type, ids):
    if product_type == 'Laptops':
        product_query = VendorLaptopProducts.objects.get(id=ids)
        product_image_query = VendorProductsImage.objects.filter(product_id=product_query.id,
                                                                 products_type=product_type)
        laptop_spec_query = VendorProductSpecification.objects.filter(products_type='Laptops', product_id=ids)

        form_1 = AddVendorProducts(instance=product_query)
        productdescriptionformset = modelformset_factory(VendorProductSpecification, form=AddVendorProductsDescription,
                                                         can_delete=True, extra=0)
        productimageformset = modelformset_factory(VendorProductsImage, form=AddVendorProductsImage,
                                                   can_delete=True, extra=0)
        formset = productdescriptionformset(prefix='formset', queryset=laptop_spec_query)
        formset1 = productimageformset(prefix='formset1', queryset=product_image_query)
        context = {'form_1': form_1, 'formset': formset, 'ids': ids, 'product_type': product_type,
                   'formset1': formset1}
        return render(request, 'vendor_admin_page/products/editProducts.html', context)

    elif product_type == 'Desktops':
        product_query = VendorDesktopsProducts.objects.get(id=ids)
        product_image_query = VendorProductsImage.objects.filter(product_id=product_query.id,
                                                                 products_type=product_type)
        laptop_spec_query = VendorProductSpecification.objects.filter(products_type='Desktops', product_id=ids)

        form_1 = AddVendorProducts(instance=product_query)
        productdescriptionformset = modelformset_factory(VendorProductSpecification, form=AddVendorProductsDescription,
                                                         can_delete=True, extra=0)
        productimageformset = modelformset_factory(VendorProductsImage, form=AddVendorProductsImage,
                                                   can_delete=True, extra=0)
        formset = productdescriptionformset(prefix='formset', queryset=laptop_spec_query)
        formset1 = productimageformset(prefix='formset1', queryset=product_image_query)

        context = {'form_1': form_1, 'formset': formset, 'ids': ids, 'product_type': product_type,
                   'formset1': formset1}
        return render(request, 'vendor_admin_page/products/editProducts.html', context)

    elif product_type == 'Apple':

        product_query = VendorAppleProducts.objects.get(id=ids)
        product_image_query = VendorProductsImage.objects.filter(product_id=product_query.id,
                                                                 products_type=product_type)
        laptop_spec_query = VendorProductSpecification.objects.filter(products_type='Apple', product_id=ids)

        form_1 = AddVendorProducts(instance=product_query)
        productdescriptionformset = modelformset_factory(VendorProductSpecification, form=AddVendorProductsDescription,
                                                         can_delete=True, extra=0)
        productimageformset = modelformset_factory(VendorProductsImage, form=AddVendorProductsImage,
                                                   can_delete=True, extra=0)
        formset = productdescriptionformset(prefix='formset', queryset=laptop_spec_query)
        formset1 = productimageformset(prefix='formset1', queryset=product_image_query)

        context = {'form_1': form_1, 'formset': formset, 'ids': ids, 'product_type': product_type,
                   'formset1': formset1}
        return render(request, 'vendor_admin_page/products/editProducts.html', context)

    elif product_type == 'Components':

        product_query = VendorComponentsProducts.objects.get(id=ids)
        product_image_query = VendorProductsImage.objects.filter(product_id=product_query.id,
                                                                 products_type=product_type)
        laptop_spec_query = VendorProductSpecification.objects.filter(products_type='Components', product_id=ids)

        form_1 = AddVendorProducts(instance=product_query)
        productdescriptionformset = modelformset_factory(VendorProductSpecification, form=AddVendorProductsDescription,
                                                         can_delete=True, extra=0)
        productimageformset = modelformset_factory(VendorProductsImage, form=AddVendorProductsImage,
                                                   can_delete=True, extra=0)
        formset = productdescriptionformset(prefix='formset', queryset=laptop_spec_query)
        formset1 = productimageformset(prefix='formset1', queryset=product_image_query)

        context = {'form_1': form_1, 'formset': formset, 'ids': ids, 'product_type': product_type,
                   'formset1': formset1}
        return render(request, 'vendor_admin_page/products/editProducts.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_edit_product_post(request, product_type, ids):
    form_1 = AddVendorProducts(request.POST, request.FILES)

    productdescriptionformset = modelformset_factory(VendorProductSpecification, form=AddVendorProductsDescription,
                                                     extra=0)
    formset = productdescriptionformset(request.POST)

    productimageformset = modelformset_factory(VendorProductsImage, form=AddVendorProductsImage,
                                               can_delete=True, extra=0)
    formset1 = productimageformset(request.POST, request.FILES)

    if all([form_1.is_valid(), formset.is_valid, formset1.is_valid]):
        categories = form_1.cleaned_data.get("categories")
        sub_categories = form_1.cleaned_data.get("sub_categories")
        brand = form_1.cleaned_data.get("brand")
        title = form_1.cleaned_data.get("title")
        description = form_1.cleaned_data.get("description")
        stock = form_1.cleaned_data.get("stock")
        latest_price = form_1.cleaned_data.get("latest_price")
        old_price = form_1.cleaned_data.get("old_price")

        photo_img = request.FILES.getlist("photo_img")

        condition = form_1.cleaned_data.get("condition")
        price_drop = form_1.cleaned_data.get("price_drop")
        just_launched = form_1.cleaned_data.get("just_launched")

        title_list = request.POST.getlist('formset-__prefix__-title')
        description_list = request.POST.getlist('formset-__prefix__-description')

        photo_img_list = request.POST.getlist('formset1-__prefix__-photo_img')

        total_ = zip(title_list, description_list)

        if product_type == 'Laptops':
            product_query = VendorLaptopProducts.objects.get(id=ids)
            if product_query:
                if product_query.categories == categories:
                    product_query.sub_categories = sub_categories
                    product_query.brand = brand
                    product_query.title = title
                    product_query.description = description
                    product_query.stock = stock
                    product_query.latest_price = latest_price
                    product_query.old_price = old_price
                    product_query.condition = condition

                    product_query.price_drop = price_drop
                    product_query.just_launched = just_launched

                    product_query.save()

                    formset.save()

                    for item in total_:
                        if item[0] == '':
                            pass
                        else:
                            VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                      product_id=product_query.id,
                                                                      products_type=categories)

                    latest_product = VendorLatestProducts.objects.get(product_id=ids)
                    latest_product.categories = categories
                    latest_product.sub_categories = sub_categories
                    latest_product.brand = brand
                    latest_product.title = title
                    latest_product.description = description
                    latest_product.stock = stock
                    latest_product.latest_price = latest_price
                    latest_product.old_price = old_price
                    latest_product.condition = condition

                    latest_product.price_drop = price_drop
                    latest_product.just_launched = just_launched

                    latest_product.save()

                    messages.success(request, 'Product Edited!')
                    return redirect('/admin_vendor/product/')
                else:
                    if categories == 'Laptops':
                        try:
                            new_product_query = VendorLaptopProducts.objects.create(categories=categories,
                                                                                    sub_categories=sub_categories,
                                                                                    brand=brand,
                                                                                    title=title,
                                                                                    description=description,
                                                                                    price_drop=price_drop,
                                                                                    just_launched=just_launched,
                                                                                    condition=condition,
                                                                                    stock=stock,
                                                                                    latest_price=latest_price,
                                                                                    old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids,
                                                                      products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=image_del,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition

                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')

                    elif categories == 'Desktops':

                        try:
                            new_product_query = VendorDesktopsProducts.objects.create(categories=categories,
                                                                                      sub_categories=sub_categories,
                                                                                      brand=brand,
                                                                                      title=title,
                                                                                      description=description,
                                                                                      condition=condition,
                                                                                      price_drop=price_drop,
                                                                                      just_launched=just_launched,
                                                                                      stock=stock,
                                                                                      latest_price=latest_price,
                                                                                      old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids,
                                                                      products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=image_del,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition

                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')

                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')

                    elif categories == 'Apple':
                        try:

                            new_product_query = VendorAppleProducts.objects.create(categories=categories,
                                                                                   sub_categories=sub_categories,
                                                                                   brand=brand,
                                                                                   title=title,
                                                                                   description=description,
                                                                                   price_drop=price_drop,
                                                                                   just_launched=just_launched,
                                                                                   condition=condition,
                                                                                   stock=stock,
                                                                                   latest_price=latest_price,
                                                                                   old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids,
                                                                      products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=image_del,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition

                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')

                    elif categories == 'Components':

                        try:
                            new_product_query = VendorComponentsProducts.objects.create(categories=categories,
                                                                                        sub_categories=sub_categories,
                                                                                        brand=brand,
                                                                                        title=title,
                                                                                        description=description,
                                                                                        price_drop=price_drop,
                                                                                        just_launched=just_launched,
                                                                                        condition=condition,
                                                                                        stock=stock,
                                                                                        latest_price=latest_price,
                                                                                        old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids, product_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=image_del,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition

                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id
                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')

            else:
                messages.error(request, 'Product not recognized!')
                return redirect('/admin_vendor/product/')

        elif product_type == 'Desktops':
            product_query = VendorDesktopsProducts.objects.get(id=ids)
            if product_query:
                if product_query.categories == categories:
                    product_query.categories = categories
                    product_query.sub_categories = sub_categories
                    product_query.brand = brand
                    product_query.title = title
                    product_query.description = description
                    product_query.stock = stock
                    product_query.latest_price = latest_price
                    product_query.old_price = old_price
                    product_query.condition = condition

                    product_query.price_drop = price_drop
                    product_query.just_launched = just_launched
                    product_query.save()

                    formset.save()

                    for item in total_:
                        if item[0] == '':
                            pass
                        else:
                            VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                      product_id=product_query.id,
                                                                      products_type=categories)

                    latest_product = VendorLatestProducts.objects.get(product_id=ids)
                    latest_product.categories = categories
                    latest_product.sub_categories = sub_categories
                    latest_product.brand = brand
                    latest_product.title = title
                    latest_product.description = description
                    latest_product.stock = stock
                    latest_product.latest_price = latest_price
                    latest_product.old_price = old_price
                    latest_product.condition = condition

                    latest_product.price_drop = price_drop
                    latest_product.just_launched = just_launched
                    latest_product.save()

                    messages.success(request, 'Product Edited!')
                    return redirect('/admin_vendor/product/')
                else:
                    if categories == 'Laptops':
                        try:
                            new_product_query = VendorLaptopProducts.objects.create(categories=categories,
                                                                                    sub_categories=sub_categories,
                                                                                    brand=brand,
                                                                                    title=title,
                                                                                    description=description,
                                                                                    price_drop=price_drop,
                                                                                    just_launched=just_launched,
                                                                                    condition=condition,
                                                                                    stock=stock,
                                                                                    latest_price=latest_price,
                                                                                    old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids,
                                                                      products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=item.photo_img.path,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition

                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')

                    elif categories == 'Desktops':

                        try:
                            new_product_query = VendorDesktopsProducts.objects.create(categories=categories,
                                                                                      sub_categories=sub_categories,
                                                                                      brand=brand,
                                                                                      title=title,
                                                                                      description=description,
                                                                                      condition=condition,
                                                                                      price_drop=price_drop,
                                                                                      just_launched=just_launched,
                                                                                      stock=stock,
                                                                                      latest_price=latest_price,
                                                                                      old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids,
                                                                      products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=item.photo_img.path,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition

                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')

                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')

                    elif categories == 'Apple':
                        try:

                            new_product_query = VendorAppleProducts.objects.create(categories=categories,
                                                                                   sub_categories=sub_categories,
                                                                                   brand=brand,
                                                                                   title=title,
                                                                                   description=description,
                                                                                   price_drop=price_drop,
                                                                                   just_launched=just_launched,
                                                                                   condition=condition,
                                                                                   stock=stock,
                                                                                   latest_price=latest_price,
                                                                                   old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids,
                                                                      products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=item.photo_img.path,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition

                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')

                    elif categories == 'Components':

                        try:
                            new_product_query = VendorComponentsProducts.objects.create(categories=categories,
                                                                                        sub_categories=sub_categories,
                                                                                        brand=brand,
                                                                                        title=title,
                                                                                        description=description,
                                                                                        condition=condition,
                                                                                        price_drop=price_drop,
                                                                                        just_launched=just_launched,
                                                                                        stock=stock,
                                                                                        latest_price=latest_price,
                                                                                        old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids, product_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=item.photo_img.path,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition

                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')
            else:
                messages.error(request, 'Product not recognized!')
                return redirect('/admin_vendor/product/')

        elif product_type == 'Apple':
            product_query = VendorAppleProducts.objects.get(id=ids)
            if product_query:
                if product_query.categories == categories:
                    product_query.categories = categories
                    product_query.sub_categories = sub_categories
                    product_query.brand = brand
                    product_query.title = title
                    product_query.description = description
                    product_query.stock = stock
                    product_query.latest_price = latest_price
                    product_query.old_price = old_price
                    product_query.condition = condition
                    product_query.price_drop = price_drop
                    product_query.just_launched = just_launched
                    product_query.save()

                    formset.save()

                    for item in total_:
                        if item[0] == '':
                            pass
                        else:
                            VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                      product_id=product_query.id,
                                                                      products_type=categories)

                    latest_product = VendorLatestProducts.objects.get(product_id=ids)
                    latest_product.categories = categories
                    latest_product.sub_categories = sub_categories
                    latest_product.brand = brand
                    latest_product.title = title
                    latest_product.description = description
                    latest_product.stock = stock
                    latest_product.latest_price = latest_price
                    latest_product.old_price = old_price
                    latest_product.condition = condition
                    latest_product.price_drop = price_drop
                    latest_product.just_launched = just_launched
                    latest_product.save()

                    messages.success(request, 'Product Edited!')
                    return redirect('/admin_vendor/product/')
                else:
                    if categories == 'Laptops':
                        try:
                            new_product_query = VendorLaptopProducts.objects.create(categories=categories,
                                                                                    sub_categories=sub_categories,
                                                                                    brand=brand,
                                                                                    title=title,
                                                                                    description=description,
                                                                                    condition=condition,
                                                                                    price_drop=price_drop,
                                                                                    just_launched=just_launched,
                                                                                    stock=stock,
                                                                                    latest_price=latest_price,
                                                                                    old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids,
                                                                      products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=item.photo_img.path,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition
                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')

                    elif categories == 'Desktops':

                        try:
                            new_product_query = VendorDesktopsProducts.objects.create(categories=categories,
                                                                                      sub_categories=sub_categories,
                                                                                      brand=brand,
                                                                                      title=title,
                                                                                      description=description,
                                                                                      condition=condition,
                                                                                      price_drop=price_drop,
                                                                                      just_launched=just_launched,
                                                                                      stock=stock,
                                                                                      latest_price=latest_price,
                                                                                      old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids,
                                                                      products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=item.photo_img.path,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition
                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')

                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')

                    elif categories == 'Apple':
                        try:

                            new_product_query = VendorAppleProducts.objects.create(categories=categories,
                                                                                   sub_categories=sub_categories,
                                                                                   brand=brand,
                                                                                   title=title,
                                                                                   description=description,
                                                                                   condition=condition,
                                                                                   price_drop=price_drop,
                                                                                   just_launched=just_launched,
                                                                                   stock=stock,
                                                                                   latest_price=latest_price,
                                                                                   old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids,
                                                                      products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=item.photo_img.path,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition
                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')

                    elif categories == 'Components':

                        try:
                            new_product_query = VendorComponentsProducts.objects.create(categories=categories,
                                                                                        sub_categories=sub_categories,
                                                                                        brand=brand,
                                                                                        title=title,
                                                                                        description=description,
                                                                                        condition=condition,
                                                                                        price_drop=price_drop,
                                                                                        just_launched=just_launched,
                                                                                        stock=stock,
                                                                                        latest_price=latest_price,
                                                                                        old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids,
                                                                      products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=item.photo_img.path,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition
                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')
            else:
                messages.error(request, 'Product not recognized!')
                return redirect('/admin_vendor/product/')

        elif product_type == 'Components':
            product_query = VendorComponentsProducts.objects.get(id=ids)
            if product_query:
                if product_query.categories == categories:
                    product_query.categories = categories
                    product_query.sub_categories = sub_categories
                    product_query.brand = brand
                    product_query.title = title
                    product_query.description = description
                    product_query.stock = stock
                    product_query.latest_price = latest_price
                    product_query.old_price = old_price
                    product_query.condition = condition

                    product_query.price_drop = price_drop
                    product_query.just_launched = just_launched
                    product_query.save()

                    formset.save()

                    for item in total_:
                        if item[0] == '':
                            pass
                        else:
                            VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                      product_id=product_query.id,
                                                                      products_type=categories)

                    latest_product = VendorLatestProducts.objects.get(product_id=ids)
                    latest_product.categories = categories
                    latest_product.sub_categories = sub_categories
                    latest_product.brand = brand
                    latest_product.title = title
                    latest_product.description = description
                    latest_product.stock = stock
                    latest_product.latest_price = latest_price
                    latest_product.old_price = old_price
                    latest_product.condition = condition
                    latest_product.price_drop = price_drop
                    latest_product.just_launched = just_launched
                    latest_product.save()

                    messages.success(request, 'Product Edited!')
                    return redirect('/admin_vendor/product/')
                else:
                    if categories == 'Laptops':
                        try:
                            new_product_query = VendorLaptopProducts.objects.create(categories=categories,
                                                                                    sub_categories=sub_categories,
                                                                                    brand=brand,
                                                                                    title=title,
                                                                                    description=description,
                                                                                    condition=condition,
                                                                                    price_drop=price_drop,
                                                                                    just_launched=just_launched,
                                                                                    stock=stock,
                                                                                    latest_price=latest_price,
                                                                                    old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids,
                                                                      products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=item.photo_img.path,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition
                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')

                    elif categories == 'Desktops':

                        try:
                            new_product_query = VendorDesktopsProducts.objects.create(categories=categories,
                                                                                      sub_categories=sub_categories,
                                                                                      brand=brand,
                                                                                      title=title,
                                                                                      description=description,
                                                                                      condition=condition,
                                                                                      price_drop=price_drop,
                                                                                      just_launched=just_launched,
                                                                                      stock=stock,
                                                                                      latest_price=latest_price,
                                                                                      old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids,
                                                                      products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=item.photo_img.path,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition
                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')

                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')

                    elif categories == 'Apple':
                        try:

                            new_product_query = VendorAppleProducts.objects.create(categories=categories,
                                                                                   sub_categories=sub_categories,
                                                                                   brand=brand,
                                                                                   title=title,
                                                                                   description=description,
                                                                                   condition=condition,
                                                                                   price_drop=price_drop,
                                                                                   just_launched=just_launched,
                                                                                   stock=stock,
                                                                                   latest_price=latest_price,
                                                                                   old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids,
                                                                      products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=item.photo_img.path,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition
                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')

                    elif categories == 'Components':

                        try:
                            new_product_query = VendorComponentsProducts.objects.create(categories=categories,
                                                                                        sub_categories=sub_categories,
                                                                                        brand=brand,
                                                                                        title=title,
                                                                                        description=description,
                                                                                        condition=condition,
                                                                                        price_drop=price_drop,
                                                                                        just_launched=just_launched,
                                                                                        stock=stock,
                                                                                        latest_price=latest_price,
                                                                                        old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            VendorProductSpecification.objects.filter(product_id=ids,
                                                                      products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = VendorProductsImage.objects.filter(product_id=ids,
                                                                                 products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        VendorProductsImage.objects.create(photo_img=item.photo_img.path,
                                                                           products_type=categories,
                                                                           product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    VendorProductSpecification.objects.create(title=item[0], description=item[1],
                                                                              product_id=new_product_query.id,
                                                                              products_type=categories)

                            latest_product = VendorLatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.condition = condition
                            latest_product.price_drop = price_drop
                            latest_product.just_launched = just_launched
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_vendor/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_vendor/product/')
            else:
                messages.error(request, 'Product not recognized!')
                return redirect('/admin_vendor/product/')
    else:
        print(form_1.errors)
        print(formset.errors)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_order(request):
    vendor_user_query = User.objects.filter(Q(is_staff=True), Q(profile__authorization=True))

    context = {'vendor_user_query': vendor_user_query}
    return render(request, 'vendor_admin_page/orders.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_vendor_account(request):
    vendor_user_query = User.objects.filter(Q(is_staff=True), Q(profile__authorization=True))

    context = {'vendor_user_query': vendor_user_query}
    return render(request, 'vendor_admin_page/account.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_per_vendor_account(request, ids):
    order_list = []
    vendor_user_query = User.objects.get(Q(is_staff=True), Q(profile__authorization=True), Q(id=ids))

    per_order = VendorOrder.objects.filter(user=vendor_user_query)
    for items in per_order:
        if items.products_type == 'Laptops':
            product = VendorLaptopProducts.objects.filter(id=items.product_id).last()
            order_list.append((product.title, product.brand, product.latest_price, items.quantity,
                               items.date_time, items.id))
        elif items.products_type == 'Desktops':
            product = VendorDesktopsProducts.objects.filter(id=items.product_id).last()
            order_list.append((product.title, product.brand, product.latest_price, items.quantity,
                               items.date_time, items.id))

        elif items.products_type == 'Apple':
            product = VendorAppleProducts.objects.filter(id=items.product_id).last()
            order_list.append(
                (product.title, product.brand, product.latest_price, items.quantity, items.date_time, items.id))

        elif items.products_type == 'Components':
            product = VendorComponentsProducts.objects.filter(id=items.product_id).last()
            order_list.append(
                (product.title, product.brand, product.latest_price, items.quantity, items.date_time, items.id))

    order_obj = zip(order_list, per_order)
    context = {'vendor_user_query': vendor_user_query, 'order_list': order_obj}
    return render(request, 'vendor_admin_page/order/perVendorList.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_view_vendor_account(request, ids):
    user_list = Profile.objects.get(user_id=ids)
    context = {'ids': ids, 'user_list': user_list}
    return render(request, 'vendor_admin_page/accounts/view_user.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_view_vendor_account_post(request, ids):
    email_exists = False
    if request.method == 'POST':

        contact = request.POST.get("contact")
        fullname = request.POST.get("fullname")
        photo_img = request.FILES.get("photo_img")
        location = request.POST.get("location")
        email = request.POST.get("email")
        username = request.POST.get("username")
        c_password = request.POST.get("c_password")
        password = request.POST.get("password")

        print(photo_img)
        url = '/admin_vendor/vendor_account/' + 'view_vendor_account' + '/' + str(ids)

        admin_all = User.objects.all().exclude(id=ids)

        for items in admin_all:

            if items.email == email:
                email_exists = True
                break
            else:
                email_exists = False

        if email_exists:
            messages.warning(request, 'Email already exists!')

            return redirect(url)

        else:
            user_query = User.objects.get(id=ids)

            if password == c_password:
                try:
                    image_del = user_query.profile.photo_img
                    if photo_img:
                        if image_del:
                            image_del.delete()

                        user_query.username = username
                        user_query.profile.fullname = fullname
                        user_query.email = email
                        user_query.profile.contact = contact
                        user_query.profile.location = location
                        user_query.profile.photo_img = photo_img
                        user_query.set_password(password)
                        user_query.save()
                        user_query.profile.save()

                        messages.success(request, 'User Updated!')
                        return redirect('sb_vendor_account_vendor_admin_page')
                    else:
                        user_query.username = username
                        user_query.profile.fullname = fullname
                        user_query.email = email
                        user_query.profile.contact = contact
                        user_query.profile.location = location
                        user_query.set_password(password)
                        user_query.save()
                        user_query.profile.save()

                        messages.success(request, 'User Updated!')
                        return redirect('sb_vendor_account_vendor_admin_page')
                except:
                    messages.error(request, 'Username exists!')
                    return redirect(url)
            else:
                messages.error(request, 'password does not match!')
                return redirect(url)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_delete_vendor_account_post(request, ids):
    if ids == request.user.id:
        messages.warning(request, 'Conflict detected!')
        return redirect('sb_vendor_account_vendor_admin_page')
    else:
        profile_query = Profile.objects.filter(user_id=ids).last()
        if profile_query.photo_img:
            profile_query.photo_img.delete()

        User.objects.filter(id=ids).delete()
        messages.success(request, 'Account deleted!')
        return redirect('sb_vendor_account_vendor_admin_page')


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_vendor_account(request):
    return render(request, 'vendor_admin_page/accounts/add_admin.html')


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_vendor_account_post(request):
    email_exists = False
    if request.method == 'POST':

        contact = request.POST.get("contact")
        fullname = request.POST.get("fullname")
        photo_img = request.FILES.get("photo_img")
        location = request.POST.get("location")
        email = request.POST.get("email")
        username = request.POST.get("username")
        c_password = request.POST.get("c_password")
        password = request.POST.get("password")

        admin_all = User.objects.all()

        for items in admin_all:

            if items.email == email:
                email_exists = True
                break
            else:
                email_exists = False

        if email_exists:
            messages.warning(request, 'Email already exists!')

            return redirect('sb_add_vendor_account_vendor_admin_page')

        else:

            if password == c_password:
                try:
                    new_user = User(username=username, email=email, is_superuser=0, is_staff=1)
                    new_user.set_password(password)
                    if photo_img:
                        new_profile = Profile(user=new_user, contact=contact, photo_img=photo_img, fullname=fullname,
                                              location=location, authorization=True)
                        new_user.save()
                        new_profile.save()
                    else:
                        new_profile = Profile(user=new_user, contact=contact, fullname=fullname,
                                              location=location, authorization=True)
                        new_user.save()
                        new_profile.save()

                    messages.success(request, 'User Added!')
                    return redirect('sb_vendor_account_vendor_admin_page')

                except Exception as e:
                    print(e)
                    messages.error(request, 'Username exists!')
                    return redirect('sb_add_vendor_account_vendor_admin_page')
            else:
                messages.error(request, 'password does not match!')
                return redirect('sb_add_vendor_account_vendor_admin_page')


@admin_only
@login_required(login_url='admin_login_admin')
def order_status(request):
    data = json.loads(request.body)
    order_id = data['order_id']
    vendor_order_status = data['order_status']

    per_order = VendorOrder.objects.filter(id=order_id).last()

    if int(vendor_order_status) == 1:
        if per_order.verified:
            VendorOrder.objects.filter(id=order_id).update(verified=False)
        else:
            VendorOrder.objects.filter(id=order_id).update(verified=True)
        return JsonResponse({'_actr': 'True'})

    elif int(vendor_order_status) == 2:
        if per_order.delivering:
            VendorOrder.objects.filter(id=order_id).update(delivering=False)
        else:
            VendorOrder.objects.filter(id=order_id).update(delivering=True)
        return JsonResponse({'_actr': 'True'})

    elif int(vendor_order_status) == 3:
        if per_order.delivered:
            VendorOrder.objects.filter(id=order_id).update(delivered=False)
        else:
            VendorOrder.objects.filter(id=order_id).update(delivered=True)
        return JsonResponse({'_actr': 'True'})


@admin_only
@login_required(login_url='admin_login_admin')
def del_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data['order_id']
        product_type = data['product_type']
        user_id = data['user_id']

        cart_add_query = VendorOrder.objects.filter(id=order_id,
                                                    products_type=product_type, user_id=user_id).last()

        cart_add_query.delete()
        return JsonResponse({'_actr': 'True'})