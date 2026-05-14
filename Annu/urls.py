"""
URL configuration for Annu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.views.static import serve
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('logout/', RedirectView.as_view(url='/admin/logout/')),
    path('base',BASE,name='base'),
    path('',HOME,name='home'),
    path('products',PRODUCT,name='product'),
    path('search',SEARCH,name='search'),
    path('contact',CONTACT_PAGE,name='contact'),
    path('product_details/<str:id>',PRODUCT_DETAILS_PAGE,name='product_details'),


    path('register',HandleRegister,name='register'),
    path('login',HandleLogin,name='login'),
    path('logout',HandleLogout,name='logout'),


    # CART
    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart-detail/',cart_detail,name='cart_detail'),
    path('cart/checkout/',CHECKOUT,name='checkout'),

    path('cart/checkout/placeorder',PLACE_ORDER,name='place_order'),

    path('success',SUCCESS,name='success'),


    path('Your_order',YOURORDER,name='your_order'),
    path('404page',BLANK,name='404'),

  


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(
            r'^media/(?P<path>.*)$',
            serve,
            {'document_root': settings.MEDIA_ROOT},
        ),
    ]
