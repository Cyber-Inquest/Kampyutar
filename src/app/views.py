# helper functions
import re
from functools import reduce
from itertools import chain

from django.template.defaultfilters import safe
from queryset_sequence import QuerySetSequence

from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db.models import Max, Min, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Sum, OuterRef, Subquery,F,Value,Case,When,IntegerField


# models
from admin_panel.models import Address, Category, Order, Billing, Delivery, Wishlist, Cart , Blogs
from admin_panel.models import Profile, ProductImage, Specification, Product, Slideshow, SubCategory, Brand, ProductReview

# forms/filters
from .decorators import client_only
try:
    from .filters import SnippetFilterProductList
except:
    pass
from .forms import LoginForm
from .filters import SnippetFilterProductList
# inbuilt
import json


#region updatedCode

# after logged-in if there is any data in cookie save the data into db and clear the cookie
def cookie_cart_loging(request, _current_user):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = None
    if cart:
        # for each product type
        for item in cart:
            check_data = Cart.objects.filter(user=_current_user, product_id=item).last()
            if check_data:
                check_data.quantity += cart[item]['quantity']
                check_data.save()
            else:
                Cart.objects.create(user=_current_user,quantity=cart[item]['quantity'],product_id=item)


# getting data for navbar which is in dictonary format and return the data
def get_navbar_data():
    nav_bar_categories      = Category.objects.filter(is_shown=True).distinct()
    nav_bar_subcategories   = SubCategory.objects.filter(is_shown=True, product__isnull=False).distinct()
    nav_bar_brands          = Brand.objects.filter(product__isnull=False).distinct()

    json_data = {
        a + 1: {
            "category_name": category.title.upper(),
            "category_slug": category.slug,
            "subcategory": {
                b + 1: {
                    "subcategory_name": subcategory.title.capitalize(),
                    "subcategory_id": subcategory.id,
                    "brand": {
                        c + 1: {
                            "brand_name": brand.title.capitalize(),
                            "brand_id": brand.id,
                        } for c, brand in enumerate(nav_bar_brands.filter(product__sub_categories=subcategory))
                    }
                } for b, subcategory in enumerate(nav_bar_subcategories.filter(category=category))
            }
        } for a, category in enumerate(nav_bar_categories)
    }
    return json_data
     
# get cart for individual user which return dictonary format for navbar content

def get_nav_cart_data(request):
    cart_quantity_total = 0
    cart_total_price = 0
    order = {
        'cart_total_price': 0, 
        'cart_total_items': 0,
        'cart_saved_price': 0}
    if request.user.is_authenticated: 
        cart_details_object = Cart.objects.filter(user=request.user)
        cart_quantity_total = cart_details_object.aggregate(total_quantity = Sum('quantity'))['total_quantity']

        cart_total_price = Cart.objects.filter(user=request.user).annotate(item_price=Subquery(Product.objects.filter(pk=OuterRef('product__id')).values('latest_price'))).aggregate(total=Sum(F('item_price')* F('quantity')))['total']
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except KeyError:
            cart = None
        if cart:
            for i in cart:
                product = Product.objects.get(id=i)
                total_price = (product.latest_price * int(cart[i]["quantity"]))
                order['cart_total_price'] += total_price
                order['cart_total_items'] += int(cart[i]["quantity"])
                if product.previous_price == 0:
                    pass
                else:
                    order['cart_saved_price'] += ((product.previous_price - product.latest_price) * int(cart[i]["quantity"]))
            cart_quantity_total = order['cart_total_items']
            cart_total_price = order['cart_total_price']
    cart_data = {
        'cart_quantity_total': cart_quantity_total,
        'cart_total_price': cart_total_price,
    }
    return cart_data


# Home page of client side
def index(request):
    #for all the product that categories in front end 
    featured_products_objects = Product.objects.filter(is_featured=True, is_comming_soon=False, is_shown=True).annotate(is_in_wishllist=Case(When(wishlist_product__user=request.user, then=Value(True)), default=Value(False))).order_by('-id')[:10]
    print(featured_products_objects.values())
    comming_soon_products_objects = Product.objects.filter(is_comming_soon=True,is_shown=True).annotate(is_in_wishllist=Case(When(wishlist_product__user=request.user, then=Value(True)), default=Value(False))).order_by('-id')[:10]
    new_arrival_products_objects = Product.objects.filter(is_comming_soon=False, is_shown=True).annotate(is_in_wishllist=Case(When(wishlist_product__user=request.user, then=Value(True)), default=Value(False))).order_by('-id')[:10]
    category_objects = Category.objects.all()
    all_products_objects = Product.objects.all().annotate(is_in_wishllist=Case(When(wishlist_product__user=request.user, then=Value(True)), default=Value(False)))
    
    blog_list = Blogs.objects.all()
    cart_data = get_nav_cart_data(request)
    nav_bar_json_data = get_navbar_data()
     
    index_data = {
        
        'featured_product': featured_products_objects,
        'comming_soon_product': comming_soon_products_objects,
        'new_arrival_product': new_arrival_products_objects,
        'category': category_objects,
        'all_products': all_products_objects,
        'blog_list': blog_list,
        'json_data': nav_bar_json_data,
        'current_user': request.user,
    }
    context = {**index_data, **cart_data}

    return render(request, 'app/index.html', context)


# for list of products after clicking on category it takes slug as a id 
def product_list(request,slug):
    product_list_categories_objects = Product.objects.filter(categories__slug=slug).all()
    selected_category_object = Category.objects.filter(slug=slug).first()

    product_max_min = Product.objects.filter(categories__slug=slug).aggregate(Max('latest_price'), Min('latest_price'))
    min_price = product_max_min['latest_price__min']
    max_price = product_max_min['latest_price__max']
    snippet_filter = SnippetFilterProductList(request.GET, queryset=product_list_categories_objects,category=selected_category_object)
    snippet_filter_product_list = snippet_filter.qs

    show_by_number = request.GET.get('show_by')

    photo_list = []
    user_wishlist_mark = []

    # get the value from user for displaying required items per page
    if show_by_number is not None:
        if show_by_number:
            paginated_filtered = Paginator(snippet_filter_product_list, int(show_by_number))
        else:
            paginated_filtered = Paginator(snippet_filter_product_list, 12)
    else:
        paginated_filtered = Paginator(snippet_filter_product_list, 12)

    # pagination
    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)

    # to mark wishlist if user is authenticated and item is in wishlist
    for items in page_obj:
        if request.user.is_authenticated :
            wishlist_query_components = Wishlist.objects.filter(product_id=items.id,
                                                                user=request.user).last()
            if wishlist_query_components:
                user_wishlist_mark.append('True')
            else:
                user_wishlist_mark.append('False')
        else:
            user_wishlist_mark.append('False')

    # to show image with product in list page
    for item in page_obj:
        photo_list.append(ProductImage.objects.filter(product_id=item.id).last())

    # bundling object with its corresponding image
    zip_pro_img = zip(page_obj, photo_list, user_wishlist_mark)
    # change to list
    zip_pro_img = list(zip_pro_img)

    products = Product.objects.filter(categories__pk=1)
    brands = Brand.objects.filter(product__in=products).distinct()

    cart_data = get_nav_cart_data(request)
    nav_bar_json_data = get_navbar_data()

    product_list_data = {
        'min_price': min_price, 'max_price': max_price,
        'product_list': product_list_categories_objects,
        'laptop_brand': brands,
        'snippet_filter': snippet_filter,
        'zip_pro_img': zip_pro_img,
        'json_data': nav_bar_json_data,
        # 'nav_bar_brands': nav_bar_brands_objects,
        'current_user': request.user,
    }
    context = {**product_list_data, **cart_data}
    return render(request, 'app/product_list.html', context)



#product details page
def product_detail(request,slug,id):
    logged_in_user = request.user
    product_object = Product.objects.get(id=id)
    image_object = ProductImage.objects.filter(product_id=id)
    product_specification = Specification.objects.filter(product_id=id)
    products_review_object = ProductReview.objects.filter(product_id=id).order_by('-id')

    if ProductReview.objects.filter(user=logged_in_user, product=product_object).exists():
        review_status = True
        product_review_object = ProductReview.objects.get(user=logged_in_user, product=product_object)
    else:
        review_status = False
        product_review_object = None

    cart_data = get_nav_cart_data(request)
    nav_bar_json_data = get_navbar_data()
    product_details_data = {
        'product': product_object,
        'per_images': image_object,
        'product_specs': product_specification,
        'json_data': nav_bar_json_data,
        'current_user': logged_in_user,
        'products_review': products_review_object,
        'review_status': review_status,
        'product_review': product_review_object,


    }
    context = {**product_details_data, **cart_data}
    return render(request, 'app/product_details.html',context)



#searching product from navbar it will search in brands title category sub category and product title and so on 
def search_product(request):
    if request.method == 'GET':
        search_key = request.GET.get('query')
        searching_result = Product.objects.filter(Q(title__icontains=search_key)|Q(short_description__icontains=search_key)|Q(description__icontains=search_key)|Q(keywords__icontains=search_key)|Q(model_number__icontains=search_key)|Q(categories__title__icontains=search_key,categories__is_shown=True)|Q(brands__title__icontains=search_key,brands__is_shown=True)|Q(sub_categories__title__icontains=search_key,sub_categories__is_shown=True))
        cart_data = get_nav_cart_data(request)
        nav_bar_json_data = get_navbar_data()
        serach_result_data  = {
                'product_searching_result_list' : searching_result, 
                'current_user' : request.user,
                'json_data': nav_bar_json_data,
                    }
        context = {**cart_data,**serach_result_data}
        return render(request, 'app/search_product.html',context)

 
    
