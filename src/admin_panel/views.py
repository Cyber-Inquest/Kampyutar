import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render

from app.forms import LoginForm
from .models import Specification
from django.db.models import Sum, F
from django.db.models import Sum, OuterRef, Subquery,F


from .decorators import is_staff


from .models import Brand, Category, Order, SubCategory, Profile, Specification, Product, ProductImage


@login_required(login_url='admin_login')
@is_staff
def index(request):

    completed_order_list_objects = Order.objects.filter(verified=True,delivering = True,delivered=True).order_by('-id')
    recent_order_list_objects = Order.objects.exclude(verified=True,delivering = True,delivered=True).order_by('-id')  
    
    batch_orders = Order.objects.values('batch').annotate(
        total_quantity=Subquery(
            Order.objects.filter(batch=OuterRef('batch')).values('batch').annotate(
                total_qty=Sum('quantity')
            ).values('total_qty')
        )
    ).annotate(
        total_amount=Subquery(
            Order.objects.filter(batch=OuterRef('batch')).values('batch').annotate(
                total_amnt=Sum(F('quantity') * F('product__latest_price'))
            ).values('total_amnt')
        )
    ).annotate(
        ordered_date = Subquery(Order.objects.filter(batch=OuterRef('batch')).values('batch').annotate(
        ordered_date=F('date_time')).values('ordered_date'))
               ).distinct().values('batch','total_quantity','total_amount','user__username','ordered_date')
    
    recent_order_list_objects = batch_orders.exclude(verified=True,delivering = True,delivered=True)
    completed_order_list_objects = batch_orders.filter(verified=True,delivering = True,delivered=True)
    context = {
        'recent_order_list': recent_order_list_objects,
        'completed_order_list': completed_order_list_objects,
    }


    return render(request, 'admin_panel/index.html', context)

@login_required(login_url='admin_login')
@is_staff
def admin_product(request):
    product_list_objects = Product.objects.filter(is_shown = True).order_by('-id')
    featured_product_list_objects = Product.objects.filter(is_featured = True).order_by('-id')
    comming_soon_list_objects = Product.objects.filter(is_comming_soon = True).order_by('-id')
    
    category_list_objects = Category.objects.filter(is_shown = True)
    context = {
        'featured_product_list': featured_product_list_objects,
        'comming_soon_list': comming_soon_list_objects,
        'product_list': product_list_objects,
        'category_list': category_list_objects
        }
    return render(request, 'admin_panel/product.html',context)

@login_required(login_url='admin_login')
@is_staff
def admin_product_add(request,id):
    if request.method == 'GET':
        selected_category_object = Category.objects.get(id=id)
        sub_category_list_objects = SubCategory.objects.filter(category=selected_category_object,is_shown = True)
        brand_list_objects = Brand.objects.filter(is_shown = True)
        context = {

            'selected_category': selected_category_object,
            'sub_category_list': sub_category_list_objects,
            'brand_list': brand_list_objects
            }
        return render(request, 'admin_panel/add_product.html',context)
    if request.method == 'POST':
        sub_category = request.POST.get('selected_sub_category')
        brand = request.POST.get('selected_brand')
        title = request.POST.get('product_title')
        short_description = request.POST.get('product_short_description')
        description = request.POST.get('product_description')
        keywords = request.POST.get('product_keywords')
        model_number = request.POST.get('product_model_no')
        product_quantity = request.POST.get('product_qty')
        product_latest_price = request.POST.get('product_lprice')
        product_previous_price = request.POST.get('product_oprice')
        is_commingsoon = request.POST.get('is_commingsoon')
        is_featured = request.POST.get('is_featured')
        is_shown = request.POST.get('is_shown')

        is_featured = False if is_featured == None else True
        is_commingsoon = False if is_commingsoon == None else True
        is_shown = False if is_shown == None else True

        product_save = Product(

            categories = Category.objects.get(id=id),
            sub_categories = SubCategory.objects.get(id=sub_category),
            brands = Brand.objects.get(id=brand),
            title = title,
            short_description = short_description,
            description = description,
            keywords = keywords,
            model_number = model_number,
            stock = product_quantity,
            latest_price = product_latest_price,
            previous_price = product_previous_price,
            is_featured = is_featured,
            is_comming_soon = is_commingsoon,
            is_shown = is_shown,
        )
        product_save.save()
        latest_product = Product.objects.latest('id')

        product_specification_title = request.POST.getlist('spec_title')
        product_specification_description = request.POST.getlist('spec_description')
        

        specifications = []
        for i in range(len(product_specification_title)):
            title = product_specification_title[i]
            description = product_specification_description[i]
            specification = Specification(product = latest_product, title=title, description=description)
            specifications.append(specification)

        Specification.objects.bulk_create(specifications)

        product_image_list = request.FILES.getlist('product_image')

        for image in product_image_list:
            new_image = ProductImage(product = latest_product, image=image)
            new_image.save()

        return redirect('admin_product')
    



