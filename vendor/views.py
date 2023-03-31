import json

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from queryset_sequence import QuerySetSequence

from .decorators import vendor_only
from .forms import LoginForm
from .models import VendorDesktopsProducts, VendorAppleProducts, VendorLaptopProducts, VendorComponentsProducts, \
    VendorBrands, VendorCart, VendorProductsImage, VendorOrder, VendorBilling, VendorDelivery


def vendor_product_cart_list(request):
    order = {'cart_total_price': 0, 'cart_total_items': 0, 'cart_saved_price': 0}
    cart_list = VendorCart.objects.filter(user_id=request.user.id)
    if cart_list:
        for items in cart_list:
            if items.products_type == 'Laptops':

                # if the cart has Laptops data run this function to calculate price and count items

                product = VendorLaptopProducts.objects.get(id=items.product_id)
                total_price = (product.latest_price * items.quantity)
                order['cart_total_price'] += total_price
                order['cart_total_items'] += items.quantity
                if product.old_price == 0:
                    pass
                else:
                    order['cart_saved_price'] += ((product.old_price - product.latest_price) * items.quantity)

            if items.products_type == 'Desktops':
                # if the cart has Desktops data run this function to calculate price and count items

                product = VendorDesktopsProducts.objects.get(id=items.product_id)
                total_price = (product.latest_price * items.quantity)
                order['cart_total_price'] += total_price
                order['cart_total_items'] += items.quantity
                if product.old_price == 0:
                    pass
                else:
                    order['cart_saved_price'] += ((product.old_price - product.latest_price) * items.quantity)

            if items.products_type == 'Apple':
                # if the cart has Apple data run this function to calculate price and count items

                product = VendorAppleProducts.objects.get(id=items.product_id)
                total_price = (product.latest_price * items.quantity)
                order['cart_total_price'] += total_price
                order['cart_total_items'] += items.quantity
                if product.old_price == 0:
                    pass
                else:
                    order['cart_saved_price'] += ((product.old_price - product.latest_price) * items.quantity)

            if items.products_type == 'Components':
                # if the cart has Apple data run this function to calculate price and count items

                product = VendorComponentsProducts.objects.get(id=items.product_id)
                total_price = (product.latest_price * items.quantity)
                order['cart_total_price'] += total_price
                order['cart_total_items'] += items.quantity
                if product.old_price == 0:
                    pass
                else:
                    order['cart_saved_price'] += ((product.old_price - product.latest_price) * items.quantity)

        return order


def vendor_login(request):
    if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization:
        return redirect('vendor_page_vendor')
    else:
        sign_in_form = LoginForm()
        context = {'sign_in_form': sign_in_form}
        return render(request, 'vendor/vendor_login.html', context)


def vendor_authentication_sign_in_post(request):
    if request.method == 'POST':

        # get email, password and remember_me options from the user
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        # check if the user email is registered
        user = User.objects.filter(email=email, profile__authorization=True).last()

        if user is not None:

            # check if user is client and password matches
            if user.is_staff and check_password(password, user.password):

                # if user credentials matches add session to the user
                login(request, user)

                return redirect('vendor_page_vendor')
            else:

                # given password does not match or the account is not client privilege
                messages.warning(request, 'Access Denied!')
                return redirect('vendor_login_vendor')
        else:

            # given email is not registered
            messages.warning(request, 'Wrong credentials!')
            return redirect('vendor_login_vendor')


@vendor_only
def vendor_page(request):
    brands_list = VendorBrands.objects.all()
    order_cart = vendor_product_cart_list(request)
    context = {'brands_list': brands_list, 'order_cart': order_cart}
    return render(request, 'vendor/tDeal.html', context)


