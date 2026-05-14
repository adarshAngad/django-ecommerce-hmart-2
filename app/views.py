from smtplib import SMTPException

import random
import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from cart.cart import Cart

from .models import *


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRATE))


def BASE(request):
    return render(request, 'Main/base.html')


def HOME(request):
    product = Product.objects.filter(status='Publish').order_by('-id')
    top = list(product[:2])
    if not top:
        hero_slides = []
    elif len(top) == 1:
        hero_slides = [top[0], top[0]]
    else:
        hero_slides = top

    context = {
        'product': product,
        'hero_slides': hero_slides,
    }
    return render(request, 'Main/index.html', context)


def PRODUCT(request):
    categories = Categories.objects.all()
    filter_price = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()
    total_products = Product.objects.count()

    CATID = request.GET.get('categories')
    PRICE_FILTER_ID = request.GET.get('filter_price')
    COLOR_ID = request.GET.get('color')
    BRAND_ID = request.GET.get('brand')
    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')
    PRICE_LOWTOHIGH_ID = request.GET.get('PRICE_LOWTOHIGH')
    PRICE_HIGHTOLOW_ID = request.GET.get('PRICE_HIGHTOLOW')
    NEW_PRODUCT_ID = request.GET.get('NEW_PRODUCT')
    OLD_PRODUCT_ID = request.GET.get('OLD_PRODUCT')

    if CATID:
        product = Product.objects.filter(categories=CATID, status='Publish')
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price=PRICE_FILTER_ID, status='Publish')
    elif COLOR_ID:
        product = Product.objects.filter(color=COLOR_ID, status='Publish')
    elif BRAND_ID:
        product = Product.objects.filter(brand=BRAND_ID, status='Publish')
    elif ATOZID:
        product = Product.objects.filter(status='Publish').order_by('name')
    elif ZTOAID:
        product = Product.objects.filter(status='Publish').order_by('-name')
    elif PRICE_LOWTOHIGH_ID:
        product = Product.objects.filter(status='Publish').order_by('price')
    elif PRICE_HIGHTOLOW_ID:
        product = Product.objects.filter(status='Publish').order_by('-price')
    elif NEW_PRODUCT_ID:
        product = Product.objects.filter(status='Publish', condition='New').order_by('-id')
    elif OLD_PRODUCT_ID:
        product = Product.objects.filter(status='Publish', condition='Old').order_by('-id')
    else:
        product = Product.objects.filter(status='Publish').order_by('-id')

    context = {
        'product': product,
        'categories': categories,
        'filter_price': filter_price,
        'color': color,
        'brand': brand,
        'total_products': total_products,
    }
    return render(request, 'Main/product.html', context)


def SEARCH(request):
    query = (request.GET.get('query') or '').strip()
    if query:
        product = Product.objects.filter(name__icontains=query)
    else:
        product = Product.objects.none()

    context = {
        'product': product,
    }
    return render(request, 'Main/search.html', context)


def PRODUCT_DETAILS_PAGE(request, id):
    prod = get_object_or_404(Product, id=id)

    context = {
        'prod': prod,
    }
    return render(request, 'Main/product_single.html', context)


def CONTACT_PAGE(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        contact.save()

        if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            try:
                send_mail(
                    subject or 'Contact form',
                    message or '',
                    settings.EMAIL_HOST_USER,
                    [email],
                )
            except SMTPException:
                pass
        return redirect('home')
    return render(request, 'Main/contact.html')


def HandleRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if not username or not email or not pass1:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('register')
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        try:
            customer = User.objects.create_user(username, email, pass1)
        except IntegrityError:
            messages.error(request, 'That username is already taken.')
            return redirect('register')

        customer.first_name = first_name or ''
        customer.last_name = last_name or ''
        customer.save()
        messages.success(request, 'Account created. Please log in.')
        return redirect('login')
    return render(request, 'Registration/auth.html')


@ensure_csrf_cookie
def HandleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
        return redirect('login')

    return render(request, 'Registration/auth.html')


def HandleLogout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product)
    return redirect('cart_detail')