# client details orders wishlist and update the profile 
def client_profile(request):
    if not request.user.is_authenticated:
        return redirect('client_sign_in') 
    else:
        logged_in_user = request.user
        if request.method == 'POST':
            email_exists = False

            # get the user input first and last name
            account_first_name = request.POST.get('account_first_name')
            account_last_name = request.POST.get('account_last_name')

            # get the checkbox value for email changes
            chkBox2 = request.POST.get('chkBox2')

            account_old_email = request.POST.get('account_old_email')
            account_new_email = request.POST.get('account_new_email')

            # get the checkbox value for password changes
            chkBox = request.POST.get('chkBox')
            account_old_password = request.POST.get('account_old_password')
            account_new_password = request.POST.get('account_new_password')
            account_confirm_password = request.POST.get('account_confirm_password')

            # get the address details
            account_company = request.POST.get('account_company')
            account_street = request.POST.get('account_street')
            account_town = request.POST.get('account_town')
            account_state = request.POST.get('account_state')
            account_zip = request.POST.get('account_zip')
            if account_zip == '':
                account_zip = 0
            account_number = request.POST.get('account_number')

            # get current user objects from db
            user_query = User.objects.filter(username = logged_in_user).last()

            if user_query:

                # if user request to change email
                if chkBox2 is not None and account_old_email != account_new_email and account_new_email != '':

                    if user_query.email == account_old_email:

                        # check whether the new email is already in use
                        email_exists = User.objects.filter(email=account_new_email).exists()

                        # if given new email is already in use show proper message to the user
                        if email_exists:
                            messages.error(request, 'User with this email is already in use')
                            return redirect('client_profile')
                        else:
                            user_query.email = account_new_email
                            messages.success(request, 'User Email updated')
                    else:
                        messages.error(request, 'Old email does not match')
                        return redirect('client_profile')

                # if user request to change password
                if chkBox is not None:

                    # error handling for the password
                    if account_new_password == account_confirm_password:
                        if check_password(account_old_password, user_query.password):
                            user_query.set_password(account_new_password)
                            messages.success(request, 'User Password updated')
                        else:
                            messages.error(request, 'Current password does not match')
                            return redirect('client_profile')
                    else:
                        messages.error(request, 'New Password does not match')
                        return redirect('client_profile')

                user_query.first_name = account_first_name
                user_query.last_name = account_last_name

                # Check the address table
                address_query = Address.objects.filter(user = user_query).last()
                if address_query:
                    address_query.first_name = account_first_name
                    address_query.last_name = account_last_name

                    address_query.company_name = account_company
                    address_query.street_address = account_street
                    address_query.town_city = account_town
                    address_query.state = account_state
                    address_query.zip = account_zip
                    address_query.contact = account_number
                    address_query.save()
                else:
                    Address.objects.create(user=user_query, 
                                   first_name=account_first_name, last_name=account_last_name,
                                   company_name=account_company, street_address=account_street, town_city=account_town,
                                   state=account_state, zip=account_zip, contact=account_number)
                user_query.save()

                messages.success(request, 'User Profile updated')
                return redirect('client_profile')
            else:
                messages.error(request, 'User not recognized')
                return redirect('client_profile')

        if request.method == 'GET':
            logged_in_user = request.user
            profile_details = Profile.objects.get(user=logged_in_user)
            address_details = Address.objects.filter(user=logged_in_user)
            order_details = Order.objects.filter(user=logged_in_user)
            wishlist_list = Wishlist.objects.filter(user=logged_in_user).annotate(product_image = Subquery(ProductImage.objects.filter(product_id=OuterRef('product_id')).values('image')[:1]))

            cart_data = get_nav_cart_data(request)
            nav_bar_json_data = get_navbar_data()

            profile_data = {'profile_details': profile_details,
                        'address_details': address_details,
                        'order_details': order_details,
                        'wishlist_list': wishlist_list,
                        'current_user': logged_in_user,
                        'json_data': nav_bar_json_data,
                        } 
            context = {**profile_data, **cart_data}
            return render(request, 'app/client_profile.html', context)
    
  
# execute after place product to cart 
def order_proceed(request):
    if request.user.id:
        current_user = request.user
        user_details = User.objects.filter(id=current_user.id).last()

        if request.method == 'POST':
            billing_firstname = request.POST.get('billing_firstname')
            billing_lastname = request.POST.get('billing_lastname')
            billing_company = request.POST.get('billing_company')
            billing_street = request.POST.get('billing_street')
            billing_town = request.POST.get('billing_town')
            billing_state = request.POST.get('billing_state')
            billing_zip = request.POST.get('billing_zip')
            billing_number = request.POST.get('billing_number')

            delivery_firstname = request.POST.get('delivery_firstname')
            delivery_lastname = request.POST.get('delivery_lastname')
            delivery_company = request.POST.get('delivery_company')
            delivery_street = request.POST.get('delivery_street')
            delivery_town = request.POST.get('delivery_town')
            delivery_state = request.POST.get('delivery_state')
            delivery_zip = request.POST.get('delivery_zip')
            delivery_number = request.POST.get('delivery_number')

            cart_list = Cart.objects.filter(user=user_details)
            try:
                batch_number = Order.objects.last().batch + 1
            except:
                batch_number = 1
            for item in cart_list:
                Order.objects.create( product=item.product, quantity=item.quantity,
                                    user=user_details,batch = batch_number)

            cart_list.delete()

            Billing.objects.create(user=user_details,batch = batch_number, 
                                   first_name=billing_firstname, last_name=billing_lastname,
                                   company_name=billing_company, street_address=billing_street, town_city=billing_town,
                                   state=billing_state, zip=billing_zip, contact=billing_number)
            
            Delivery.objects.create(user=user_details,batch = batch_number,
                                    first_name=delivery_firstname, last_name=delivery_lastname,
                                    company_name=delivery_company, street_address=delivery_street, town_city=delivery_town,
                                    state=delivery_state, zip=delivery_zip, contact=delivery_number)
            
            return redirect('index_app')
        if request.method == 'GET':
            address = Address.objects.filter(user=current_user).last()
            cart_data = get_nav_cart_data(request)
            nav_bar_json_data = get_navbar_data()
            order_proceed_data = {
                'user_details': user_details,
                'address': address,
                'json_data': nav_bar_json_data,
            }
            context = {**order_proceed_data, **cart_data}
        return render(request, 'client_page/order_proceed.html', context)
    else:
        return redirect('client_sign_in')
    

# function that execute shopping_cart form topbar
def shopping_cart(request):
    order = {'cart_total_price': 0, 'cart_total_items': 0,'cart_saved_price': 0}
    current_user = request.user.id
    nav_bar_json_data = get_navbar_data()
    if current_user: 
        cart_details_object = Cart.objects.filter(user=current_user)
        cart_quantity_total = cart_details_object.aggregate(total_quantity = Sum('quantity'))['total_quantity']
        cart_total_price = Cart.objects.filter(user=current_user).annotate(
        item_price=Subquery(Product.objects.filter(pk=OuterRef('product__id')).values('latest_price'))).aggregate(total=Sum(F('item_price')* F('quantity')))['total']
        cart_product_list_objects = Cart.objects.filter(user = request.user).annotate(saved_amount = (F('product__previous_price') - F('product__latest_price'))*F('quantity')).annotate(product_image = Subquery(ProductImage.objects.filter(product_id = OuterRef('product__id')).values('image')[:1]))
        
        items_total = cart_product_list_objects.aggregate(total_items = Sum('quantity'))
        total_amount = cart_product_list_objects.aggregate(total_amount = Sum('product__latest_price'))
        saved_amount = cart_product_list_objects.aggregate(total_saved_amount = Sum('saved_amount'))
        
        cookies_cart_prodcut_list = None

    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except KeyError:
            cart = None
        if cart:
            for i in cart:
                product = Product.objects.get(id=i)
                total_price = (product.latest_price * int(cart[i]["quantity"]))
                order['cart_total_price'] += total_price
                order['cart_total_items'] += int(cart[i]["quantity"])
                if product.previous_price == 0:
                    pass
                else:
                    order['cart_saved_price'] += ((product.previous_price - product.latest_price) * int(cart[i]["quantity"]))
            cart_quantity_total = order['cart_total_items']
            cart_total_price = order['cart_total_price']
            product_queryset = Product.objects.filter(id__in=cart.keys())
            product_quantities = {int(k): v.get('quantity') for k, v in cart.items() if v is not None}
            cookies_cart_prodcut_list = product_queryset.annotate(quantity=Case(
                *[When(id=id, then=Value(quantity)) for id, quantity in product_quantities.items()],
                default=Value(0),
                output_field=IntegerField(),
            )).annotate(saved_amount = (F('previous_price') - F('latest_price'))*F('quantity'))
            items_total = cookies_cart_prodcut_list.aggregate(total_items = Sum('quantity'))
            total_amount = cookies_cart_prodcut_list.aggregate(total_amount = Sum('latest_price'))
            saved_amount = cookies_cart_prodcut_list.aggregate(total_saved_amount = Sum('saved_amount'))
            cart_product_list_objects = None
           
        else:
            cart_quantity_total = None
            cart_total_price = None
            cart_product_list_objects = None
            cookies_cart_prodcut_list = None
            items_total = {'total_items': '0'}
            total_amount = {'total_amount': '0'}
            saved_amount = {'total_saved_amount': '0'}

    context = {
        'cart_quantity_total': cart_quantity_total,
        'cart_total_price': cart_total_price,
        'cart_product_list': cart_product_list_objects,
        'json_data': nav_bar_json_data,
        'cookies_cart_prodcut_list': cookies_cart_prodcut_list,
        'total_amount': total_amount['total_amount'],
        'saved_amount': saved_amount['total_saved_amount'],
        'items_total': items_total['total_items'],
        'current_user': request.user,

    }
    return render(request, 'client_page/checkout.html',context)