def admin_login(request):
    next_url = request.GET.get('next')
    if request.method == 'GET':
        if request.user.is_authenticated and request.user.is_staff:
            return redirect('index_admin')
        form = LoginForm(initial={'next': next_url})  # Pass the 'next' value to the login form
        context = {'form': form}
        return render(request, "admin_panel/login.html", context)
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('index_admin')
            else:
                messages.warning(request, 'Access Denied!')
                return redirect('admin_login')
        else:
            messages.warning(request, 'Wrong credentials!')
            return redirect('admin_login')

@login_required(login_url='admin_login')
@is_staff
def admin_sets(request):
    category_list_objects = Category.objects.all()
    sub_category_list_objects = SubCategory.objects.all()
    brand_list_objects = Brand.objects.all()

    context = {
        'category_list': category_list_objects,
        'brand_list': brand_list_objects,
        'sub_category_list': sub_category_list_objects
        }
    return render(request, 'admin_panel/sets.html',context)

@login_required(login_url='admin_login')
@is_staff
def admin_category_add(request):
    if request.method == 'GET':
        return render(request, 'admin_panel/add_category.html')
    if request.method == 'POST':
        category_title = request.POST.get('category_title')
        category_is_shown = request.POST.get('category_is_shown')
        category_image = request.FILES.get('category_image')

        category_is_shown = False if category_is_shown == None else True

        category_save = Category(
            title = category_title,
            is_shown = category_is_shown,
            image = category_image
        )
        category_save.save()
        return redirect('admin_sets')

@login_required(login_url='admin_login')
@is_staff   
def admin_subcategory_add(request,id):
    if request.method == 'GET':
        category_list_objects = Category.objects.get(id=id)
        context = {'category_list': category_list_objects}
        return render(request, 'admin_panel/add_sub_category.html',context)
    if request.method == 'POST':
        category = request.POST.get('product_title_id')
        sub_category_title = request.POST.get('sub_category_title')
        sub_category_is_shown = request.POST.get('sub_category_is_shown')
        sub_category_image = request.FILES.get('sub_category_image')

        sub_category_is_shown = False if sub_category_is_shown == None else True

        sub_category_save = SubCategory(
            category = Category.objects.get(id=category),
            title = sub_category_title,
            image = sub_category_image,
            is_shown = sub_category_is_shown
        )
        sub_category_save.save()
        return redirect('admin_sets')

@login_required(login_url='admin_login')
@is_staff
def admin_brand_add(request):
    if request.method == 'GET':
        return render(request, 'admin_panel/add_brand.html')
    if request.method == 'POST':
        brand_title = request.POST.get('brand_title')
        brand_is_shown = request.POST.get('brand_is_shown')
        brand_image = request.FILES.get('brand_image')

        brand_is_shown = False if brand_is_shown == None else True

        brand_save = Brand(
            title = brand_title,
            image = brand_image,
            is_shown = brand_is_shown
        )
        brand_save.save()
        return redirect('admin_sets')

@login_required(login_url='admin_login')
@is_staff
def admin_user_account(request):
    staff_list_object = User.objects.filter(is_superuser=0, is_staff=1)
    customer_list_object = User.objects.filter(is_superuser=0, is_staff=0)
    context = {
        'staff_list': staff_list_object, 
        'customer_list': customer_list_object
        }
    return render(request, 'admin_panel/user_account.html', context)

