# helper functions

from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db.models import Max, Min, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Sum, OuterRef, Subquery,F,Value,Case,When,IntegerField
from django.http import HttpResponse,HttpResponseRedirect



# models
from admin_panel.models import Address, Category, Order, Billing, Delivery, Wishlist, Cart , Blogs
from admin_panel.models import Profile, ProductImage, Specification, Product, SubCategory, Brand, ProductReview
from app.forms import LoginForm

# forms/filters
try:
    from .filters import SnippetFilterProductList
except:
    pass
from .filters import SnippetFilterProductList
# inbuilt
import json


#region updatedCode

# after logged-in if there is any data in cookie save the data into db cart table
def cookie_cart_loging(request, _current_user):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = None
    if cart:
        print('cookie_cart_loging')
        # for each product type
        for item in cart:
            print(item)
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
    if request.user.is_authenticated:
        featured_products_objects = Product.objects.filter(is_featured=True, is_comming_soon=False, is_shown=True).annotate(is_in_wishllist=Case(When(wishlist_product__user=request.user, then=Value(True)), default=Value(False))).order_by('-id')[:10]
        comming_soon_products_objects = Product.objects.filter(is_comming_soon=True,is_shown=True).annotate(is_in_wishllist=Case(When(wishlist_product__user=request.user, then=Value(True)), default=Value(False))).order_by('-id')[:10]
        new_arrival_products_objects = Product.objects.filter(is_comming_soon=False, is_shown=True).annotate(is_in_wishllist=Case(When(wishlist_product__user=request.user, then=Value(True)), default=Value(False))).order_by('-id')[:10]
        all_products_objects = Product.objects.all().annotate(is_in_wishllist=Case(When(wishlist_product__user=request.user, then=Value(True)), default=Value(False)))
    else:
        featured_products_objects = Product.objects.filter(is_featured=True, is_comming_soon=False, is_shown=True).order_by('-id')[:10]
        comming_soon_products_objects = Product.objects.filter(is_comming_soon=True,is_shown=True).order_by('-id')[:10]
        new_arrival_products_objects = Product.objects.filter(is_comming_soon=False, is_shown=True).order_by('-id')[:10]
        all_products_objects = Product.objects.all()      
    
    
    category_objects = Category.objects.all()
    
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
    if request.user.is_authenticated:
        logged_in_user = request.user
    else:
        logged_in_user = None
    product_object = Product.objects.get(id=id)
    image_object = ProductImage.objects.filter(product_id=id)
    product_specification = Specification.objects.filter(product_id=id)
    products_review_list_object = ProductReview.objects.filter(product_id=id).order_by('-id')
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
        'current_user': request.user,
        'products_review_list': products_review_list_object,
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
        return render(request, 'app/order_proceed.html', context)
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
            print(cookies_cart_prodcut_list.values())
           
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
    return render(request, 'app/shopping_cart.html',context)



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
                response = redirect('index_app')
                print('cookie_cart_loging')
                response.delete_cookie('cart')
                return response
            
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
        print(request.user.is_authenticated)
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
                print('update')
                quantity = data['quantity']
                print(quantity)
                if quantity <= 0:
                    cart_add_query = Cart.objects.filter(user=current_user, product_id=product_id).last()
                    cart_add_query.delete()
                    return JsonResponse({'_actr': 'True'})
                cart_add_query = Cart.objects.filter(user=current_user, product_id=product_id).last()
                if cart_add_query:
                    cart_add_query.quantity = int(quantity)
                    cart_add_query.save()
                    return JsonResponse({'_actr': 'True'})
                
            elif action == 'details_cart_button_update':
                quantity = data['quantity']
                cart_add_query = Cart.objects.filter(user=current_user, product_id=product_id).last()
                if cart_add_query:
                    cart_add_query.quantity += int(quantity)
                    cart_add_query.save()
                    return JsonResponse({'_actr': 'True'})
                else:
                    new_cart_query = Cart(user=current_user, product_id=product_id, quantity=quantity)
                    new_cart_query.save()
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
        order_status = Order.objects.filter(user=logged_in_user,product= product_object, delivered = True).exists()
        if order_status:
            if ProductReview.objects.filter(user=logged_in_user, product=product_object).exists():
                ProductReview.objects.filter(user=logged_in_user, product=product_object).update(rating=star, review=review)
            else:
                ProductReview.objects.create(user = logged_in_user, product = product_object,rating=star,fullname=full_name, review=review)
            messages.success(request, 'Thanks for The Feedback!')
        else:
            messages.warning(request, 'You can not review this product because you have not bought it yet!')
        url = '/' + str(product_object.categories.slug) + '/' + str(product_id)
        return redirect(url)

# add wishlist if user is logged-in
def delete_wishlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['productId']
        wishlist_query = Wishlist.objects.get(product_id=product_id, user=request.user)
        wishlist_query.delete()

        return JsonResponse({'_actr': 'True'})
    

# updating the orderlist of current user
def cancel_orderlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['productId']

        orderlist_query = Order.objects.get(id=product_id, user=request.user)
        orderlist_query.delete()
        return JsonResponse({'_actr': 'True'})


# updating the cartlist of current user
def delete_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)

            product_id = data['productId']

            wishlist_query = Cart.objects.get(product_id=product_id, user=request.user)
            wishlist_query.delete()
            return JsonResponse({'_actr': 'True'})


#endregion
