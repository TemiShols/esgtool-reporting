from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CustomUserViewSet, DashboardAPIView)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('api/dashboard/', DashboardAPIView.as_view(), name='dashboard-api'),
    path('api/', include(router.urls)),
]
