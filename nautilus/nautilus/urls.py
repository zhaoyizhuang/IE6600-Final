from django.contrib import admin
from django.urls import path, re_path, include

from v1.views import StockViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stock', StockViewSet, basename='stock')

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include(router.urls)),
]

