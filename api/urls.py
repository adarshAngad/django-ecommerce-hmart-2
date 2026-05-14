from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='api-product')

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/simulate/', views.simulate_checkout, name='api-checkout-simulate'),
]