# function for handling user sigup
def client_sign_up(request):
    email_exists = False
    if request.method == 'GET':
        sign_in_form = LoginForm()
        context = {'sign_in_form': sign_in_form}
        return render(request, 'app/sign_up_sign_in.html', context)
    if request.method == 'POST':

        # get credentials from the user
        username = request.POST.get("_username")
        email = request.POST.get("_email")
        c_password = request.POST.get("_cpassword")
        n_password = request.POST.get("_npassword")
        checkbox = request.POST.get("_checkbox")

        # if user accept the terms and conditions
        if checkbox:
            admin_all = User.objects.all()

            # check if the email is already in use in other account
            for items in admin_all:

                if items.email == email:
                    email_exists = True
                    break
                else:
                    email_exists = False

            # if the email is already in use show the message to the user
            if email_exists:
                messages.warning(request, 'Email already exists!')

                sign_in_form = LoginForm()
                context = {'sign_in_form': sign_in_form}
                return render(request, 'app/sign_up_sign_in.html', context)

            # if the email authorized by the system for new account
            else:

                # check if the password matches
                if n_password == c_password:
                    try:
                        new_user = User(username=username, email=email, is_superuser=0, is_staff=0)
                        new_user.set_password(c_password)
                        # new_profile = Profile(user=new_user)
                        new_user.save()
                        # new_profile.save()

                        messages.success(request, 'Please LogIn !')
                        sign_in_form = LoginForm()
                        context = {'sign_in_form': sign_in_form}
                        return render(request, 'app/sign_up_sign_in.html', context)

                    except Exception as e:
                        print(e)
                        messages.error(request, 'Username exists!')
                        sign_in_form = LoginForm()
                        context = {'sign_in_form': sign_in_form}
                        return render(request, 'app/sign_up_sign_in.html', context)
                else:
                    messages.error(request, 'password does not match!')
                    sign_in_form = LoginForm()
                    context = {'sign_in_form': sign_in_form}
                    return render(request, 'app/sign_up_sign_in.html', context)
    
    


# user authentication handling process
def client_sign_in(request):
    if request.method == 'GET':
        sign_in_form = LoginForm()
        context = {'sign_in_form': sign_in_form}
        return render(request, 'app/sign_up_sign_in.html', context)
    
    if request.method == 'POST':
        # get email, password and remember_me options from the user
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        # check if the user email is registered
        user = User.objects.filter(email=email).last()
        if user is not None:

            # check if user is client and password matches
            if check_password(password, user.password):

                # if user credentials matches add session to the user
                login(request, user)
                # save cart item to db and delete cart form cookie
                cookie_cart_loging(request, request.user)
                return redirect('index_app')
            
            else:
                # given password does not match or the account is not client privilege
                messages.warning(request, 'Access Denied!')
                sign_in_form = LoginForm()
                context = {'sign_in_form': sign_in_form}
                return render(request, 'app/sign_up_sign_in.html', context)
        else:
            # given email is not registered
            messages.warning(request, 'Wrong credentials!')
            sign_in_form = LoginForm()
            context = {'sign_in_form': sign_in_form}
            return render(request, 'app/sign_up_sign_in.html', context)
    

  

# log-out functionality that release the session of the current user
def logged_out(request):
    logout(request)
    return redirect('index_app')
 


#adding and update cart list to database
def update_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated :
            current_user = request.user
            data = json.loads(request.body)
            product_id = data['productId']
            action = data['action']

            if action == 'add':

                cart_add_query = Cart.objects.filter(user=current_user, product_id=product_id).last()
                if cart_add_query:
                    cart_add_query.quantity += 1
                    cart_add_query.save()
                    return JsonResponse({'_actr': 'True'})
                else:
                    new_cart_query = Cart(user=current_user, product_id=product_id)
                    new_cart_query.save()
                    return JsonResponse({'_actr': 'True'})

            elif action == 'update':
                quantity = data['quantity']

                cart_add_query = Cart.objects.filter(user=current_user, product_id=product_id).last()
                if cart_add_query:
                    cart_add_query.quantity = int(quantity)
                    cart_add_query.save()
                    return JsonResponse({'_actr': 'True'})


# add wishlist if user is logged-in
def update_wishlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['productId']
        wishlist_query = Wishlist.objects.get(product_id=product_id, user=request.user)
        wishlist_query.delete()

        return JsonResponse({'_actr': 'True'})
    

# adding wishlist from per page
def add_wishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)

            product_id = data['productId']

            wishlist_query = Wishlist.objects.filter(product_id=product_id, user=request.user,
                                                     ).last()

            if wishlist_query:
                wishlist_query.delete()
                return JsonResponse({'_actr': 'True'})
            else:
                Wishlist.objects.create(product_id=product_id, user=request.user)
                return JsonResponse({'_actr': 'True'})
        else:
            return JsonResponse({'_actr': 'False'})



#post a review in product description page 
def product_review(request):
    if not request.user.is_authenticated:
        return redirect('client_sign_in')  
    if request.method == 'POST':
        logged_in_user = request.user
        full_name = logged_in_user.username
        rating = request.POST.get('rate')
        review = request.POST.get('_review_box')
        product_id = request.POST.get('product_id')

        if rating:
            star = rating
        else:
            star = 2
        product_object = Product.objects.get(id=product_id)
        order_status = Order.objects.filter(user=logged_in_user,product= product_object, delivered = False).exists()
        if order_status:
            print('order status is true')
            if ProductReview.objects.filter(user=logged_in_user, product=product_object).exists():
                print('review already exists')
                ProductReview.objects.filter(user=logged_in_user, product=product_object).update(rating=star, review=review)
            else:
                ProductReview.objects.create(user = logged_in_user, product = product_object,rating=star,fullname=full_name, review=review)
            messages.success(request, 'Thanks for The Feedback!')
        else:
            messages.warning(request, 'You can not review this product because you have not bought it yet!')
        url = '/' + str(product_object.categories.slug) + '/' + str(product_id)
        print(url)
        return redirect(url)


#endregion




#region old code 


def cookie_cart(request):
    # get cart cookie value
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    # initial the order value from the cart
    order = {'cart_total_price': 0, 'cart_total_items': 0, 'cart_saved_price': 0}

    for items in cart:

        if items == 'Laptops':

            # if the cart has laptops data run this function to calculate price and count items

            for i in cart[items]:
                product = LaptopProducts.objects.get(id=i)
                total_price = (product.latest_price * int(cart[items][i]["quantity"]))
                order['cart_total_price'] += total_price
                order['cart_total_items'] += int(cart[items][i]["quantity"])
                if product.old_price == 0:
                    pass
                else:
                    order['cart_saved_price'] += (
                            (product.old_price - product.latest_price) * int(cart[items][i]["quantity"]))

        elif items == 'Desktops':

            # if the cart has Desktops data run this function to calculate price and count items

            for i in cart[items]:
                product = DesktopsProducts.objects.get(id=i)
                total_price = (product.latest_price * int(cart[items][i]["quantity"]))
                order['cart_total_price'] += total_price
                order['cart_total_items'] += int(cart[items][i]["quantity"])
                if product.old_price == 0:
                    pass
                else:
                    order['cart_saved_price'] += (
                            (product.old_price - product.latest_price) * int(cart[items][i]["quantity"]))

        elif items == 'Apple':

            # if the cart has Apple data run this function to calculate price and count items

            for i in cart[items]:
                product = AppleProducts.objects.get(id=i)
                total_price = (product.latest_price * int(cart[items][i]["quantity"]))
                order['cart_total_price'] += total_price
                order['cart_total_items'] += int(cart[items][i]["quantity"])
                if product.old_price == 0:
                    pass
                else:
                    order['cart_saved_price'] += (
                            (product.old_price - product.latest_price) * int(cart[items][i]["quantity"]))

        elif items == 'Components':

            # if the cart has Components data run this function to calculate price and count items

            for i in cart[items]:
                product = ComponentsProducts.objects.get(id=i)
                total_price = (product.latest_price * int(cart[items][i]["quantity"]))
                order['cart_total_price'] += total_price
                order['cart_total_items'] += int(cart[items][i]["quantity"])
                if product.old_price == 0:
                    pass
                else:
                    order['cart_saved_price'] += (
                            (product.old_price - product.latest_price) * int(cart[items][i]["quantity"]))

    return order

# if user is logged-in show cartoonist data in shopping cart
def user_saved_cart(request, _current_user):
    order = {'cart_total_price': 0, 'cart_total_items': 0, 'cart_saved_price': 0}

    cart_list = Cart.objects.filter(user=_current_user).all()

    for items in cart_list:

        if items.products_type == 'Laptops':

            # if the cart has Laptops data run this function to calculate price and count items

            product = LaptopProducts.objects.get(id=items.product_id)
            total_price = (product.latest_price * items.quantity)
            order['cart_total_price'] += total_price
            order['cart_total_items'] += items.quantity
            if product.old_price == 0:
                pass
            else:
                order['cart_saved_price'] += ((product.old_price - product.latest_price) * items.quantity)

        if items.products_type == 'Desktops':
            # if the cart has Desktops data run this function to calculate price and count items

            product = DesktopsProducts.objects.get(id=items.product_id)
            total_price = (product.latest_price * items.quantity)
            order['cart_total_price'] += total_price
            order['cart_total_items'] += items.quantity
            if product.old_price == 0:
                pass
            else:
                order['cart_saved_price'] += ((product.old_price - product.latest_price) * items.quantity)

        if items.products_type == 'Apple':
            # if the cart has Apple data run this function to calculate price and count items

            product = AppleProducts.objects.get(id=items.product_id)
            total_price = (product.latest_price * items.quantity)
            order['cart_total_price'] += total_price
            order['cart_total_items'] += items.quantity
            if product.old_price == 0:
                pass
            else:
                order['cart_saved_price'] += ((product.old_price - product.latest_price) * items.quantity)

        if items.products_type == 'Components':
            # if the cart has Apple data run this function to calculate price and count items

            product = ComponentsProducts.objects.get(id=items.product_id)
            total_price = (product.latest_price * items.quantity)
            order['cart_total_price'] += total_price
            order['cart_total_items'] += items.quantity
            if product.old_price == 0:
                pass
            else:

                order['cart_saved_price'] += ((product.old_price - product.latest_price) * items.quantity)

    return order