@vendor_only
def vendor_ajax_today_deals(request):
    brandtype = request.GET.get('brandId')
    product_list = []
    if brandtype:
        final_laptop_products = VendorLaptopProducts.objects.filter(brand_id=brandtype)
        final_desktop_products = VendorDesktopsProducts.objects.filter(brand_id=brandtype)
        final_apple_products = VendorAppleProducts.objects.filter(brand_id=brandtype)
        final_components_products = VendorComponentsProducts.objects.filter(brand_id=brandtype)

        price_min = request.GET.get('price_min')
        if price_min:
            final_laptop_products = final_laptop_products.filter(latest_price__gte=price_min)
            final_desktop_products = final_desktop_products.filter(latest_price__gte=price_min)
            final_apple_products = final_apple_products.filter(latest_price__gte=price_min)
            final_components_products = final_components_products.filter(latest_price__gte=price_min)

        price_max = request.GET.get('price_max')
        if price_max:
            final_laptop_products = final_laptop_products.filter(latest_price__lte=price_max)
            final_desktop_products = final_desktop_products.filter(latest_price__lte=price_max)
            final_apple_products = final_apple_products.filter(latest_price__lte=price_max)
            final_components_products = final_components_products.filter(latest_price__lte=price_max)

        condition = request.GET.get('condition')
        if condition:
            if condition == 'All':
                final_laptop_products = final_laptop_products
                final_desktop_products = final_desktop_products
                final_apple_products = final_apple_products
                final_components_products = final_components_products

            elif condition == 'New':
                final_laptop_products = final_laptop_products
                final_desktop_products = final_desktop_products
                final_apple_products = final_apple_products
                final_components_products = final_components_products

            elif condition == 'refurbished':
                final_laptop_products = final_laptop_products
                final_desktop_products = final_desktop_products
                final_apple_products = final_apple_products
                final_components_products = final_components_products

        toggle_checkbox = request.GET.get('toggle_checkbox')
        if toggle_checkbox:

            if toggle_checkbox == 'no':
                final_laptop_products = final_laptop_products
                final_desktop_products = final_desktop_products
                final_apple_products = final_apple_products
                final_components_products = final_components_products

            elif toggle_checkbox == 'yes':
                final_laptop_products = final_laptop_products.filter(stock__gt=0)
                final_desktop_products = final_desktop_products.filter(stock__gt=0)
                final_apple_products = final_apple_products.filter(stock__gt=0)
                final_components_products = final_components_products.filter(stock__gt=0)

        total_products = QuerySetSequence(final_laptop_products, final_desktop_products, final_apple_products,
                                          final_components_products)

        for item in total_products:
            product_list.append((item.title, item.description, item.latest_price, item.stock, item.id, item.categories))
        return JsonResponse(product_list, safe=False)


# add to cart function used in home page which return jsonresponse
@vendor_only
def update_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization:
            current_user = request.user
            data = json.loads(request.body)
            product_id = data['productId']
            product_type = data['producttype']

            action = data['action']

            if action == 'add':
                quantity = data['quantity']
                print('quantity', quantity)
                cart_add_query = VendorCart.objects.filter(user=current_user, product_id=product_id,
                                                           products_type=product_type).last()
                if cart_add_query:
                    cart_add_query.quantity += int(quantity)
                    cart_add_query.save()
                    return JsonResponse({'_actr': 'True'})
                else:
                    new_cart_query = VendorCart(user=current_user, product_id=product_id, products_type=product_type,
                                                quantity=quantity)
                    new_cart_query.save()
                    return JsonResponse({'_actr': 'True'})

            elif action == 'delete':
                VendorCart.objects.get(user=current_user, product_id=product_id,
                                       products_type=product_type).delete()
                return JsonResponse({'_actr': 'True'})

            elif action == 'update':
                quantity = data['quantity']
                print('quantity', quantity)
                VendorCart.objects.filter(user=current_user, product_id=product_id,
                                          products_type=product_type).update(quantity=quantity)
                return JsonResponse({'_actr': 'True'})


