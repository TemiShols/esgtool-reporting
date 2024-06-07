from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from reporting.models import FuelModel, WasteModel, ElectricityModel, HeatingModelEmission
from .serializers import FuelModelSerializer, WasteModelSerializer, ElectricityModelSerializer, \
    HeatingModelEmissionSerializer


class FuelModelViewSet(viewsets.ModelViewSet):
    queryset = FuelModel.objects.all()
    serializer_class = FuelModelSerializer
    permission_classes = [IsAuthenticated]


class WasteModelViewSet(viewsets.ModelViewSet):
    queryset = WasteModel.objects.all()
    serializer_class = WasteModelSerializer
    permission_classes = [IsAuthenticated]


class ElectricityModelViewSet(viewsets.ModelViewSet):
    queryset = ElectricityModel.objects.all()
    serializer_class = ElectricityModelSerializer
    permission_classes = [IsAuthenticated]


class HeatingModelEmissionViewSet(viewsets.ModelViewSet):
    queryset = HeatingModelEmission.objects.all()
    serializer_class = HeatingModelEmissionSerializer
    permission_classes = [IsAuthenticated]