def blog_page(request):
    # returns all the blog
    blog_list = Blogs.objects.all().order_by('-id')

    # find brands that are in laptops to show in top-bar
    laptop_topnav = SubCategory.objects.filter(categories='Laptops')
    laptop_brand_id = topbar_laptops()

    laptop_brand = []
    for item in laptop_brand_id:
        laptop_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in desktops to show in top-bar
    desktop_topnav = SubCategory.objects.filter(categories='Desktops')
    desktop_brand_id = topbar_desktops()

    desktop_brand = []
    for item in desktop_brand_id:
        desktop_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in apple to show in top-bar
    apple_topnav = SubCategory.objects.filter(categories='Apple')
    apple_brand_id = topbar_apple()

    apple_brand = []
    for item in apple_brand_id:
        apple_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in components to show in top-bar
    components_topnav = SubCategory.objects.filter(categories='Components')
    components_brand_id = topbar_components()

    components_brand = []
    for item in components_brand_id:
        components_brand.append(Brands.objects.filter(id=item).last())

    if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
        order_cart_cookie = user_saved_cart(request, request.user)

        # get current user
        current_user = request.user

        # variable to know when to del cart after logged-in right-now is set to true meaning save and del cookie cart
        _cart_selection = '_tr_del_g'

    else:
        order_cart_cookie = cookie_cart(request)

        # no current user indication
        current_user = []

        # variable indicating server to pass the deletion of cart
        _cart_selection = '_fl_del_g'

    paginator_blog_list = Paginator(blog_list, 10)
    page_number_blog_list = request.GET.get('page_blog')
    try:
        page_obj_blog_list = paginator_blog_list.page(page_number_blog_list)
    except PageNotAnInteger:
        page_obj_blog_list = paginator_blog_list.page(1)
    except EmptyPage:
        page_obj_blog_list = paginator_blog_list.page(paginator_blog_list.num_pages)

    context = {'blog_list': page_obj_blog_list, 'cart_quantity_total': order_cart_cookie['cart_total_items'],
               'cart_total_price': order_cart_cookie['cart_total_price'], 'current_user': current_user,
               'laptop_topnav': laptop_topnav,
               'desktop_topnav': desktop_topnav, 'apple_topnav': apple_topnav, 'components_topnav': components_topnav,
               'laptop_brand': laptop_brand, 'desktop_brand': desktop_brand, 'apple_brand': apple_brand,
               'components_brand': components_brand, 'cart_selection': _cart_selection, }
    return render(request, 'client_page/index_blogList.html', context)


def per_blog_page(request, ids):
    # query get relevent blog
    per_blog_query = Blogs.objects.get(id=ids)

    # find brands that are in laptops to show in top-bar
    laptop_topnav = SubCategory.objects.filter(categories='Laptops')
    laptop_brand_id = topbar_laptops()

    laptop_brand = []
    for item in laptop_brand_id:
        laptop_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in desktops to show in top-bar
    desktop_topnav = SubCategory.objects.filter(categories='Desktops')
    desktop_brand_id = topbar_desktops()

    desktop_brand = []
    for item in desktop_brand_id:
        desktop_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in apple to show in top-bar
    apple_topnav = SubCategory.objects.filter(categories='Apple')
    apple_brand_id = topbar_apple()

    apple_brand = []
    for item in apple_brand_id:
        apple_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in components to show in top-bar
    components_topnav = SubCategory.objects.filter(categories='Components')
    components_brand_id = topbar_components()

    components_brand = []
    for item in components_brand_id:
        components_brand.append(Brands.objects.filter(id=item).last())

    if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
        order_cart_cookie = user_saved_cart(request, request.user)

        # get current user
        current_user = request.user

        # variable to know when to del cart after logged-in right-now is set to true meaning save and del cookie cart
        _cart_selection = '_tr_del_g'

    else:
        order_cart_cookie = cookie_cart(request)

        # no current user indication
        current_user = []

        # variable indicating server to pass the deletion of cart
        _cart_selection = '_fl_del_g'

    context = {'per_blog_query': per_blog_query, 'cart_quantity_total': order_cart_cookie['cart_total_items'],
               'cart_total_price': order_cart_cookie['cart_total_price'], 'current_user': current_user,
               'laptop_topnav': laptop_topnav,
               'desktop_topnav': desktop_topnav, 'apple_topnav': apple_topnav, 'components_topnav': components_topnav,
               'laptop_brand': laptop_brand, 'desktop_brand': desktop_brand, 'apple_brand': apple_brand,
               'components_brand': components_brand, 'cart_selection': _cart_selection, }
    return render(request, 'client_page/index_blog.html', context)


def blog_search(request):
    if request.method == 'POST' or request.method == 'GET':
        if request.method == 'POST':
            search_name = request.POST.get('_search_blog_text')
            if search_name == '\\':
                search_name = ''
        else:
            search_name = request.GET.get('search_blog')

        blog_list = Blogs.objects.all().order_by('-id')

        # search based title search, description
        blog_query_search = Blogs.objects.filter(
            Q(title__icontains=search_name) | Q(blog_summary__icontains=search_name))

        paginator_blog_search_list = Paginator(blog_query_search, 10)
        page_number_blog_search_list = request.GET.get('page_search_blog')
        try:
            page_obj_blog_search_list = paginator_blog_search_list.page(page_number_blog_search_list)
        except PageNotAnInteger:
            page_obj_blog_search_list = paginator_blog_search_list.page(1)
        except EmptyPage:
            page_obj_blog_search_list = paginator_blog_search_list.page(paginator_blog_search_list.num_pages)

        # find brands that are in laptops to show in top-bar
        laptop_topnav = SubCategory.objects.filter(categories='Laptops')
        laptop_brand_id = topbar_laptops()

        laptop_brand = []
        for item in laptop_brand_id:
            laptop_brand.append(Brands.objects.filter(id=item).last())

        # find brands that are in desktops to show in top-bar
        desktop_topnav = SubCategory.objects.filter(categories='Desktops')
        desktop_brand_id = topbar_desktops()

        desktop_brand = []
        for item in desktop_brand_id:
            desktop_brand.append(Brands.objects.filter(id=item).last())

        # find brands that are in apple to show in top-bar
        apple_topnav = SubCategory.objects.filter(categories='Apple')
        apple_brand_id = topbar_apple()

        apple_brand = []
        for item in apple_brand_id:
            apple_brand.append(Brands.objects.filter(id=item).last())

        # find brands that are in components to show in top-bar
        components_topnav = SubCategory.objects.filter(categories='Components')
        components_brand_id = topbar_components()

        components_brand = []
        for item in components_brand_id:
            components_brand.append(Brands.objects.filter(id=item).last())

        if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
            order_cart_cookie = user_saved_cart(request, request.user)

            # get current user
            current_user = request.user

            # variable to know when to del cart after logged-in right-now is set to true meaning save and del cookie
            # cart
            _cart_selection = '_tr_del_g'

        else:
            order_cart_cookie = cookie_cart(request)

            # no current user indication
            current_user = []

            # variable indicating server to pass the deletion of cart
            _cart_selection = '_fl_del_g'

        context = {'cart_quantity_total': order_cart_cookie['cart_total_items'],
                   'cart_total_price': order_cart_cookie['cart_total_price'], 'current_user': current_user,
                   'laptop_topnav': laptop_topnav, 'page_obj_blog_search_list': page_obj_blog_search_list,
                   'desktop_topnav': desktop_topnav, 'apple_topnav': apple_topnav, 'blog_list': blog_list,
                   'components_topnav': components_topnav, 'search_name': search_name,
                   'laptop_brand': laptop_brand, 'desktop_brand': desktop_brand, 'apple_brand': apple_brand,
                   'components_brand': components_brand, 'cart_selection': _cart_selection, }
        return render(request, 'client_page/blog/search.html', context)