@login_required(login_url='login')
def item_clear(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
    return redirect('cart_detail')


@login_required(login_url='login')
def item_increment(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product)
    return redirect('cart_detail')


@login_required(login_url='login')
def item_decrement(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.decrement(product=product)
    return redirect('cart_detail')


@login_required(login_url='login')
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')


@login_required(login_url='login')
def cart_detail(request):
    return render(request, 'Cart/cart.html')


@login_required(login_url='login')
def CHECKOUT(request):
    cart = request.session.get(settings.CART_SESSION_ID) or {}
    if not cart:
        return redirect('cart_detail')

    amount_str = request.POST.get('amount')

    if not amount_str:
        return HttpResponse('Amount is missing', status=400)

    amount_str = amount_str.replace('$', '').replace(',', '').strip()

    try:
        amount = int(float(amount_str))
    except ValueError:
        return HttpResponse('Invalid amount provided', status=400)

    try:
        payment = client.order.create({
            'amount': amount * 100,
            'currency': 'INR',
            'payment_capture': 1,
        })

        order_id = payment['id']
        context = {
            'order_id': order_id,
            'order_amount_paise': amount * 100,
        }
        return render(request, 'Cart/checkout.html', context)
    except Exception:
        return render(request, 'Main/404.html')


def generate_tracking_id():
    tracking_id = random.randint(10**9, 10**10 - 1)
    return str(tracking_id)


def _safe_int(value, default=0):
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return default


@login_required(login_url='login')
def PLACE_ORDER(request):
    context = {}
    cart = request.session.get(settings.CART_SESSION_ID) or {}
    if not cart:
        return redirect('cart_detail')

    if request.method != 'POST':
        return redirect('cart_detail')

    user = request.user

    firstname = request.POST.get('firstname') or ''
    lastname = request.POST.get('lastname') or ''
    country = request.POST.get('country') or ''
    addr1 = request.POST.get('address') or ''
    addr2 = request.POST.get('address2') or ''
    address = (addr1 + ('\n' + addr2 if addr2 else '')).strip() or '-'
    city = request.POST.get('city') or ''
    state = request.POST.get('state') or ''
    postcode = _safe_int(request.POST.get('postcode'), 0)
    phone = _safe_int(request.POST.get('phone'), 0)
    email = request.POST.get('email') or user.email or ''
    additional_info = request.POST.get('additional_info') or ''

    order_id = request.POST.get('order_id')
    amount_raw = (request.POST.get('amount') or '').replace('$', '').replace(',', '').strip()
    amount = amount_raw or '0'

    context = {
        'order_id': order_id,
        'order_amount_paise': 0,
    }

    if not order_id:
        return render(request, 'Cart/placeorder.html', context)

    total_rupees = 0
    for i in cart:
        try:
            total_rupees += int(cart[i]['price']) * int(cart[i]['quantity'])
        except (ValueError, TypeError, KeyError):
            continue
    context['order_amount_paise'] = total_rupees * 100

    data = Order(
        user=user,
        firstname=firstname,
        lastname=lastname,
        country=country,
        address=address,
        city=city,
        state=state,
        postcode=postcode,
        phone=phone,
        email=email,
        additional_info=additional_info,
        payment_id=order_id,
        amount=amount,
    )
    data.tracking_id = generate_tracking_id()
    data.save()

    for i in cart:
        try:
            a = int(cart[i]['price'])
            b = int(cart[i]['quantity'])
        except (ValueError, TypeError, KeyError):
            continue
        total = a * b
        OrderItems.objects.create(
            user=user,
            order=data,
            product=cart[i]['name'],
            image=cart[i].get('image', '') or '',
            quantity=str(cart[i]['quantity']),
            price=str(cart[i]['price']),
            total=str(total),
        )

    return render(request, 'Cart/placeorder.html', context)


@csrf_exempt
def SUCCESS(request):
    if request.method == 'POST':
        order_id = ''
        for key, val in request.POST.items():
            if key == 'razorpay_order_id':
                order_id = val
                break

        if order_id:
            order = Order.objects.filter(payment_id=order_id).first()
            if order:
                order.paid = True
                order.save()

    request.session[settings.CART_SESSION_ID] = {}
    request.session.modified = True
    return render(request, 'Cart/thank-you.html')


@login_required(login_url='login')
def YOURORDER(request):
    order = OrderItems.objects.filter(user=request.user)

    context = {
        'order': order,
    }

    return render(request, 'Main/your_order.html', context)


def BLANK(request):
    return render(request, 'Main/404.html')
