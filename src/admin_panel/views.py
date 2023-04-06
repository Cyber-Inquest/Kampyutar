import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render

from .decorators import admin_only
from admin_panel.forms import LoginForm
try:
    from .forms import  AddBrands, AddSlideshow, AddProducts, AddProductsDescription, AddProductsImage, AddBlog, EditBlog
except:
    pass

from .models import Brand, Order, SubCategory, Slideshow, Profile, Specification, Product, ProductImage, Blogs


@login_required(login_url='admin_login_admin')
def logged_out(request):
    logout(request)
    return redirect('admin_login_admin')


def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('index_admin')
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, "admin_page/login_page.html", context)


def admin_login_post(request):
    if request.method == 'POST':

        user_name = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('index_admin')
            else:
                messages.warning(request, 'Access Denied!')
                return redirect('admin_login_admin')
        else:
            messages.warning(request, 'Wrong credentials!')
            return redirect('admin_login_admin')


@admin_only
@login_required(login_url='admin_login_admin')
def index(request):

    # not delivered not verified and product list for admin to verify

    order_list = Order.objects.filter(verified=False, delivering=False,delivered=False)
    context = {'order_list': order_list}

    return render(request, 'admin_page/index.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_blog(request):
    blogs_query = Blogs.objects.all()
    form = AddBlog()
    context = {'form': form, 'blogs_query': blogs_query}
    return render(request, 'admin_page/blogs/all_blogs.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_blog_post(request):
    form = AddBlog(request.POST, request.FILES)

    if form.is_valid():
        title = form.cleaned_data.get("title")
        editor_name = form.cleaned_data.get("editor_name")
        location = form.cleaned_data.get("location")
        photo_img = form.cleaned_data.get("photo_img")
        blog_summary = form.cleaned_data.get("blog_summary")
        content = form.cleaned_data.get("description")

        Blogs.objects.create(title=title, editor_name=editor_name, location=location, photo_img=photo_img,
                             blog_summary=blog_summary, description=content)
        messages.success(request, 'Blog Added!')
        return redirect('sb_blog_admin')
    else:
        print(form.errors)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_blog_edit(request, ids):
    per_blog_query = Blogs.objects.get(id=ids)
    form = EditBlog(instance=per_blog_query)
    context = {'form': form, 'per_blog_query': per_blog_query}
    return render(request, 'admin_page/blogs/edit_blog.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_blog_edit_post(request, ids):
    form = AddBlog(request.POST, request.FILES)

    if form.is_valid():
        title = form.cleaned_data.get("title")
        editor_name = form.cleaned_data.get("editor_name")
        location = form.cleaned_data.get("location")
        photo_img = form.cleaned_data.get("photo_img")
        blog_summary = form.cleaned_data.get("blog_summary")
        content = form.cleaned_data.get("description")

        blog_query = Blogs.objects.get(id=ids)

        url = '/admin_django/sb_blog_edit/' + str(ids)

        if photo_img != 'default':

            blog_query.photo_img.delete()
            blog_query.title = title
            blog_query.editor_name = editor_name
            blog_query.location = location
            blog_query.blog_summary = blog_summary
            blog_query.content = content
            blog_query.photo_img = photo_img

            blog_query.save()
            messages.success(request, 'Blog Updated!')
            return redirect(url)
        else:
            blog_query.title = title
            blog_query.editor_name = editor_name
            blog_query.location = location
            blog_query.blog_summary = blog_summary
            blog_query.content = content

            blog_query.save()
            messages.success(request, 'Blog Updated!')
            return redirect(url)
    else:
        print(form.errors)


def distinct_image(image_object, product_type):
    list_product_id = []
    per_product_image = []
    for item in image_object:
        list_product_id.append(item.product_id)

    if product_type == 'Laptops':
        for items in set(list_product_id):
            per_product_image.append(ProductsImage.objects.filter(product_id=items, products_type=product_type).last())

    elif product_type == 'Desktops':
        for items in set(list_product_id):
            per_product_image.append(ProductsImage.objects.filter(product_id=items, products_type=product_type).last())

    elif product_type == 'Apple':
        for items in set(list_product_id):
            per_product_image.append(ProductsImage.objects.filter(product_id=items, products_type=product_type).last())

    elif product_type == 'Components':
        for items in set(list_product_id):
            per_product_image.append(ProductsImage.objects.filter(product_id=items, products_type=product_type).last())

    return per_product_image


@admin_only
@login_required(login_url='admin_login_admin')
def sb_product(request):
    brands_list = Brands.objects.all()
    sub_category_list = SubCategory.objects.all()

    sub_category_laptop = SubCategory.objects.filter(categories='Laptops').order_by('categories')
    sub_category_desktop = SubCategory.objects.filter(categories='Desktops').order_by('categories')
    sub_category_apple = SubCategory.objects.filter(categories='Apple').order_by('categories')
    sub_category_components = SubCategory.objects.filter(categories='Components').order_by('categories')

    laptop_list = LaptopProducts.objects.all()
    product_images_laptop = ProductsImage.objects.filter(products_type='Laptops').order_by('product_id').distinct()
    laptop_image = distinct_image(product_images_laptop, 'Laptops')

    desktop_list = DesktopsProducts.objects.all()
    product_images_desktop = ProductsImage.objects.filter(products_type='Desktops').order_by('product_id').distinct()
    desktop_image = distinct_image(product_images_desktop, 'Desktops')

    apple_list = AppleProducts.objects.all()
    product_images_apple = ProductsImage.objects.filter(products_type='Apple').order_by('product_id').distinct()
    apple_image = distinct_image(product_images_apple, 'Apple')

    components_list = ComponentsProducts.objects.all()
    product_images_components = ProductsImage.objects.filter(products_type='Components').order_by(
        'product_id').distinct()
    components_image = distinct_image(product_images_components, 'Components')

    product_specification_list = ProductSpecification.objects.all()
    product_image_form = AddProductsImage()
    category_list = ['Laptops', 'Desktops', 'Apple', 'Components']

    form_1 = AddProducts()

    productdescriptionformset = modelformset_factory(ProductSpecification, form=AddProductsDescription, extra=0)
    formset = productdescriptionformset(queryset=ProductSpecification.objects.none())

    context = {'brands_list': brands_list, 'sub_category_laptop': sub_category_laptop,
               'product_specification_list': product_specification_list, 'form_1': form_1, 'formset': formset,
               'product_image_form': product_image_form, 'category_list': category_list, 'laptop_list': laptop_list,
               'product_images_laptop': laptop_image, 'sub_category_desktop': sub_category_desktop,
               'desktop_list': desktop_list, 'product_images_desktop': desktop_image, 'apple_list': apple_list,
               'apple_image': apple_image, 'sub_category_apple': sub_category_apple,
               'product_images_apple': apple_image, 'sub_category_list': sub_category_list,
               'components_list': components_list, 'product_images_components': components_image,
               'sub_category_components': sub_category_components}
    return render(request, 'admin_page/products.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_product_add_product_post(request):
    if request.method == 'POST':
        form_1 = AddProducts(request.POST, request.FILES)
        productdescriptionformset = modelformset_factory(ProductSpecification, form=AddProductsDescription, extra=0)
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
            featured_product = form_1.cleaned_data.get("featured_product")
            coming_soon = form_1.cleaned_data.get("coming_soon")

            photo_img = request.FILES.getlist("photo_img")

            title_list = request.POST.getlist('form-__prefix__-title')
            description_list = request.POST.getlist('form-__prefix__-description')

            total_ = zip(title_list, description_list)

            if categories == 'Laptops':
                new_product = LaptopProducts.objects.create(categories=categories, sub_categories=sub_categories,
                                                            brand=brand,
                                                            title=title, coming_soon=coming_soon,
                                                            featured_product=featured_product,
                                                            description=description,
                                                            stock=stock, latest_price=latest_price, old_price=old_price)

                for item in photo_img:
                    ProductsImage.objects.create(photo_img=item, product_id=new_product.id,
                                                 products_type=categories)

                for item in total_:
                    if item[0] == '':
                        pass
                    else:
                        ProductSpecification.objects.create(title=item[0], description=item[1],
                                                            product_id=new_product.id,
                                                            products_type=categories)

                LatestProducts.objects.create(categories=categories, sub_categories=sub_categories,
                                              brand=brand, title=title, description=description,
                                              stock=stock, latest_price=latest_price, coming_soon=coming_soon,
                                              featured_product=featured_product,
                                              old_price=old_price, product_id=new_product.id)

                messages.success(request, 'Product Added!')
                return redirect('/admin_django/product/')

            elif categories == 'Desktops':
                new_product = DesktopsProducts.objects.create(categories=categories, sub_categories=sub_categories,
                                                              brand=brand,
                                                              title=title, coming_soon=coming_soon,
                                                              featured_product=featured_product,
                                                              description=description,
                                                              stock=stock, latest_price=latest_price,
                                                              old_price=old_price)
                new_product.save()

                for item in photo_img:
                    new_product_image = ProductsImage.objects.create(photo_img=item, product_id=new_product.id,
                                                                     products_type=categories)
                    new_product_image.save()

                for item in total_:
                    if item[0] == '':
                        pass
                    else:
                        ProductSpecification.objects.create(title=item[0], description=item[1],
                                                            product_id=new_product.id,
                                                            products_type=categories)

                LatestProducts.objects.create(categories=categories, sub_categories=sub_categories,
                                              brand=brand, title=title, description=description,
                                              stock=stock, latest_price=latest_price, coming_soon=coming_soon,
                                              featured_product=featured_product,
                                              old_price=old_price, product_id=new_product.id)

                messages.success(request, 'Product Added!')
                return redirect('/admin_django/product/')

            elif categories == 'Apple':
                new_product = AppleProducts.objects.create(categories=categories, sub_categories=sub_categories,
                                                           brand=brand, coming_soon=coming_soon,
                                                           featured_product=featured_product,
                                                           title=title,
                                                           description=description,
                                                           stock=stock, latest_price=latest_price, old_price=old_price)
                new_product.save()

                for item in photo_img:
                    new_product_image = ProductsImage.objects.create(photo_img=item, product_id=new_product.id,
                                                                     products_type=categories)
                    new_product_image.save()

                for item in total_:
                    if item[0] == '':
                        pass
                    else:
                        ProductSpecification.objects.create(title=item[0], description=item[1],
                                                            product_id=new_product.id,
                                                            products_type=categories)

                LatestProducts.objects.create(categories=categories, sub_categories=sub_categories,
                                              brand=brand, title=title, description=description,
                                              stock=stock, latest_price=latest_price, coming_soon=coming_soon,
                                              featured_product=featured_product,
                                              old_price=old_price, product_id=new_product.id)

                messages.success(request, 'Product Added!')
                return redirect('/admin_django/product/')

            elif categories == 'Components':
                new_product = ComponentsProducts.objects.create(categories=categories, sub_categories=sub_categories,
                                                                brand=brand,
                                                                title=title,
                                                                description=description, coming_soon=coming_soon,
                                                                featured_product=featured_product,
                                                                stock=stock, latest_price=latest_price,
                                                                old_price=old_price)
                new_product.save()

                for item in photo_img:
                    new_product_image = ProductsImage.objects.create(photo_img=item, product_id=new_product.id,
                                                                     products_type=categories)
                    new_product_image.save()

                for item in total_:
                    if item[0] == '':
                        pass
                    else:
                        ProductSpecification.objects.create(title=item[0], description=item[1],
                                                            product_id=new_product.id,
                                                            products_type=categories)

                LatestProducts.objects.create(categories=categories, sub_categories=sub_categories,
                                              brand=brand, title=title, description=description,
                                              stock=stock, latest_price=latest_price, coming_soon=coming_soon,
                                              featured_product=featured_product,
                                              old_price=old_price, product_id=new_product.id)

                messages.success(request, 'Product Added!')
                return redirect('/admin_django/product/')


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_category_product(request):
    brand_add_form = AddBrands()
    context = {'brand_add_form': brand_add_form}
    return render(request, 'admin_page/products/add_category.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_edit_product(request, product_type, ids):
    if product_type == 'Laptops':
        product_query = LaptopProducts.objects.get(id=ids)
        product_image_query = ProductsImage.objects.filter(product_id=product_query.id, products_type=product_type)
        laptop_spec_query = ProductSpecification.objects.filter(products_type='Laptops', product_id=ids)

        form_1 = AddProducts(instance=product_query)
        productdescriptionformset = modelformset_factory(ProductSpecification, form=AddProductsDescription,
                                                         can_delete=True, extra=0)
        productimageformset = modelformset_factory(ProductsImage, form=AddProductsImage,
                                                   can_delete=True, extra=0)
        formset = productdescriptionformset(prefix='formset', queryset=laptop_spec_query)
        formset1 = productimageformset(prefix='formset1', queryset=product_image_query)
        context = {'form_1': form_1, 'formset': formset, 'ids': ids, 'product_type': product_type,
                   'formset1': formset1}
        return render(request, 'admin_page/products/editProducts.html', context)

    elif product_type == 'Desktops':
        product_query = DesktopsProducts.objects.get(id=ids)
        product_image_query = ProductsImage.objects.filter(product_id=product_query.id, products_type=product_type)
        laptop_spec_query = ProductSpecification.objects.filter(products_type='Desktops', product_id=ids)

        form_1 = AddProducts(instance=product_query)
        productdescriptionformset = modelformset_factory(ProductSpecification, form=AddProductsDescription,
                                                         can_delete=True, extra=0)
        productimageformset = modelformset_factory(ProductsImage, form=AddProductsImage,
                                                   can_delete=True, extra=0)
        formset = productdescriptionformset(prefix='formset', queryset=laptop_spec_query)
        formset1 = productimageformset(prefix='formset1', queryset=product_image_query)

        context = {'form_1': form_1, 'formset': formset, 'ids': ids, 'product_type': product_type,
                   'formset1': formset1}
        return render(request, 'admin_page/products/editProducts.html', context)

    elif product_type == 'Apple':

        product_query = AppleProducts.objects.get(id=ids)
        product_image_query = ProductsImage.objects.filter(product_id=product_query.id, products_type=product_type)
        laptop_spec_query = ProductSpecification.objects.filter(products_type='Apple', product_id=ids)

        form_1 = AddProducts(instance=product_query)
        productdescriptionformset = modelformset_factory(ProductSpecification, form=AddProductsDescription,
                                                         can_delete=True, extra=0)
        productimageformset = modelformset_factory(ProductsImage, form=AddProductsImage,
                                                   can_delete=True, extra=0)
        formset = productdescriptionformset(prefix='formset', queryset=laptop_spec_query)
        formset1 = productimageformset(prefix='formset1', queryset=product_image_query)

        context = {'form_1': form_1, 'formset': formset, 'ids': ids, 'product_type': product_type,
                   'formset1': formset1}
        return render(request, 'admin_page/products/editProducts.html', context)

    elif product_type == 'Components':

        product_query = ComponentsProducts.objects.get(id=ids)
        product_image_query = ProductsImage.objects.filter(product_id=product_query.id, products_type=product_type)
        laptop_spec_query = ProductSpecification.objects.filter(products_type='Components', product_id=ids)

        form_1 = AddProducts(instance=product_query)
        productdescriptionformset = modelformset_factory(ProductSpecification, form=AddProductsDescription,
                                                         can_delete=True, extra=0)
        productimageformset = modelformset_factory(ProductsImage, form=AddProductsImage,
                                                   can_delete=True, extra=0)
        formset = productdescriptionformset(prefix='formset', queryset=laptop_spec_query)
        formset1 = productimageformset(prefix='formset1', queryset=product_image_query)

        context = {'form_1': form_1, 'formset': formset, 'ids': ids, 'product_type': product_type,
                   'formset1': formset1}
        return render(request, 'admin_page/products/editProducts.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_edit_product_post(request, product_type, ids):
    form_1 = AddProducts(request.POST, request.FILES)

    productdescriptionformset = modelformset_factory(ProductSpecification, form=AddProductsDescription, extra=0)
    formset = productdescriptionformset(request.POST)

    productimageformset = modelformset_factory(ProductsImage, form=AddProductsImage,
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
        coming_soon = form_1.cleaned_data.get("coming_soon")
        featured_product = form_1.cleaned_data.get("featured_product")
        photo_img = request.FILES.getlist("photo_img")
        title_list = request.POST.getlist('formset-__prefix__-title')
        description_list = request.POST.getlist('formset-__prefix__-description')

        photo_img_list = request.POST.getlist('formset1-__prefix__-photo_img')

        total_ = zip(title_list, description_list)

        if product_type == 'Laptops':
            product_query = LaptopProducts.objects.get(id=ids)
            if product_query:
                if product_query.categories == categories:
                    product_query.sub_categories = sub_categories
                    product_query.brand = brand
                    product_query.title = title
                    product_query.description = description
                    product_query.stock = stock
                    product_query.latest_price = latest_price
                    product_query.old_price = old_price
                    product_query.coming_soon = coming_soon

                    product_query.featured_product = featured_product

                    product_query.save()

                    formset.save()

                    for item in total_:
                        if item[0] == '':
                            pass
                        else:
                            ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                product_id=product_query.id,
                                                                products_type=categories)

                    latest_product = LatestProducts.objects.get(product_id=ids)
                    latest_product.categories = categories
                    latest_product.sub_categories = sub_categories
                    latest_product.brand = brand
                    latest_product.title = title
                    latest_product.description = description
                    latest_product.stock = stock
                    latest_product.latest_price = latest_price
                    latest_product.old_price = old_price
                    latest_product.coming_soon = coming_soon
                    latest_product.featured_product = featured_product

                    latest_product.save()

                    messages.success(request, 'Product Edited!')
                    return redirect('/admin_django/product/')
                else:
                    if categories == 'Laptops':
                        try:
                            new_product_query = LaptopProducts.objects.create(categories=categories,
                                                                              sub_categories=sub_categories,
                                                                              brand=brand,
                                                                              title=title,
                                                                              description=description,
                                                                              coming_soon=coming_soon,
                                                                              featured_product=featured_product,
                                                                              stock=stock, latest_price=latest_price,
                                                                              old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=image_del, products_type=categories,
                                                                     product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')

                    elif categories == 'Desktops':

                        try:
                            new_product_query = DesktopsProducts.objects.create(categories=categories,
                                                                                sub_categories=sub_categories,
                                                                                brand=brand,
                                                                                title=title,
                                                                                description=description,
                                                                                coming_soon=coming_soon,
                                                                                featured_product=featured_product,
                                                                                stock=stock, latest_price=latest_price,
                                                                                old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=image_del, products_type=categories,
                                                                     product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')

                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')

                    elif categories == 'Apple':
                        try:

                            new_product_query = AppleProducts.objects.create(categories=categories,
                                                                             sub_categories=sub_categories,
                                                                             brand=brand,
                                                                             title=title,
                                                                             description=description,
                                                                             coming_soon=coming_soon,
                                                                             featured_product=featured_product,
                                                                             stock=stock, latest_price=latest_price,
                                                                             old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=image_del, products_type=categories,
                                                                     product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')

                    elif categories == 'Components':

                        try:
                            new_product_query = ComponentsProducts.objects.create(categories=categories,
                                                                                  sub_categories=sub_categories,
                                                                                  brand=brand,
                                                                                  title=title,
                                                                                  description=description,
                                                                                  coming_soon=coming_soon,
                                                                                  featured_product=featured_product,
                                                                                  stock=stock, latest_price=latest_price,
                                                                                  old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, product_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=image_del, products_type=categories,
                                                                     product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id
                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')

            else:
                messages.error(request, 'Product not recognized!')
                return redirect('/admin_django/product/')

        elif product_type == 'Desktops':
            product_query = DesktopsProducts.objects.get(id=ids)
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
                    product_query.coming_soon = coming_soon

                    product_query.featured_product = featured_product
                    product_query.save()

                    formset.save()

                    for item in total_:
                        if item[0] == '':
                            pass
                        else:
                            ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                product_id=product_query.id,
                                                                products_type=categories)

                    latest_product = LatestProducts.objects.get(product_id=ids)
                    latest_product.categories = categories
                    latest_product.sub_categories = sub_categories
                    latest_product.brand = brand
                    latest_product.title = title
                    latest_product.description = description
                    latest_product.stock = stock
                    latest_product.latest_price = latest_price
                    latest_product.old_price = old_price
                    latest_product.coming_soon = coming_soon
                    latest_product.featured_product = featured_product
                    latest_product.save()

                    messages.success(request, 'Product Edited!')
                    return redirect('/admin_django/product/')
                else:
                    if categories == 'Laptops':
                        try:
                            new_product_query = LaptopProducts.objects.create(categories=categories,
                                                                              sub_categories=sub_categories,
                                                                              brand=brand,
                                                                              title=title,
                                                                              description=description,
                                                                              coming_soon=coming_soon,
                                                                              featured_product=featured_product,
                                                                              stock=stock, latest_price=latest_price,
                                                                              old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=item.photo_img.path, products_type=categories,
                                                                     product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')

                    elif categories == 'Desktops':

                        try:
                            new_product_query = DesktopsProducts.objects.create(categories=categories,
                                                                                sub_categories=sub_categories,
                                                                                brand=brand,
                                                                                title=title,
                                                                                description=description,
                                                                                coming_soon=coming_soon,
                                                                                featured_product=featured_product,
                                                                                stock=stock, latest_price=latest_price,
                                                                                old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=item.photo_img.path, products_type=categories,
                                                                     product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')

                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')

                    elif categories == 'Apple':
                        try:

                            new_product_query = AppleProducts.objects.create(categories=categories,
                                                                             sub_categories=sub_categories,
                                                                             brand=brand,
                                                                             title=title,
                                                                             description=description,
                                                                             coming_soon=coming_soon,
                                                                             featured_product=featured_product,
                                                                             stock=stock, latest_price=latest_price,
                                                                             old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=item.photo_img.path, products_type=categories,
                                                                     product_id=new_product_query.id)


                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')

                    elif categories == 'Components':

                        try:
                            new_product_query = ComponentsProducts.objects.create(categories=categories,
                                                                                  sub_categories=sub_categories,
                                                                                  brand=brand,
                                                                                  title=title,
                                                                                  description=description,
                                                                                  coming_soon=coming_soon,
                                                                                  featured_product=featured_product,
                                                                                  stock=stock,
                                                                                  latest_price=latest_price,
                                                                                  old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, product_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=item.photo_img.path, products_type=categories,
                                                                     product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')
            else:
                messages.error(request, 'Product not recognized!')
                return redirect('/admin_django/product/')

        elif product_type == 'Apple':
            product_query = AppleProducts.objects.get(id=ids)
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
                    product_query.coming_soon = coming_soon

                    product_query.featured_product = featured_product
                    product_query.save()

                    formset.save()

                    for item in total_:
                        if item[0] == '':
                            pass
                        else:
                            ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                product_id=product_query.id,
                                                                products_type=categories)

                    latest_product = LatestProducts.objects.get(product_id=ids)
                    latest_product.categories = categories
                    latest_product.sub_categories = sub_categories
                    latest_product.brand = brand
                    latest_product.title = title
                    latest_product.description = description
                    latest_product.stock = stock
                    latest_product.latest_price = latest_price
                    latest_product.old_price = old_price
                    latest_product.coming_soon = coming_soon
                    latest_product.featured_product = featured_product
                    latest_product.save()

                    messages.success(request, 'Product Edited!')
                    return redirect('/admin_django/product/')
                else:
                    if categories == 'Laptops':
                        try:
                            new_product_query = LaptopProducts.objects.create(categories=categories,
                                                                              sub_categories=sub_categories,
                                                                              brand=brand,
                                                                              title=title,
                                                                              description=description,
                                                                              coming_soon=coming_soon,
                                                                              featured_product=featured_product,
                                                                              stock=stock, latest_price=latest_price,
                                                                              old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=item.photo_img.path, products_type=categories,
                                                                     product_id=new_product_query.id)


                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')

                    elif categories == 'Desktops':

                        try:
                            new_product_query = DesktopsProducts.objects.create(categories=categories,
                                                                                sub_categories=sub_categories,
                                                                                brand=brand,
                                                                                title=title,
                                                                                description=description,
                                                                                coming_soon=coming_soon,
                                                                                featured_product=featured_product,
                                                                                stock=stock, latest_price=latest_price,
                                                                                old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=item.photo_img.path, products_type=categories,
                                                                     product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')

                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')

                    elif categories == 'Apple':
                        try:

                            new_product_query = AppleProducts.objects.create(categories=categories,
                                                                             sub_categories=sub_categories,
                                                                             brand=brand,
                                                                             title=title,
                                                                             description=description,
                                                                             coming_soon=coming_soon,
                                                                             featured_product=featured_product,
                                                                             stock=stock, latest_price=latest_price,
                                                                             old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=item.photo_img.path, products_type=categories,
                                                                     product_id=new_product_query.id)


                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')

                    elif categories == 'Components':

                        try:
                            new_product_query = ComponentsProducts.objects.create(categories=categories,
                                                                                  sub_categories=sub_categories,
                                                                                  brand=brand,
                                                                                  title=title,
                                                                                  description=description,
                                                                                  coming_soon=coming_soon,
                                                                                  featured_product=featured_product,
                                                                                  stock=stock,
                                                                                  latest_price=latest_price,
                                                                                  old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=item.photo_img.path, products_type=categories,
                                                                     product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')
            else:
                messages.error(request, 'Product not recognized!')
                return redirect('/admin_django/product/')

        elif product_type == 'Components':
            product_query = ComponentsProducts.objects.get(id=ids)
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
                    product_query.coming_soon = coming_soon

                    product_query.featured_product = featured_product
                    product_query.save()

                    formset.save()

                    for item in total_:
                        if item[0] == '':
                            pass
                        else:
                            ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                product_id=product_query.id,
                                                                products_type=categories)

                    latest_product = LatestProducts.objects.get(product_id=ids)
                    latest_product.categories = categories
                    latest_product.sub_categories = sub_categories
                    latest_product.brand = brand
                    latest_product.title = title
                    latest_product.description = description
                    latest_product.stock = stock
                    latest_product.latest_price = latest_price
                    latest_product.old_price = old_price
                    latest_product.coming_soon = coming_soon
                    latest_product.featured_product = featured_product
                    latest_product.save()

                    messages.success(request, 'Product Edited!')
                    return redirect('/admin_django/product/')
                else:
                    if categories == 'Laptops':
                        try:
                            new_product_query = LaptopProducts.objects.create(categories=categories,
                                                                              sub_categories=sub_categories,
                                                                              brand=brand,
                                                                              title=title,
                                                                              description=description,
                                                                              coming_soon=coming_soon,
                                                                              featured_product=featured_product,
                                                                              stock=stock, latest_price=latest_price,
                                                                              old_price=old_price)

                            new_product_query.save()   

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=item.photo_img.path, products_type=categories,
                                                                     product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')

                    elif categories == 'Desktops':

                        try:
                            new_product_query = DesktopsProducts.objects.create(categories=categories,
                                                                                sub_categories=sub_categories,
                                                                                brand=brand,
                                                                                title=title,
                                                                                description=description,
                                                                                coming_soon=coming_soon,
                                                                                featured_product=featured_product,
                                                                                stock=stock, latest_price=latest_price,
                                                                                old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=item.photo_img.path, products_type=categories,
                                                                     product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()
                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')

                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')

                    elif categories == 'Apple':
                        try:

                            new_product_query = AppleProducts.objects.create(categories=categories,
                                                                             sub_categories=sub_categories,
                                                                             brand=brand,
                                                                             title=title,
                                                                             description=description,
                                                                             coming_soon=coming_soon,
                                                                             featured_product=featured_product,
                                                                             stock=stock, latest_price=latest_price,
                                                                             old_price=old_price)

                            new_product_query.save()

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=item.photo_img.path, products_type=categories,
                                                                     product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')

                    elif categories == 'Components':

                        try:
                            new_product_query = ComponentsProducts.objects.create(categories=categories,
                                                                                  sub_categories=sub_categories,
                                                                                  brand=brand,
                                                                                  title=title,
                                                                                  description=description,
                                                                                  coming_soon=coming_soon,
                                                                                  featured_product=featured_product,
                                                                                  stock=stock,
                                                                                  latest_price=latest_price,
                                                                                  old_price=old_price)

                            new_product_query.save()  

                            formset.save()

                            ProductSpecification.objects.filter(product_id=ids, products_type=product_type).update(
                                products_type=categories, product_id=new_product_query.id)

                            all_image_query = ProductsImage.objects.filter(product_id=ids, products_type=product_type)
                            if all_image_query:
                                for item in all_image_query:
                                    image_del = item.photo_img
                                    if image_del:
                                        ProductsImage.objects.create(photo_img=item.photo_img.path, products_type=categories,
                                                                     product_id=new_product_query.id)

                                all_image_query.delete()

                            for item in total_:
                                if item[0] == '':
                                    pass
                                else:
                                    ProductSpecification.objects.create(title=item[0], description=item[1],
                                                                        product_id=new_product_query.id,
                                                                        products_type=categories)

                            latest_product = LatestProducts.objects.get(product_id=ids)
                            latest_product.categories = categories
                            latest_product.sub_categories = sub_categories
                            latest_product.brand = brand
                            latest_product.title = title
                            latest_product.description = description
                            latest_product.stock = stock
                            latest_product.latest_price = latest_price
                            latest_product.old_price = old_price
                            latest_product.coming_soon = coming_soon
                            latest_product.featured_product = featured_product
                            latest_product.product_id = new_product_query.id

                            latest_product.save()

                            product_query.delete()

                            messages.success(request, 'Product Edited!')
                            return redirect('/admin_django/product/')
                        except Exception as e:
                            messages.success(request, e)
                            return redirect('/admin_django/product/')
            else:
                messages.error(request, 'Product not recognized!')
                return redirect('/admin_django/product/')
    else:
        print(form_1.errors)
        print(formset.errors)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_subcategory_product(request, _categories):
    brand_add_form = AddBrands()
    context = {'brand_add_form': brand_add_form, 'categories': _categories}
    return render(request, 'admin_page/products/add_subcategory.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_subcategory_product_post(request, _categories):
    if request.method == 'POST':
        form = AddBrands(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data.get("title")
            image = form.cleaned_data.get("photo_img")
            discount = form.cleaned_data.get("discount")

            new_subcategory = SubCategory(title=title, photo_img=image, discount=discount, categories=_categories)
            new_subcategory.save()

            messages.success(request, 'SubCategory added!')
            return redirect('sb_product_admin')


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_brand_product(request):
    brand_add_form = AddBrands()
    context = {'brand_add_form': brand_add_form}
    return render(request, 'admin_page/products/add_brand.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_brand_product_post(request):
    if request.method == 'POST':
        form = AddBrands(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data.get("title")
            image = form.cleaned_data.get("photo_img")
            discount = form.cleaned_data.get("discount")

            new_brand = Brands(title=title, photo_img=image, discount=discount)
            new_brand.save()

            messages.success(request, 'Brand added!')
            return redirect('sb_product_admin')


@admin_only
@login_required(login_url='admin_login_admin')
def sb_images(request):
    slideshow_list = Slideshow.objects.all()

    context = {'slideshow_list': slideshow_list}
    return render(request, 'admin_page/images.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_images(request):
    add_images = AddSlideshow()
    context = {'add_images': add_images}
    return render(request, 'admin_page/banner/add_banner.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_images_post(request):
    if request.method == 'POST':
        form = AddSlideshow(request.POST, request.FILES)

        if form.is_valid():
            link = form.cleaned_data.get("link")
            image = form.cleaned_data.get("photo_img")

            new_slideshow = Slideshow(link=link, photo_img=image)
            new_slideshow.save()

            messages.success(request, 'Slideshow added!')
            return redirect(sb_images)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_del_images(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['productId']

        slideshowlist_query = Slideshow.objects.get(id=product_id)
        slideshowlist_query.delete()
        return JsonResponse({'_actr': 'True'})


@admin_only
@login_required(login_url='admin_login_admin')
def image_slideshow(request):
    slideshow_list = Slideshow.objects.all()

    context = {'slideshow_list': slideshow_list}
    return render(request, 'admin_page/banner/preview_slideshow.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def image_slideshow_deploy(request):
    slideshow_list = Slideshow.objects.filter(upload=0)
    for item in slideshow_list:
        item.upload = 1
        item.save()

    messages.success(request, 'Slideshow Deployed!')
    return redirect(sb_images)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_ads(request):
    return render(request, 'admin_page/ads.html')


@admin_only
@login_required(login_url='admin_login_admin')
def sb_account(request):
    user_list = User.objects.filter(is_superuser=1, is_staff=0, profile__authorization=False)
    customer_list = User.objects.filter(is_superuser=0, is_staff=1, profile__authorization=False)
    context = {'user_list': user_list, 'customer_list': customer_list}
    return render(request, 'admin_page/account.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_view_admin_account(request, ids):
    user_list = Profile.objects.get(user_id=ids)
    context = {'ids': ids, 'user_list': user_list}
    return render(request, 'admin_page/accounts/view_user.html', context)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_view_admin_account_post(request, ids):
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

        url = '/admin_django/account/' + 'view_admin_account' + '/' + str(ids)

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
                        return redirect('sb_account_admin')
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
                        return redirect('sb_account_admin')
                except:
                    messages.error(request, 'Username exists!')
                    return redirect(url)
            else:
                messages.error(request, 'password does not match!')
                return redirect(url)


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_admin_account(request):
    return render(request, 'admin_page/accounts/add_admin.html')


@admin_only
@login_required(login_url='admin_login_admin')
def sb_add_admin_account_post(request):
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

            return redirect('sb_add_admin_account_admin')

        else:

            if password == c_password:
                try:
                    new_user = User(username=username, email=email, is_superuser=1)
                    new_user.set_password(password)
                    if photo_img:
                        new_profile = Profile(user=new_user, contact=contact, photo_img=photo_img, fullname=fullname,
                                              location=location,authorization=True)
                        new_user.save()
                        new_profile.save()
                    else:
                        new_profile = Profile(user=new_user, contact=contact, fullname=fullname,
                                              location=location,authorization=True )
                        new_user.save()
                        new_profile.save()

                    messages.success(request, 'User Added!')
                    return redirect('sb_account_admin')

                except Exception as e:
                    print(e)
                    messages.error(request, 'Username exists!')
                    return redirect('sb_add_admin_account_admin')
            else:
                messages.error(request, 'password does not match!')
                return redirect('sb_add_admin_account_admin')


@admin_only
@login_required(login_url='admin_login_admin')
def sb_delete_admin_account_post(request, ids):
    if ids == request.user.id:
        messages.warning(request, 'Conflict detected!')
        return redirect('sb_account_admin')
    else:
        profile_query = Profile.objects.filter(user_id=ids).last()
        if profile_query.photo_img:
            profile_query.photo_img.delete()

        User.objects.filter(id=ids).delete()
        messages.success(request, 'Account deleted!')
        return redirect('sb_account_admin')


@admin_only
@login_required(login_url='admin_login_admin')
def del_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['productId']
        producttype = data['producttype']

        if producttype == 'Laptops':
            product_query = LaptopProducts.objects.get(id=product_id, categories=producttype)

            product_news_query = LatestProducts.objects.filter(product_id=product_id, categories=producttype)
            product_news_query.delete()

            ProductSpecification.objects.filter(product_id=product_id, products_type=producttype).delete()

            product_image = ProductsImage.objects.filter(product_id=product_id, products_type=producttype)
            for item in product_image:
                if item.photo_img:
                    item.photo_img.delete()
                item.delete()

            product_query.delete()
            return JsonResponse({'_actr': 'True'})

        elif producttype == 'Desktops':
            product_query = DesktopsProducts.objects.get(id=product_id, categories=producttype)

            product_news_query = LatestProducts.objects.get(product_id=product_id, categories=producttype)
            product_news_query.delete()

            ProductSpecification.objects.filter(product_id=product_id, products_type=producttype).delete()

            product_image = ProductsImage.objects.filter(product_id=product_id, products_type=producttype)
            for item in product_image:
                if item.photo_img:
                    item.photo_img.delete()
                item.delete()

            product_query.delete()

            return JsonResponse({'_actr': 'True'})

        elif producttype == 'Apple':
            product_query = AppleProducts.objects.get(id=product_id, categories=producttype)

            product_news_query = LatestProducts.objects.get(product_id=product_id, categories=producttype)
            product_news_query.delete()

            ProductSpecification.objects.filter(product_id=product_id, products_type=producttype).delete()

            product_image = ProductsImage.objects.filter(product_id=product_id, products_type=producttype)
            for item in product_image:
                if item.photo_img:
                    item.photo_img.delete()
                item.delete()

            product_query.delete()

            return JsonResponse({'_actr': 'True'})

        elif producttype == 'Components':
            product_query = ComponentsProducts.objects.get(id=product_id, categories=producttype)

            product_news_query = LatestProducts.objects.get(product_id=product_id, categories=producttype)
            product_news_query.delete()

            ProductSpecification.objects.filter(product_id=product_id, products_type=producttype).delete()

            product_image = ProductsImage.objects.filter(product_id=product_id, products_type=producttype)
            for item in product_image:
                if item.photo_img:
                    item.photo_img.delete()
                item.delete()

            product_query.delete()

            return JsonResponse({'_actr': 'True'})


@admin_only
@login_required(login_url='admin_login_admin')
def product_selected(request):
    producttype = request.GET.get('producttype')

    if producttype == 'Laptops':
        desktop_sub_category_list = SubCategory.objects.filter(categories='Laptops')
        return JsonResponse(list(desktop_sub_category_list.values('id', 'title', 'categories')), safe=False)

    elif producttype == 'Desktops':
        desktop_sub_category_list = SubCategory.objects.filter(categories='Desktops')
        return JsonResponse(list(desktop_sub_category_list.values('id', 'title', 'categories')), safe=False)

    elif producttype == 'Apple':
        desktop_sub_category_list = SubCategory.objects.filter(categories='Apple')
        return JsonResponse(list(desktop_sub_category_list.values('id', 'title', 'categories')), safe=False)

    elif producttype == 'Components':
        desktop_sub_category_list = SubCategory.objects.filter(categories='Components')
        return JsonResponse(list(desktop_sub_category_list.values('id', 'title', 'categories')), safe=False)