# list_page of the components
def list_page(request, _product):
    # find brands that are in laptops to show in top-bar
    laptop_topnav = SubCategory.objects.filter(categories='Laptops')
    laptop_brand_id = topbar_laptops()

    laptop_brand = []
    for item in laptop_brand_id:
        laptop_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in desktops to show in top-bar
    desktop_topnav = SubCategory.objects.filter(categories='Desktops')
    desktop_brand_id = topbar_desktops()

    desktop_brand = []
    for item in desktop_brand_id:
        desktop_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in apple to show in top-bar
    apple_topnav = SubCategory.objects.filter(categories='Apple')
    apple_brand_id = topbar_apple()

    apple_brand = []
    for item in apple_brand_id:
        apple_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in components to show in top-bar
    components_topnav = SubCategory.objects.filter(categories='Components')
    components_brand_id = topbar_components()

    components_brand = []
    for item in components_brand_id:
        components_brand.append(Brands.objects.filter(id=item).last())

    # required data for the shopping cart tab if user is logged-in
    if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:

        order_cart_cookie = user_saved_cart(request, request.user)
        current_user = request.user
    else:

        order_cart_cookie = cookie_cart(request)
        current_user = []

    # if the list_page is for laptops components this function is executed
    if _product == 'Laptops':
        photo_list = []
        user_wishlist_mark = []

        # get total laptop items
        laptop_list = LaptopProducts.objects.all()

        # get the min and max value of the total laptops
        product_max_min = LaptopProducts.objects.aggregate(Max('latest_price'), Min('latest_price'))
        min_price = product_max_min['latest_price__min']
        max_price = product_max_min['latest_price__max']

        # dynamic filtering with the queryset as the total laptop items
        snippet_filter = SnippetFilterLaptop(request.GET, queryset=laptop_list)

        # get the value from user for displaying required items per page
        show_by_number = request.GET.get('show_by')

        # default value is 12 , user can choose between 12, 24, 36 items per page
        if show_by_number is not None:
            if show_by_number:
                paginated_filtered = Paginator(snippet_filter.qs, int(show_by_number))
            else:
                paginated_filtered = Paginator(snippet_filter.qs, 12)
        else:
            paginated_filtered = Paginator(snippet_filter.qs, 12)

        # pagination
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)

        # to mark wishlist if user is authenticated and item is in wishlist
        for items in page_obj:
            if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
                wishlist_query_laptop = Wishlist.objects.filter(product_id=items.id, products_type='Laptops',
                                                                user=current_user).last()
                if wishlist_query_laptop:
                    user_wishlist_mark.append('True')
                else:
                    user_wishlist_mark.append('False')
            else:
                user_wishlist_mark.append('False')

        # to show image with product in list page
        for item in page_obj:
            photo_list.append(ProductsImage.objects.filter(product_id=item.id, products_type=_product).last())

        # bundling object with its corresponding image
        zip_pro_img = zip(page_obj, photo_list, user_wishlist_mark)

        context = {'laptop_list': laptop_list,
                   'min_price': min_price, 'max_price': max_price,
                   'snippet_filter': snippet_filter, 'cart_quantity_total': order_cart_cookie['cart_total_items'],
                   'cart_total_price': order_cart_cookie['cart_total_price'], 'paginated_filtered': paginated_filtered,
                   'page_obj': page_obj, 'zip_pro_img': zip_pro_img, 'photo_list': photo_list, 'product': _product,
                   'current_user': current_user, 'laptop_topnav': laptop_topnav,
                   'laptop_brand': laptop_brand, 'desktop_topnav': desktop_topnav, 'desktop_brand': desktop_brand,
                   'apple_topnav': apple_topnav, 'apple_brand': apple_brand, 'components_topnav': components_topnav,
                   'components_brand': components_brand}
        return render(request, 'client_page/list_product.html', context)

    # if the list_page is for laptops components this function is executed
    elif _product == 'Desktops':

        photo_list = []
        user_wishlist_mark = []

        # get total desktops items
        laptop_list = DesktopsProducts.objects.all()

        # get the min and max value of the total desktops
        product_max_min = DesktopsProducts.objects.aggregate(Max('latest_price'), Min('latest_price'))
        min_price = product_max_min['latest_price__min']
        max_price = product_max_min['latest_price__max']

        # dynamic filtering with the queryset as the total desktops items
        snippet_filter = SnippetFilterDesktop(request.GET, queryset=laptop_list)
        laptop_list = snippet_filter.qs

        # get the value from user for displaying required items per page
        show_by_number = request.GET.get('show_by')

        # default value is 12 , user can choose between 12, 24, 36 items per page
        if show_by_number is not None:
            if show_by_number:
                paginated_filtered = Paginator(laptop_list, int(show_by_number))
            else:
                paginated_filtered = Paginator(laptop_list, 12)
        else:
            paginated_filtered = Paginator(laptop_list, 12)

        # pagination
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)

        # to mark wishlist if user is authenticated and item is in wishlist
        for items in page_obj:
            if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
                wishlist_query_desktops = Wishlist.objects.filter(product_id=items.id, products_type='Desktops',
                                                                  user=current_user).last()
                if wishlist_query_desktops:
                    user_wishlist_mark.append('True')
                else:
                    user_wishlist_mark.append('False')
            else:
                user_wishlist_mark.append('False')

        # to show image with product in list page
        for item in page_obj:
            photo_list.append(ProductsImage.objects.filter(product_id=item.id, products_type=_product).last())

        # bundling object with its corresponding image
        zip_pro_img = zip(page_obj, photo_list, user_wishlist_mark)
        context = {'laptop_list': laptop_list,
                   'min_price': min_price, 'max_price': max_price,
                   'snippet_filter': snippet_filter, 'cart_quantity_total': order_cart_cookie['cart_total_items'],
                   'cart_total_price': order_cart_cookie['cart_total_price'], 'paginated_filtered': paginated_filtered,
                   'page_obj': page_obj, 'zip_pro_img': zip_pro_img, 'product': _product, 'current_user': current_user,
                   'laptop_topnav': laptop_topnav,
                   'laptop_brand': laptop_brand, 'desktop_topnav': desktop_topnav, 'desktop_brand': desktop_brand,
                   'apple_topnav': apple_topnav, 'apple_brand': apple_brand, 'components_topnav': components_topnav,
                   'components_brand': components_brand
                   }
        return render(request, 'client_page/list_product.html', context)

    # if the list_page is for laptops components this function is executed
    elif _product == 'Apple':

        photo_list = []
        user_wishlist_mark = []

        # get total Apple items
        laptop_list = AppleProducts.objects.all()

        # get the min and max value of the total Apple
        product_max_min = AppleProducts.objects.aggregate(Max('latest_price'), Min('latest_price'))
        min_price = product_max_min['latest_price__min']
        max_price = product_max_min['latest_price__max']

        # dynamic filtering with the queryset as the total Apple items
        snippet_filter = SnippetFilterApple(request.GET, queryset=laptop_list)
        laptop_list = snippet_filter.qs

        # get the value from user for displaying required items per page
        show_by_number = request.GET.get('show_by')

        # default value is 12 , user can choose between 12, 24, 36 items per page
        if show_by_number is not None:
            if show_by_number:
                paginated_filtered = Paginator(laptop_list, int(show_by_number))
            else:
                paginated_filtered = Paginator(laptop_list, 12)
        else:
            paginated_filtered = Paginator(laptop_list, 12)

        # pagination
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)

        # to mark wishlist if user is authenticated and item is in wishlist
        for items in page_obj:
            if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
                wishlist_query_apple = Wishlist.objects.filter(product_id=items.id, products_type='Apple',
                                                               user=current_user).last()
                if wishlist_query_apple:
                    user_wishlist_mark.append('True')
                else:
                    user_wishlist_mark.append('False')
            else:
                user_wishlist_mark.append('False')

        # to show image with product in list page
        for item in page_obj:
            photo_list.append(ProductsImage.objects.filter(product_id=item.id, products_type=_product).last())

        # bundling object with its corresponding image
        zip_pro_img = zip(page_obj, photo_list, user_wishlist_mark)

        context = {'laptop_list': laptop_list,
                   'min_price': min_price, 'max_price': max_price,
                   'snippet_filter': snippet_filter, 'cart_quantity_total': order_cart_cookie['cart_total_items'],
                   'cart_total_price': order_cart_cookie['cart_total_price'], 'paginated_filtered': paginated_filtered,
                   'page_obj': page_obj, 'zip_pro_img': zip_pro_img, 'product': _product, 'current_user': current_user,
                   'laptop_topnav': laptop_topnav,
                   'laptop_brand': laptop_brand, 'desktop_topnav': desktop_topnav, 'desktop_brand': desktop_brand,
                   'apple_topnav': apple_topnav, 'apple_brand': apple_brand, 'components_topnav': components_topnav,
                   'components_brand': components_brand
                   }
        return render(request, 'client_page/list_product.html', context)

    # if the list_page is for laptops components this function is executed
    elif _product == 'Components':

        photo_list = []
        user_wishlist_mark = []

        # get total Components items
        laptop_list = ComponentsProducts.objects.all()

        # get the min and max value of the total Components
        product_max_min = ComponentsProducts.objects.aggregate(Max('latest_price'), Min('latest_price'))
        min_price = product_max_min['latest_price__min']
        max_price = product_max_min['latest_price__max']

        snippet_filter = SnippetFilterComponents(request.GET, queryset=laptop_list)

        # dynamic filtering with the queryset as the total Components items
        laptop_list = snippet_filter.qs
        show_by_number = request.GET.get('show_by')

        # get the value from user for displaying required items per page
        if show_by_number is not None:
            if show_by_number:
                paginated_filtered = Paginator(laptop_list, int(show_by_number))
            else:
                paginated_filtered = Paginator(laptop_list, 12)
        else:
            paginated_filtered = Paginator(laptop_list, 12)

        # pagination
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)

        # to mark wishlist if user is authenticated and item is in wishlist
        for items in page_obj:
            if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
                wishlist_query_components = Wishlist.objects.filter(product_id=items.id, products_type='Components',
                                                                    user=current_user).last()
                if wishlist_query_components:
                    user_wishlist_mark.append('True')
                else:
                    user_wishlist_mark.append('False')
            else:
                user_wishlist_mark.append('False')

        # to show image with product in list page
        for item in page_obj:
            photo_list.append(ProductsImage.objects.filter(product_id=item.id, products_type=_product).last())

        # bundling object with its corresponding image
        zip_pro_img = zip(page_obj, photo_list, user_wishlist_mark)

        context = {'laptop_list': laptop_list,
                   'min_price': min_price, 'max_price': max_price,
                   'snippet_filter': snippet_filter, 'cart_quantity_total': order_cart_cookie['cart_total_items'],
                   'cart_total_price': order_cart_cookie['cart_total_price'], 'paginated_filtered': paginated_filtered,
                   'page_obj': page_obj, 'zip_pro_img': zip_pro_img, 'product': _product, 'current_user': current_user,
                   'laptop_topnav': laptop_topnav,
                   'laptop_brand': laptop_brand, 'desktop_topnav': desktop_topnav, 'desktop_brand': desktop_brand,
                   'apple_topnav': apple_topnav, 'apple_brand': apple_brand, 'components_topnav': components_topnav,
                   'components_brand': components_brand
                   }
        return render(request, 'client_page/list_product.html', context)

#minecode 


