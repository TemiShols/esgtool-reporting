from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import FuelModelViewSet, WasteModelViewSet, ElectricityModelViewSet, HeatingModelEmissionViewSet

router = DefaultRouter()
router.register(r'fuel-emissions', FuelModelViewSet)
router.register(r'waste-emissions', WasteModelViewSet)
router.register(r'electricity-emissions', ElectricityModelViewSet)
router.register(r'heating-emissions', HeatingModelEmissionViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="ESG Reporting API",
        default_version='v1',
        description="API documentation for the ESG Reporting Dashboard",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@esg.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)

urlpatterns = [
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]