@vendor_only
def checkout_page(request):
    order_cart = vendor_product_cart_list(request)
    order_status = vendor_product_cart_list(request)
    cart_list = VendorCart.objects.filter(user=request.user)

    cart_list_photo = []
    cart_list_title = []
    cart_list_quanity = []

    # check the cartlist for the current-user
    for items in cart_list:
        if items.products_type == 'Laptops':

            cart_list_photo.append(
                VendorProductsImage.objects.filter(product_id=items.product_id,
                                                   products_type=items.products_type).last())

            cart_list_title.append(VendorLaptopProducts.objects.filter(id=items.product_id).last())
            cart_list_quanity.append(
                VendorCart.objects.filter(product_id=items.product_id, products_type=items.products_type,
                                          user=request.user).last().quantity)

        elif items.products_type == 'Desktops':
            cart_list_photo.append(
                VendorProductsImage.objects.filter(product_id=items.product_id,
                                                   products_type=items.products_type).last())
            cart_list_title.append(VendorDesktopsProducts.objects.filter(id=items.product_id).last())
            cart_list_quanity.append(
                VendorCart.objects.filter(product_id=items.product_id, products_type=items.products_type,
                                          user=request.user).last().quantity)

        elif items.products_type == 'Apple':
            cart_list_photo.append(
                VendorProductsImage.objects.filter(product_id=items.product_id,
                                                   products_type=items.products_type).last())
            cart_list_title.append(VendorAppleProducts.objects.filter(id=items.product_id).last())
            cart_list_quanity.append(
                VendorCart.objects.filter(product_id=items.product_id, products_type=items.products_type,
                                          user=request.user).last().quantity)

        elif items.products_type == 'Components':
            cart_list_photo.append(
                VendorProductsImage.objects.filter(product_id=items.product_id,
                                                   products_type=items.products_type).last())
            cart_list_title.append(VendorComponentsProducts.objects.filter(id=items.product_id).last())
            cart_list_quanity.append(
                VendorCart.objects.filter(product_id=items.product_id, products_type=items.products_type,
                                          user=request.user).last().quantity)

    # bundle item, quantity of per items and photo of the corresponding item
    cart_obj = zip(cart_list_title, cart_list_quanity, cart_list_photo)

    context = {'cart_obj': cart_obj, 'order_status': order_status, 'order_cart': order_cart}
    return render(request, 'vendor/vendor_checkout.html', context)


@vendor_only
def price_drop_page(request):
    brands_list = VendorBrands.objects.all()
    order_cart = vendor_product_cart_list(request)
    context = {'brands_list': brands_list, 'order_cart': order_cart}
    return render(request, 'vendor/pDrop.html', context)


@vendor_only
def vendor_ajax_price_drop(request):
    brandtype = request.GET.get('brandId')
    product_list = []
    if brandtype:
        final_laptop_products = VendorLaptopProducts.objects.filter(brand_id=brandtype, price_drop=1)
        final_desktop_products = VendorDesktopsProducts.objects.filter(brand_id=brandtype, price_drop=1)
        final_apple_products = VendorAppleProducts.objects.filter(brand_id=brandtype, price_drop=1)
        final_components_products = VendorComponentsProducts.objects.filter(brand_id=brandtype, price_drop=1)

        price_min = request.GET.get('price_min')
        if price_min:
            final_laptop_products = final_laptop_products.filter(latest_price__gte=price_min)
            final_desktop_products = final_desktop_products.filter(latest_price__gte=price_min)
            final_apple_products = final_apple_products.filter(latest_price__gte=price_min)
            final_components_products = final_components_products.filter(latest_price__gte=price_min)

        price_max = request.GET.get('price_max')
        if price_max:
            final_laptop_products = final_laptop_products.filter(latest_price__lte=price_max)
            final_desktop_products = final_desktop_products.filter(latest_price__lte=price_max)
            final_apple_products = final_apple_products.filter(latest_price__lte=price_max)
            final_components_products = final_components_products.filter(latest_price__lte=price_max)

        condition = request.GET.get('condition')
        if condition:
            if condition == 'All':
                final_laptop_products = final_laptop_products
                final_desktop_products = final_desktop_products
                final_apple_products = final_apple_products
                final_components_products = final_components_products

            elif condition == 'New':
                final_laptop_products = final_laptop_products
                final_desktop_products = final_desktop_products
                final_apple_products = final_apple_products
                final_components_products = final_components_products

            elif condition == 'refurbished':
                final_laptop_products = final_laptop_products
                final_desktop_products = final_desktop_products
                final_apple_products = final_apple_products
                final_components_products = final_components_products

        toggle_checkbox = request.GET.get('toggle_checkbox')
        if toggle_checkbox:

            if toggle_checkbox == 'no':
                final_laptop_products = final_laptop_products
                final_desktop_products = final_desktop_products
                final_apple_products = final_apple_products
                final_components_products = final_components_products

            elif toggle_checkbox == 'yes':
                final_laptop_products = final_laptop_products.filter(stock__gt=0)
                final_desktop_products = final_desktop_products.filter(stock__gt=0)
                final_apple_products = final_apple_products.filter(stock__gt=0)
                final_components_products = final_components_products.filter(stock__gt=0)

        total_products = QuerySetSequence(final_laptop_products, final_desktop_products, final_apple_products,
                                          final_components_products)
        for item in total_products:
            product_list.append((item.title, item.description, item.latest_price, item.stock, item.id, item.categories))
        return JsonResponse(product_list, safe=False)