# function executing for per item page
def per_page(request, _product, ids):
    # find brands that are in laptops to show in top-bar
    laptop_topnav = SubCategory.objects.filter(categories='Laptops')
    laptop_brand_id = topbar_laptops()

    laptop_brand = []
    for item in laptop_brand_id:
        laptop_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in desktops to show in top-bar
    desktop_topnav = SubCategory.objects.filter(categories='Desktops')
    desktop_brand_id = topbar_desktops()

    desktop_brand = []
    for item in desktop_brand_id:
        desktop_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in apple to show in top-bar
    apple_topnav = SubCategory.objects.filter(categories='Apple')
    apple_brand_id = topbar_apple()

    apple_brand = []
    for item in apple_brand_id:
        apple_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in components to show in top-bar
    components_topnav = SubCategory.objects.filter(categories='Components')
    components_brand_id = topbar_components()

    components_brand = []
    for item in components_brand_id:
        components_brand.append(Brands.objects.filter(id=item).last())

    if _product == 'Laptops':

        # item object query
        per_product = LaptopProducts.objects.filter(id=ids).last()

        # get images of corresponding item
        per_images = ProductsImage.objects.filter(product_id=ids, products_type=_product).all()

        # get images of corresponding item
        meta_images = ProductsImage.objects.filter(product_id=ids, products_type=_product).last()

        # get corresponding specification of the item
        per_desc = ProductSpecification.objects.filter(product_id=ids, products_type=_product)

        # get list of reviews from the user
        review_list = ProductReview.objects.filter(categories=_product, product_id=ids).order_by('-id')

    elif _product == 'Desktops':

        # item object query
        per_product = DesktopsProducts.objects.filter(id=ids).last()

        # get images of corresponding item
        per_images = ProductsImage.objects.filter(product_id=ids, products_type=_product).all()

        # get images of corresponding item
        meta_images = ProductsImage.objects.filter(product_id=ids, products_type=_product).last()

        # get corresponding specification of the item
        per_desc = ProductSpecification.objects.filter(product_id=ids, products_type=_product)

        # get list of reviews from the user
        review_list = ProductReview.objects.filter(categories=_product, product_id=ids).order_by('-id')

    elif _product == 'Apple':

        # item object query
        per_product = AppleProducts.objects.filter(id=ids).last()

        # get images of corresponding item
        per_images = ProductsImage.objects.filter(product_id=ids, products_type=_product).all()

        # get images of corresponding item
        meta_images = ProductsImage.objects.filter(product_id=ids, products_type=_product).last()

        # get corresponding specification of the item
        per_desc = ProductSpecification.objects.filter(product_id=ids, products_type=_product)

        # get list of reviews from the user
        review_list = ProductReview.objects.filter(categories=_product, product_id=ids).order_by('-id')

    elif _product == 'Components':

        # item object query
        per_product = ComponentsProducts.objects.filter(id=ids).last()

        # get images of corresponding item
        per_images = ProductsImage.objects.filter(product_id=ids, products_type=_product).all()

        # get images of corresponding item
        meta_images = ProductsImage.objects.filter(product_id=ids, products_type=_product).last()

        # get corresponding specification of the item
        per_desc = ProductSpecification.objects.filter(product_id=ids, products_type=_product)

        # get list of reviews from the user
        review_list = ProductReview.objects.filter(categories=_product, product_id=ids).order_by('-id')

    else:
        per_product = []
        per_images = []
        per_desc = []
        meta_images = []
        review_list = []

    # required data for the shopping cart tab if user is logged-in
    if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
        order_cart_cookie = user_saved_cart(request, request.user)
        current_user = request.user
    else:
        order_cart_cookie = cookie_cart(request)
        current_user = []



    context = {'cart_quantity_total': order_cart_cookie['cart_total_items'],
               'cart_total_price': order_cart_cookie['cart_total_price'], 
               'per_product': per_product,
               'per_images': per_images, 
               'per_desc': per_desc, 
               'current_user': current_user,
               'laptop_topnav': laptop_topnav, 
               'review_list': review_list,
               'laptop_brand': laptop_brand, 
               'desktop_topnav': desktop_topnav, 
               'desktop_brand': desktop_brand,
               'apple_topnav': apple_topnav, 
               'apple_brand': apple_brand, 
               'components_topnav': components_topnav,
               'components_brand': components_brand, 
               'meta_images': meta_images}
    return render(request, 'client_page/perPage/product_des.html', context)

# add to cart function used in home page which return jsonresponse
## markdown important


# user logging function
def client_authentication(request):
    # find brands that are in laptops to show in top-bar
    laptop_topnav = SubCategory.objects.filter(categories='Laptops')
    laptop_brand_id = topbar_laptops()

    laptop_brand = []
    for item in laptop_brand_id:
        laptop_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in desktops to show in top-bar
    desktop_topnav = SubCategory.objects.filter(categories='Desktops')
    desktop_brand_id = topbar_desktops()

    desktop_brand = []
    for item in desktop_brand_id:
        desktop_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in apple to show in top-bar
    apple_topnav = SubCategory.objects.filter(categories='Apple')
    apple_brand_id = topbar_apple()

    apple_brand = []
    for item in apple_brand_id:
        apple_brand.append(Brands.objects.filter(id=item).last())

    # find brands that are in components to show in top-bar
    components_topnav = SubCategory.objects.filter(categories='Components')
    components_brand_id = topbar_components()

    components_brand = []
    for item in components_brand_id:
        components_brand.append(Brands.objects.filter(id=item).last())

    # check if user is logged-in or not
    if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:

        order_cart_cookie = user_saved_cart(request, request.user)
        current_user = request.user

        # display the orderlist, billing and delivery information, wishlist, cart_list of the user
        order_list = []
        per_order = Order.objects.filter(user=current_user)
        for items in per_order:
            if items.products_type == 'Laptops':

                order_list.append(
                    (LaptopProducts.objects.filter(id=items.product_id).last().title, items.quantity,
                     items.date_time))
            elif items.products_type == 'Desktops':
                order_list.append(
                    (DesktopsProducts.objects.filter(id=items.product_id).last().title, items.quantity,
                     items.date_time))

            elif items.products_type == 'Apple':
                order_list.append(
                    (AppleProducts.objects.filter(id=items.product_id).last().title, items.quantity,
                     items.date_time))

            elif items.products_type == 'Components':
                order_list.append((
                    ComponentsProducts.objects.filter(id=items.product_id).last().title, items.quantity,
                    items.date_time))

        order_obj = zip(order_list, per_order)

        billing_query = Billing.objects.filter(user=current_user).last()
        delivery_query = Delivery.objects.filter(user=current_user).last()
        wish_list = Wishlist.objects.filter(user=current_user).all()
        cart_list = Cart.objects.filter(user=current_user).all()

        cart_list_photo = []
        cart_list_title = []

        wish_list_photo = []
        wish_list_title = []

        for items in cart_list:
            if items.products_type == 'Laptops':
                cart_list_photo.append(
                    ProductsImage.objects.filter(product_id=items.product_id, products_type=items.products_type).last())
                cart_list_title.append(LaptopProducts.objects.filter(id=items.product_id).last())

            if items.products_type == 'Desktops':
                cart_list_photo.append(
                    ProductsImage.objects.filter(product_id=items.product_id, products_type=items.products_type).last())
                cart_list_title.append(DesktopsProducts.objects.filter(id=items.product_id).last())

            if items.products_type == 'Apple':
                cart_list_photo.append(
                    ProductsImage.objects.filter(product_id=items.product_id, products_type=items.products_type).last())
                cart_list_title.append(AppleProducts.objects.filter(id=items.product_id).last())

            if items.products_type == 'Components':
                cart_list_photo.append(
                    ProductsImage.objects.filter(product_id=items.product_id, products_type=items.products_type).last())
                cart_list_title.append(ComponentsProducts.objects.filter(id=items.product_id).last())

        cart_obj = zip(cart_list, cart_list_photo, cart_list_title)

        for items in wish_list:
            if items.products_type == 'Laptops':
                wish_list_photo.append(
                    ProductsImage.objects.filter(product_id=items.product_id, products_type=items.products_type).last())
                wish_list_title.append(LaptopProducts.objects.filter(id=items.product_id).last())

            if items.products_type == 'Desktops':
                wish_list_photo.append(
                    ProductsImage.objects.filter(product_id=items.product_id, products_type=items.products_type).last())
                wish_list_title.append(DesktopsProducts.objects.filter(id=items.product_id).last())

            if items.products_type == 'Apple':
                wish_list_photo.append(
                    ProductsImage.objects.filter(product_id=items.product_id, products_type=items.products_type).last())
                wish_list_title.append(AppleProducts.objects.filter(id=items.product_id).last())

            if items.products_type == 'Components':
                wish_list_photo.append(
                    ProductsImage.objects.filter(product_id=items.product_id, products_type=items.products_type).last())
                wish_list_title.append(ComponentsProducts.objects.filter(id=items.product_id).last())

        wish_obj = zip(wish_list, wish_list_photo, wish_list_title)

        context = {'cart_quantity_total': order_cart_cookie['cart_total_items'],
                   'cart_total_price': order_cart_cookie['cart_total_price'],
                   'current_user': current_user, 
                   'order_list': order_obj, 
                   'billing_query': billing_query,
                   'delivery_query': delivery_query, 'wish_obj': wish_obj, 'cart_obj': cart_obj,
                   'laptop_topnav': laptop_topnav, 'desktop_topnav': desktop_topnav, 'apple_topnav': apple_topnav,
                   'components_topnav': components_topnav, 'laptop_brand': laptop_brand, 'desktop_brand': desktop_brand,
                   'apple_brand': apple_brand, 'components_brand': components_brand}
        return render(request, 'client_page/userAccount/index_userAccount.html', context)

    else:

        # if user is not logged-in shows login, signup page
        sign_in_form = LoginForm()
        context = {'sign_in_form': sign_in_form}
        return render(request, 'client_page/userAccount/account_login.html', context)


# updating the orderlist of current user
def update_orderlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['productId']

        orderlist_query = Order.objects.get(id=product_id, user=request.user)
        orderlist_query.delete()
        return JsonResponse({'_actr': 'True'})


