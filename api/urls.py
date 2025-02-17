from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockCompanyViewSet, StockRatingViewSet, UserViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'stocks', StockCompanyViewSet)
router.register(r'ratings', StockRatingViewSet)
router.register(r'users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