@vendor_only
def just_launch_page(request):
    brands_list = VendorBrands.objects.all()
    order_cart = vendor_product_cart_list(request)
    context = {'brands_list': brands_list, 'order_cart': order_cart}
    return render(request, 'vendor/jLaunched.html', context)


@vendor_only
def vendor_ajax_just_launched(request):
    brandtype = request.GET.get('brandId')
    product_list = []
    if brandtype:
        final_laptop_products = VendorLaptopProducts.objects.filter(brand_id=brandtype, just_launched=1)
        final_desktop_products = VendorDesktopsProducts.objects.filter(brand_id=brandtype, just_launched=1)
        final_apple_products = VendorAppleProducts.objects.filter(brand_id=brandtype, just_launched=1)
        final_components_products = VendorComponentsProducts.objects.filter(brand_id=brandtype, just_launched=1)

        price_min = request.GET.get('price_min')
        if price_min:
            final_laptop_products = final_laptop_products.filter(latest_price__gte=price_min)
            final_desktop_products = final_desktop_products.filter(latest_price__gte=price_min)
            final_apple_products = final_apple_products.filter(latest_price__gte=price_min)
            final_components_products = final_components_products.filter(latest_price__gte=price_min)

        price_max = request.GET.get('price_max')
        if price_max:
            final_laptop_products = final_laptop_products.filter(latest_price__lte=price_max)
            final_desktop_products = final_desktop_products.filter(latest_price__lte=price_max)
            final_apple_products = final_apple_products.filter(latest_price__lte=price_max)
            final_components_products = final_components_products.filter(latest_price__lte=price_max)

        condition = request.GET.get('condition')
        if condition:
            if condition == 'All':
                final_laptop_products = final_laptop_products
                final_desktop_products = final_desktop_products
                final_apple_products = final_apple_products
                final_components_products = final_components_products

            elif condition == 'New':
                final_laptop_products = final_laptop_products.filter(condition=0)
                final_desktop_products = final_desktop_products.filter(condition=0)
                final_apple_products = final_apple_products.filter(condition=0)
                final_components_products = final_components_products.filter(condition=0)

            elif condition == 'refurbished':
                final_laptop_products = final_laptop_products.filter(condition=1)
                final_desktop_products = final_desktop_products.filter(condition=1)
                final_apple_products = final_apple_products.filter(condition=1)
                final_components_products = final_components_products.filter(condition=1)

        toggle_checkbox = request.GET.get('toggle_checkbox')
        if toggle_checkbox:

            if toggle_checkbox == 'no':
                final_laptop_products = final_laptop_products
                final_desktop_products = final_desktop_products
                final_apple_products = final_apple_products
                final_components_products = final_components_products

            elif toggle_checkbox == 'yes':
                final_laptop_products = final_laptop_products.filter(stock__gt=0)
                final_desktop_products = final_desktop_products.filter(stock__gt=0)
                final_apple_products = final_apple_products.filter(stock__gt=0)
                final_components_products = final_components_products.filter(stock__gt=0)

        total_products = QuerySetSequence(final_laptop_products, final_desktop_products, final_apple_products,
                                          final_components_products)
        for item in total_products:
            product_list.append((item.title, item.description, item.latest_price, item.stock, item.id, item.categories))
        return JsonResponse(product_list, safe=False)