# updating the cartlist of current user
def update_cartlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
            data = json.loads(request.body)

            product_id = data['productId']

            wishlist_query = Cart.objects.get(product_id=product_id, user=request.user)
            wishlist_query.delete()
            return JsonResponse({'_actr': 'True'})


# function handling user changing their delivery and billing information
@login_required
def client_information_billing_post(request, ids):
    if request.method == 'POST':

        billing_firstname = request.POST.get('billing_firstname')
        billing_lastname = request.POST.get('billing_lastname')
        billing_company = request.POST.get('billing_company')
        billing_street = request.POST.get('billing_street')
        billing_town = request.POST.get('billing_town')
        billing_state = request.POST.get('billing_state')
        billing_zip = request.POST.get('billing_zip')
        billing_number = request.POST.get('billing_number')

        delivery_firstname = request.POST.get('delivery_firstname')
        delivery_lastname = request.POST.get('delivery_lastname')
        delivery_company = request.POST.get('delivery_company')
        delivery_street = request.POST.get('delivery_street')
        delivery_town = request.POST.get('delivery_town')
        delivery_state = request.POST.get('delivery_state')
        delivery_zip = request.POST.get('delivery_zip')
        delivery_number = request.POST.get('delivery_number')

        # get the current user credentials from db
        user_query = User.objects.filter(id=ids).last()
        if user_query:
            billing_query = Billing.objects.filter(user=user_query).last()
            delivery_query = Delivery.objects.filter(user=user_query).last()

            if billing_query:

                billing_query.first_name = billing_firstname
                billing_query.last_name = billing_lastname
                billing_query.company_name = billing_company
                billing_query.street_address = billing_street
                billing_query.town_city = billing_town
                billing_query.state = billing_state
                billing_query.zip = billing_zip
                billing_query.contact = billing_number
                billing_query.save()

            else:
                Billing.objects.create(first_name=billing_firstname, last_name=billing_lastname,
                                       company_name=billing_company,
                                       street_address=billing_street, town_city=billing_town, state=billing_state,
                                       zip=billing_zip,
                                       contact=billing_number, user=user_query)

            if delivery_query:

                delivery_query.first_name = delivery_firstname
                delivery_query.last_name = delivery_lastname
                delivery_query.company_name = delivery_company
                delivery_query.street_address = delivery_street
                delivery_query.town_city = delivery_town
                delivery_query.state = delivery_state
                delivery_query.zip = delivery_zip
                delivery_query.contact = delivery_number
                delivery_query.save()

            else:
                Delivery.objects.create(first_name=delivery_firstname, last_name=delivery_lastname,
                                        company_name=delivery_company,
                                        street_address=delivery_street, town_city=delivery_town, state=delivery_state,
                                        zip=delivery_zip,
                                        contact=delivery_number, user=user_query)

            messages.success(request, 'Information updated')
            return redirect('client_authentication_app')
        else:
            messages.error(request, 'User not recognized')
            return redirect('client_authentication_app')


# function handling user changing their name , email and password
@login_required
def client_information_account_post(request, ids):
    if request.method == 'POST':
        email_exists = False

        # get the user input first and last name
        account_first_name = request.POST.get('account_first_name')
        account_last_name = request.POST.get('account_last_name')

        # get the checkbox value for email changes
        chkBox2 = request.POST.get('chkBox2')

        account_old_email = request.POST.get('account_old_email')
        account_new_email = request.POST.get('account_new_email')

        # get the checkbox value for password changes
        chkBox = request.POST.get('chkBox')
        account_old_password = request.POST.get('account_old_password')
        account_new_password = request.POST.get('account_new_password')
        account_confirm_password = request.POST.get('account_confirm_password')

        # get current user objects from db
        user_query = User.objects.filter(id=ids).last()

        if user_query:

            # if user request to change email
            if chkBox2 is not None:

                if user_query.email == account_old_email:

                    admin_all = User.objects.all()
                    # check whether the new email is already in use
                    for items in admin_all:

                        if items.email == account_new_email:
                            email_exists = True
                            break
                        else:
                            email_exists = False

                    # if given new email is already in use show proper message to the user
                    if email_exists:
                        messages.error(request, 'User with this email is already in use')
                        return redirect('client_authentication_app')
                    else:

                        # if user request to change password
                        if chkBox is not None:

                            # error handling for the password
                            if account_new_password == account_confirm_password:
                                if check_password(account_old_password, user_query.password):
                                    user_query.first_name = account_first_name
                                    user_query.last_name = account_last_name
                                    user_query.email = account_new_email
                                    user_query.set_password(account_new_password)

                                    user_query.save()

                                    messages.success(request, 'User updated')
                                    return redirect('client_authentication_app')
                                else:
                                    messages.error(request, 'Current password does not match')
                                    return redirect('client_authentication_app')
                            else:
                                messages.error(request, 'New Password does not match')
                                return redirect('client_authentication_app')

                        else:
                            user_query.first_name = account_first_name
                            user_query.last_name = account_last_name
                            user_query.email = account_new_email

                            user_query.save()

                            messages.success(request, 'User updated')
                            return redirect('client_authentication_app')
            else:
                if chkBox is not None:
                    if account_new_password == account_confirm_password:
                        if check_password(account_old_password, user_query.password):
                            user_query.first_name = account_first_name
                            user_query.last_name = account_last_name
                            user_query.set_password(account_new_password)

                            user_query.save()

                            messages.success(request, 'User updated')
                            return redirect('client_authentication_app')
                        else:
                            messages.error(request, 'Current password does not match')
                            return redirect('client_authentication_app')
                    else:
                        messages.error(request, 'New Password does not match')
                        return redirect('client_authentication_app')
                else:
                    user_query.first_name = account_first_name
                    user_query.last_name = account_last_name

                    user_query.save()

                    messages.success(request, 'User updated')
                    return redirect('client_authentication_app')

        else:
            messages.error(request, 'User not recognized')
            return redirect('client_authentication_app')