@login_required(login_url='admin_login')
@is_staff
def admin_staff_add(request):
    if request.method == 'GET':
        return render(request, 'admin_panel/staff_add.html')
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

        
        email_exists = User.objects.filter(email=email).exists()
        username_exists = User.objects.filter(username=username).exists()

        if email_exists:
            messages.warning(request, 'Email already exists!')
            return redirect('admin_staff_add')
        if username_exists:
            return redirect('admin_staff_add')

        else:

            if password == c_password:
                try:
                    new_user = User(username=username, email=email, is_staff=1, is_superuser=0)
                    new_user.set_password(password)
                    new_user.save()
                    if photo_img:
                        Profile.objects.filter(user=new_user).update(contact=contact, photo_img=photo_img, fullname=fullname,
                                                location=location,authorization=True)
                        
                    else:
                        Profile.objects.filter(user=new_user).update(contact=contact, fullname=fullname,
                                                location=location,authorization=True)
                    messages.success(request, 'User Added!')
                    return redirect('admin_user_account')
                except Exception as e:
                    print(e)
                    messages.error(request, 'Error Occured!')
                    return redirect('admin_staff_add')
            else:
                messages.error(request, 'password does not match!')
                return redirect('admin_staff_add')

@login_required(login_url='admin_login')
@is_staff
def admin_staff_edit(request, id):
    if request.method == 'GET':
        user_list = Profile.objects.get(user_id=id)
        context = {'ids': id, 'user_list': user_list}
        return render(request, 'admin_panel/staff_edit.html', context)
    if request.method == 'POST':
        url = f'/admin-staff-edit/{id}/'
        admin_all = False
        user_name_all = False
        contact = request.POST.get("contact")
        fullname = request.POST.get("fullname")
        photo_img = request.FILES.get("photo_img")
        location = request.POST.get("location")
        email = request.POST.get("email")
        username = request.POST.get("username")
        c_password = request.POST.get("c_password")
        password = request.POST.get("password")

        admin_all = User.objects.all().exclude(id=id)
        user_name_all = User.objects.all().exclude(id=id)
        for items in admin_all:

            if items.email == email:
                email_exists = True
                break
            else:
                email_exists = False
        for items in user_name_all:

            if items.username == username:
                email_exists = True
                break
            else:
                email_exists = False

        if email_exists:
            messages.warning(request, 'Email already exists!')

            return redirect(url)
        if email_exists:
            messages.warning(request, 'Username already exists!')

            return redirect(url)

        else:
            user_query = User.objects.get(id=id)

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
                        return redirect('admin_user_account')
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
                        return redirect('admin_user_account')
                except:
                    messages.error(request, 'Username exists!')
                    return redirect(url)
            else:
                messages.error(request, 'password does not match!')
                return redirect(url)

@login_required(login_url='admin_login')
@is_staff
def admin_product_detail(request, id):
    product_details = Product.objects.get(id=id)
    context = {'product': product_details}
    return render(request, 'admin_panel/product_details.html', context)


@login_required(login_url='admin_login')
@is_staff
def admin_product_edit(request, id):
    if request.method == 'GET':
        product_details = Product.objects.get(id=id)
        subcategory_list_object = SubCategory.objects.filter(category__id=product_details.categories.id,is_shown=True)
        
        brand_list_object = Brand.objects.filter(is_shown=True)
        # print(product_details.specification_set.all())
        context = {
            'product_details': product_details,
            'subcategory_list': subcategory_list_object,
            'brand_list': brand_list_object,
            }
        return render(request, 'admin_panel/product_edit.html', context)
    if request.method == 'POST':
        product_details = Product.objects.get(id=id)
        product_sub_category = request.POST.get("selected_sub_category")
        product_brand = request.POST.get("selected_brand")
        product_title = request.POST.get("product_title")
        product_short_description = request.POST.get("product_short_description")
        product_keywords = request.POST.get("product_keywords")
        product_model_no = request.POST.get("product_model_no")
        product_description = request.POST.get("product_description")
        product_qty = request.POST.get("product_qty")
        product_latest_price = request.POST.get("product_lprice")
        product_previous_price = request.POST.get("product_oprice")
        product_is_featured = request.POST.get("is_featured")

        product_is_commingsoon = request.POST.get("is_commingsoon")
        product_is_shown = request.POST.get("is_shown")	

        is_featured = False if product_is_featured == None else True
        is_comming_soon = False if product_is_commingsoon == None else True
        is_shown = False if product_is_shown == None else True

        Product.objects.filter(id=id).update(
            sub_categories = SubCategory.objects.get(id=product_sub_category),
            brands = Brand.objects.get(id=product_brand),
            title = product_title,
            short_description = product_short_description,
            keywords = product_keywords,
            model_number = product_model_no,
            description = product_description,
            stock = product_qty,
            latest_price = product_latest_price,
            previous_price = product_previous_price,
            is_featured = is_featured,
            is_comming_soon = is_comming_soon,
            is_shown = is_shown,
            )
        product_specification_title_list = request.POST.getlist("spec_title")
        product_specification_description_list = request.POST.getlist("spec_description")
        Specification.objects.filter(product=product_details).delete()
        for i in range(len(product_specification_title_list)):
            if product_specification_title_list[i] == '':
                pass
            else:
                title = product_specification_title_list[i]
                description = product_specification_description_list[i]
                Specification.objects.create(product = product_details, title=title, description=description)
                print(title, description)

        deleted_image_ids = request.POST.getlist('deleted_image_ids')
        if len(deleted_image_ids) == 1 and deleted_image_ids[0] == '':
            pass
        else:
            ids = [int(id) for id in deleted_image_ids[0].split(',')]
            ProductImage.objects.filter(id__in=ids).delete()
        product_image_list = request.FILES.getlist('product_image')

        for image in product_image_list:
            new_image = ProductImage(product = product_details, image=image)
            new_image.save()
        return redirect(admin_product_detail, id=id)