@vendor_only
def just_sold_page(request):
    brands_list = VendorBrands.objects.all()
    order_cart = vendor_product_cart_list(request)
    context = {'brands_list': brands_list, 'order_cart': order_cart}
    return render(request, 'vendor/jSold.html', context)


@vendor_only
def vendor_ajax_just_sold(request):
    brandtype = request.GET.get('brandId')
    product_list = []
    if brandtype:
        final_laptop_products = VendorLaptopProducts.objects.filter(brand_id=brandtype, just_launched=1)
        final_desktop_products = VendorDesktopsProducts.objects.filter(brand_id=brandtype, just_launched=1)
        final_apple_products = VendorAppleProducts.objects.filter(brand_id=brandtype, just_launched=1)
        final_components_products = VendorComponentsProducts.objects.filter(brand_id=brandtype, just_launched=1)

        price_min = request.GET.get('price_min')
        if price_min:
            final_laptop_products = final_laptop_products.filter(latest_price__gte=price_min)
            final_desktop_products = final_desktop_products.filter(latest_price__gte=price_min)
            final_apple_products = final_apple_products.filter(latest_price__gte=price_min)
            final_components_products = final_components_products.filter(latest_price__gte=price_min)

        price_max = request.GET.get('price_max')
        if price_max:
            final_laptop_products = final_laptop_products.filter(latest_price__lte=price_max)
            final_desktop_products = final_desktop_products.filter(latest_price__lte=price_max)
            final_apple_products = final_apple_products.filter(latest_price__lte=price_max)
            final_components_products = final_components_products.filter(latest_price__lte=price_max)

        condition = request.GET.get('condition')
        if condition:
            if condition == 'All':
                final_laptop_products = final_laptop_products
                final_desktop_products = final_desktop_products
                final_apple_products = final_apple_products
                final_components_products = final_components_products

            elif condition == 'New':
                final_laptop_products = final_laptop_products.filter(condition=0)
                final_desktop_products = final_desktop_products.filter(condition=0)
                final_apple_products = final_apple_products.filter(condition=0)
                final_components_products = final_components_products.filter(condition=0)

            elif condition == 'refurbished':
                final_laptop_products = final_laptop_products.filter(condition=1)
                final_desktop_products = final_desktop_products.filter(condition=1)
                final_apple_products = final_apple_products.filter(condition=1)
                final_components_products = final_components_products.filter(condition=1)

        toggle_checkbox = request.GET.get('toggle_checkbox')
        if toggle_checkbox:

            if toggle_checkbox == 'no':
                final_laptop_products = final_laptop_products
                final_desktop_products = final_desktop_products
                final_apple_products = final_apple_products
                final_components_products = final_components_products

            elif toggle_checkbox == 'yes':
                final_laptop_products = final_laptop_products.filter(stock__gt=0)
                final_desktop_products = final_desktop_products.filter(stock__gt=0)
                final_apple_products = final_apple_products.filter(stock__gt=0)
                final_components_products = final_components_products.filter(stock__gt=0)

        total_products = QuerySetSequence(final_laptop_products, final_desktop_products, final_apple_products,
                                          final_components_products)
        for item in total_products:
            product_list.append((item.title, item.description, item.latest_price, item.stock, item.id, item.categories))
        return JsonResponse(product_list, safe=False)