# this function is used when search
def search_btns_post(request):
    if request.method == 'POST' or request.method == 'GET':
        if request.method == 'POST':
            search_name = request.POST.get('_search_text')
            if search_name == '\\':
                search_name = ''
        else:
            search_name = request.GET.get('search_name')

        queryset_list = []
        total_images = []

        # find brands that are in laptops to show in top-bar
        laptop_topnav = SubCategory.objects.filter(categories='Laptops')
        laptop_brand_id = topbar_laptops()

        laptop_brand = []
        for item in laptop_brand_id:
            laptop_brand.append(Brands.objects.filter(id=item).last())

        # find brands that are in desktops to show in top-bar
        desktop_topnav = SubCategory.objects.filter(categories='Desktops')
        desktop_brand_id = topbar_desktops()

        desktop_brand = []
        for item in desktop_brand_id:
            desktop_brand.append(Brands.objects.filter(id=item).last())

        # find brands that are in apple to show in top-bar
        apple_topnav = SubCategory.objects.filter(categories='Apple')
        apple_brand_id = topbar_apple()

        apple_brand = []
        for item in apple_brand_id:
            apple_brand.append(Brands.objects.filter(id=item).last())

        # find brands that are in components to show in top-bar
        components_topnav = SubCategory.objects.filter(categories='Components')
        components_brand_id = topbar_components()

        components_brand = []
        for item in components_brand_id:
            components_brand.append(Brands.objects.filter(id=item).last())

        # required value for topnav bar
        if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
            order_cart_cookie = user_saved_cart(request, request.user)

            # get current user
            current_user = request.user
        else:
            order_cart_cookie = cookie_cart(request)
            current_user = []

        if re.search(search_name.casefold(), 'laptop'):

            user_wishlist_mark_laptop = []

            laptop_query = LaptopProducts.objects.all()

            for items in laptop_query:
                total_images.append(
                    ProductsImage.objects.filter(product_id=items.id, products_type=items.categories).last())

            for items in laptop_query:
                if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
                    wishlist_query = Wishlist.objects.filter(user=request.user, product_id=items.id,
                                                             products_type=items.categories).last()
                    if wishlist_query:
                        user_wishlist_mark_laptop.append('True')
                    else:
                        user_wishlist_mark_laptop.append('False')
                else:
                    user_wishlist_mark_laptop.append('False')

            # pagination
            paginated_filtered = Paginator(laptop_query, 12)
            page_number = request.GET.get('pages')

            try:
                page_obj = paginated_filtered.page(page_number)
            except PageNotAnInteger:
                page_obj = paginated_filtered.page(1)
            except EmptyPage:
                page_obj = paginated_filtered.page(page_number.num_pages)

            object_bundle = zip(page_obj, total_images, user_wishlist_mark_laptop)

            context = {'object_bundle': object_bundle,
                       'laptop_brand': laptop_brand, 'desktop_brand': desktop_brand, 'apple_brand': apple_brand,
                       'components_brand': components_brand, 'laptop_topnav': laptop_topnav,
                       'desktop_topnav': desktop_topnav,
                       'apple_topnav': apple_topnav, 'components_topnav': components_topnav,
                       'current_user': current_user, 'cart_quantity_total': order_cart_cookie['cart_total_items'],
                       'cart_total_price': order_cart_cookie['cart_total_price'], 'page_obj': page_obj,
                       'search_name': search_name}

            return render(request, 'client_page/search/list_products.html', context)

        elif re.search(search_name.casefold(), 'desktop'):

            laptop_query = DesktopsProducts.objects.all()
            for items in laptop_query:
                total_images.append(
                    ProductsImage.objects.filter(product_id=items.id, products_type=items.categories).last())

            user_wishlist_mark_laptop = []
            for items in laptop_query:
                if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
                    wishlist_query = Wishlist.objects.filter(user=request.user, product_id=items.id,
                                                             products_type=items.categories).last()
                    if wishlist_query:
                        user_wishlist_mark_laptop.append('True')
                    else:
                        user_wishlist_mark_laptop.append('False')
                else:
                    user_wishlist_mark_laptop.append('False')

            # pagination
            paginated_filtered = Paginator(laptop_query, 12)
            page_number = request.GET.get('pages')
            try:
                page_obj = paginated_filtered.page(page_number)
            except PageNotAnInteger:
                page_obj = paginated_filtered.page(1)
            except EmptyPage:
                page_obj = paginated_filtered.page(page_number.num_pages)

            object_bundle = zip(page_obj, total_images, user_wishlist_mark_laptop)

            context = {'object_bundle': object_bundle,
                       'laptop_brand': laptop_brand, 'desktop_brand': desktop_brand, 'apple_brand': apple_brand,
                       'components_brand': components_brand, 'laptop_topnav': laptop_topnav,
                       'desktop_topnav': desktop_topnav,
                       'apple_topnav': apple_topnav, 'components_topnav': components_topnav,
                       'current_user': current_user, 'cart_quantity_total': order_cart_cookie['cart_total_items'],
                       'cart_total_price': order_cart_cookie['cart_total_price'], 'page_obj': page_obj,
                       'search_name': search_name
                       }

            return render(request, 'client_page/search/list_products.html', context)

        elif re.search(search_name.casefold(), 'apple'):
            laptop_query = AppleProducts.objects.all()
            for items in laptop_query:
                total_images.append(
                    ProductsImage.objects.filter(product_id=items.id, products_type=items.categories).last())

            user_wishlist_mark_laptop = []
            for items in laptop_query:
                if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
                    wishlist_query = Wishlist.objects.filter(user=request.user, product_id=items.id,
                                                             products_type=items.categories).last()
                    if wishlist_query:
                        user_wishlist_mark_laptop.append('True')
                    else:
                        user_wishlist_mark_laptop.append('False')
                else:
                    user_wishlist_mark_laptop.append('False')

            # pagination
            paginated_filtered = Paginator(laptop_query, 12)
            page_number = request.GET.get('pages')

            try:
                page_obj = paginated_filtered.page(page_number)
            except PageNotAnInteger:
                page_obj = paginated_filtered.page(1)
            except EmptyPage:
                page_obj = paginated_filtered.page(page_number.num_pages)

            object_bundle = zip(page_obj, total_images, user_wishlist_mark_laptop)

            context = {'object_bundle': object_bundle,
                       'laptop_brand': laptop_brand, 'desktop_brand': desktop_brand, 'apple_brand': apple_brand,
                       'components_brand': components_brand, 'laptop_topnav': laptop_topnav,
                       'desktop_topnav': desktop_topnav,
                       'apple_topnav': apple_topnav, 'components_topnav': components_topnav,
                       'current_user': current_user, 'cart_quantity_total': order_cart_cookie['cart_total_items'],
                       'cart_total_price': order_cart_cookie['cart_total_price'], 'page_obj': page_obj,
                       'search_name': search_name
                       }

            return render(request, 'client_page/search/list_products.html', context)

        elif re.search(search_name.casefold(), 'Components'):
            laptop_query = ComponentsProducts.objects.all()
            for items in laptop_query:
                total_images.append(
                    ProductsImage.objects.filter(product_id=items.id, products_type=items.categories).last())

            user_wishlist_mark_laptop = []
            for items in laptop_query:
                if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
                    wishlist_query = Wishlist.objects.filter(user=request.user, product_id=items.id,
                                                             products_type=items.categories).last()
                    if wishlist_query:
                        user_wishlist_mark_laptop.append('True')
                    else:
                        user_wishlist_mark_laptop.append('False')
                else:
                    user_wishlist_mark_laptop.append('False')

            # pagination
            paginated_filtered = Paginator(laptop_query, 12)
            page_number = request.GET.get('pages')

            try:
                page_obj = paginated_filtered.page(page_number)
            except PageNotAnInteger:
                page_obj = paginated_filtered.page(1)
            except EmptyPage:
                page_obj = paginated_filtered.page(page_number.num_pages)

            object_bundle = zip(page_obj, total_images, user_wishlist_mark_laptop)

            context = {'object_bundle': object_bundle,
                       'laptop_brand': laptop_brand, 'desktop_brand': desktop_brand, 'apple_brand': apple_brand,
                       'components_brand': components_brand, 'laptop_topnav': laptop_topnav,
                       'desktop_topnav': desktop_topnav,
                       'apple_topnav': apple_topnav, 'components_topnav': components_topnav,
                       'current_user': current_user, 'cart_quantity_total': order_cart_cookie['cart_total_items'],
                       'cart_total_price': order_cart_cookie['cart_total_price'], 'page_obj': page_obj,
                       'search_name': search_name
                       }

            return render(request, 'client_page/search/list_products.html', context)

        else:
            image_list = []
            new_query = []
            # search based title search, description
            laptop_query_search = LaptopProducts.objects.filter(
                Q(title__icontains=search_name) | Q(description__icontains=search_name))

            if laptop_query_search:
                for item in laptop_query_search:
                    queryset_list.append(item)

            desktop_query_search = DesktopsProducts.objects.filter(
                Q(title__icontains=search_name) | Q(description__icontains=search_name))
            if desktop_query_search:
                for item in desktop_query_search:
                    queryset_list.append(item)

            apple_query_search = AppleProducts.objects.filter(
                Q(title__icontains=search_name) | Q(description__icontains=search_name))
            if apple_query_search:
                for item in apple_query_search:
                    queryset_list.append(item)

            components_query_search = ComponentsProducts.objects.filter(
                Q(title__icontains=search_name) | Q(description__icontains=search_name))
            if components_query_search:
                for item in apple_query_search:
                    queryset_list.append(item)

            cars_list = sorted(
                chain(laptop_query_search, desktop_query_search, apple_query_search, components_query_search),
                key=lambda car: car.id, reverse=True)

            for item in cars_list:
                image_list.append(
                    ProductsImage.objects.filter(product_id=item.id, products_type=item.categories).last())

            user_wishlist_mark_laptop = []
            for items in cars_list:
                if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
                    wishlist_query = Wishlist.objects.filter(user=request.user, product_id=items.id,
                                                             products_type=items.categories).last()
                    if wishlist_query:
                        user_wishlist_mark_laptop.append('True')
                    else:
                        user_wishlist_mark_laptop.append('False')
                else:
                    user_wishlist_mark_laptop.append('False')

            # pagination
            paginated_filtered = Paginator(cars_list, 12)
            page_number = request.GET.get('pages')
            try:
                page_obj = paginated_filtered.page(page_number)
            except PageNotAnInteger:
                page_obj = paginated_filtered.page(1)
            except EmptyPage:
                page_obj = paginated_filtered.page(page_number.num_pages)

            obj_total = zip(cars_list, image_list, user_wishlist_mark_laptop)

            if cars_list:
                context = {'object_bundle': obj_total,
                           'laptop_brand': laptop_brand, 'desktop_brand': desktop_brand, 'apple_brand': apple_brand,
                           'components_brand': components_brand, 'laptop_topnav': laptop_topnav,
                           'desktop_topnav': desktop_topnav,
                           'apple_topnav': apple_topnav, 'components_topnav': components_topnav,
                           'current_user': current_user, 'cart_quantity_total': order_cart_cookie['cart_total_items'],
                           'cart_total_price': order_cart_cookie['cart_total_price'],
                           'page_obj': page_obj, 'search_name': search_name}
                return render(request, 'client_page/search/list_products.html', context)
            else:
                specification_image_list = []
                query_finals = []

                # search based on specification
                specification_query = ProductSpecification.objects.filter(
                    Q(title__icontains=search_name) | Q(description__icontains=search_name))

                for items in specification_query:
                    if items.products_type == 'Laptops':
                        per_laptop = LaptopProducts.objects.filter(id=items.product_id).last()
                        query_finals.append(per_laptop)

                    elif items.products_type == 'Desktops':
                        per_desktop = DesktopsProducts.objects.filter(id=items.product_id).last()
                        query_finals.append(per_desktop)

                    elif items.products_type == 'Apple':
                        per_apple = AppleProducts.objects.filter(id=items.product_id).last()
                        query_finals.append(per_apple)

                    elif items.products_type == 'Components':
                        per_components = ComponentsProducts.objects.filter(id=items.product_id).last()
                        query_finals.append(per_components)

                for item in query_finals:
                    specification_image_list.append(
                        ProductsImage.objects.filter(product_id=item.id, products_type=item.categories).last())

                user_wishlist_mark_laptops = []
                for items in query_finals:
                    if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization is False:
                        wishlist_query = Wishlist.objects.filter(user=request.user, product_id=items.id,
                                                                 products_type=items.categories).last()
                        if wishlist_query:
                            user_wishlist_mark_laptops.append('True')
                        else:
                            user_wishlist_mark_laptops.append('False')
                    else:
                        user_wishlist_mark_laptops.append('False')

                # pagination
                paginated_filtered = Paginator(new_query, 12)
                page_number = request.GET.get('page')
                try:
                    page_obj = paginated_filtered.page(page_number)
                except PageNotAnInteger:
                    page_obj = paginated_filtered.page(1)
                except EmptyPage:
                    page_obj = paginated_filtered.page(page_number.num_pages)

                obj_spec = zip(query_finals, specification_image_list, user_wishlist_mark_laptops)

                context = {'object_bundle': obj_spec,
                           'laptop_brand': laptop_brand, 'desktop_brand': desktop_brand, 'apple_brand': apple_brand,
                           'components_brand': components_brand, 'laptop_topnav': laptop_topnav,
                           'desktop_topnav': desktop_topnav,
                           'apple_topnav': apple_topnav, 'components_topnav': components_topnav,
                           'current_user': current_user, 'cart_quantity_total': order_cart_cookie['cart_total_items'],
                           'cart_total_price': order_cart_cookie['cart_total_price'], 'page_obj': page_obj,
                           'search_name': search_name}
                return render(request, 'client_page/search/list_products.html', context)

#endregion