@login_required(login_url='admin_login')
@is_staff
def admin_category_edit(request, id):
    if request.method == 'GET':
        category_details = Category.objects.get(id=id)
        context = {'category': category_details}
        return render(request, 'admin_panel/edit_category.html', context)
    if request.method == 'POST':
        print(request.POST)
        category_details = Category.objects.get(id=id)
        category_title = request.POST.get("category_title")
        category_is_shown = request.POST.get("category_is_shown")
        category_image = request.FILES.get("category_image")
        print(category_image)
        is_shown = False if category_is_shown == None else True
        if category_image == None:
            Category.objects.filter(id=id).update(
                title = category_title,
                is_shown = is_shown,
                )
        else:
            
            category_object =  Category.objects.get(id=id)
            category_object.title = category_title
            category_object.is_shown = is_shown
            category_object.image = category_image
            category_object.save()
        return redirect(admin_sets)  



@login_required(login_url='admin_login')
@is_staff
def admin_subcategory_edit(request, id):
    if request.method == 'GET':
        subcategory_details = SubCategory.objects.get(id=id)
        context = {
            'subcategory': subcategory_details,
            }
        return render(request, 'admin_panel/edit_sub_category.html', context)
    if request.method == 'POST':
        subcategory_details = SubCategory.objects.get(id=id)
        subcategory_title = request.POST.get("sub_category_title")
        category_id = request.POST.get("category_title_id")
        subcategory_is_shown = request.POST.get("sub_category_is_shown")
        subcategory_image = request.FILES.get("sub_category_image")
        is_shown = False if subcategory_is_shown == None else True
        if subcategory_image == None:
            SubCategory.objects.filter(id=id).update(
                title = subcategory_title,
                is_shown = is_shown,
                category = Category.objects.get(id=category_id),
                )
        else:
            sub_category_object = SubCategory.objects.get(id=id)
            sub_category_object.title = subcategory_title
            sub_category_object.is_shown = is_shown
            sub_category_object.category = Category.objects.get(id=category_id)
            sub_category_object.image = subcategory_image
            sub_category_object.save()
        return redirect(admin_sets)


@login_required(login_url='admin_login')
@is_staff  
def admin_brand_edit(request, id):
    if request.method == 'GET':
        brand_details = Brand.objects.get(id=id)
        context = {'brand': brand_details}
        return render(request, 'admin_panel/edit_brands.html', context)
    if request.method == 'POST':
        brand_details = Brand.objects.get(id=id)
        brand_title = request.POST.get("brand_title")
        brand_is_shown = request.POST.get("brand_is_shown")
        brand_image = request.FILES.get("brand_image")
        is_shown = False if brand_is_shown == None else True
        if brand_image == None:
            Brand.objects.filter(id=id).update(
                title = brand_title,
                is_shown = is_shown,
                )
        else:
            brand_objects = Brand.objects.get(id=id)
            brand_objects.title = brand_title
            brand_objects.is_shown = is_shown
            brand_objects.image = brand_image
            brand_objects.save()
            
        return redirect(admin_sets)


def logged_out(request):
    logout(request)
    return redirect('admin_login')