@vendor_only
def vendor_authentication(request):
    order_list = []
    order_cart = vendor_product_cart_list(request)
    per_order = VendorOrder.objects.filter(user_id=request.user.id)
    for items in per_order:
        if items.products_type == 'Laptops':

            order_list.append((VendorLaptopProducts.objects.filter(id=items.product_id).last().title, items.quantity,
                               items.date_time))
        elif items.products_type == 'Desktops':
            order_list.append((VendorDesktopsProducts.objects.filter(id=items.product_id).last().title, items.quantity,
                               items.date_time))

        elif items.products_type == 'Apple':
            order_list.append(
                (VendorAppleProducts.objects.filter(id=items.product_id).last().title, items.quantity, items.date_time))

        elif items.products_type == 'Components':
            order_list.append((
                VendorComponentsProducts.objects.filter(id=items.product_id).last().title, items.quantity,
                items.date_time))

    order_obj = zip(order_list, per_order)

    billing_query = VendorBilling.objects.filter(user=request.user).last()
    delivery_query = VendorDelivery.objects.filter(user=request.user).last()

    context = {'order_cart': order_cart, 'order_list': order_obj, 'billing_query': billing_query,
               'delivery_query': delivery_query}
    return render(request, 'vendor/userAccount/index_userAccount.html', context)


@vendor_only
def checkout_order_save(request):
    cart_list = VendorCart.objects.filter(user_id=request.user.id)
    for item in cart_list:
        VendorOrder.objects.create(products_type=item.products_type, product_id=item.product_id, quantity=item.quantity,
                                   user_id=item.user_id)

    cart_list.delete()

    return redirect('vendor_authentication_vendor')


@vendor_only
def vendor_address_post(request, ids):
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
        user_query = User.objects.filter(id=ids, is_superuser=False, is_staff=True, profile__authorization=True).last()
        if user_query:
            billing_query = VendorBilling.objects.filter(user=user_query).last()
            delivery_query = VendorDelivery.objects.filter(user=user_query).last()

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
                VendorBilling.objects.create(first_name=billing_firstname, last_name=billing_lastname,
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
                VendorDelivery.objects.create(first_name=delivery_firstname, last_name=delivery_lastname,
                                              company_name=delivery_company,
                                              street_address=delivery_street, town_city=delivery_town,
                                              state=delivery_state,
                                              zip=delivery_zip,
                                              contact=delivery_number, user=user_query)

            messages.success(request, 'Information updated')
            return redirect('vendor_authentication_vendor')
        else:
            messages.error(request, 'User not recognized')
            return redirect('vendor_authentication_vendor')


@vendor_only
def vendor_information_account_post(request, ids):
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
                        return redirect('vendor_authentication_vendor')
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
                                    return redirect('vendor_authentication_vendor')
                                else:
                                    messages.error(request, 'Current password does not match')
                                    return redirect('vendor_authentication_vendor')
                            else:
                                messages.error(request, 'New Password does not match')
                                return redirect('vendor_authentication_vendor')

                        else:
                            user_query.first_name = account_first_name
                            user_query.last_name = account_last_name
                            user_query.email = account_new_email

                            user_query.save()

                            messages.success(request, 'User updated')
                            return redirect('vendor_authentication_vendor')
            else:
                if chkBox is not None:
                    if account_new_password == account_confirm_password:
                        if check_password(account_old_password, user_query.password):
                            user_query.first_name = account_first_name
                            user_query.last_name = account_last_name
                            user_query.set_password(account_new_password)

                            user_query.save()

                            messages.success(request, 'User updated')
                            return redirect('vendor_authentication_vendor')
                        else:
                            messages.error(request, 'Current password does not match')
                            return redirect('vendor_authentication_vendor')
                    else:
                        messages.error(request, 'New Password does not match')
                        return redirect('vendor_authentication_vendor')
                else:
                    user_query.first_name = account_first_name
                    user_query.last_name = account_last_name

                    user_query.save()

                    messages.success(request, 'User updated')
                    return redirect('vendor_authentication_vendor')

        else:
            messages.error(request, 'User not recognized')
            return redirect('vendor_authentication_vendor')


# add to cart function used in home page which return jsonresponse
@vendor_only
def update_order(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_staff and request.user.profile.authorization:
            current_user = request.user
            data = json.loads(request.body)
            product_id = data['productId']
            product_type = data['producttype']

            action = data['action']

            if action == 'delete':
                cart_add_query = VendorOrder.objects.filter(user=current_user, id=product_id,
                                                            products_type=product_type).last()

                if cart_add_query.verified:
                    return JsonResponse({'_actr': 'False'})
                else:
                    cart_add_query.delete()
                    return JsonResponse({'_actr': 'True'})

