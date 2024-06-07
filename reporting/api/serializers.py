from rest_framework import serializers
from reporting.models import FuelModel, WasteModel, ElectricityModel, HeatingModelEmission


class FuelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelModel
        fields = ['user', 'start_date', 'end_date', 'fuel', 'coal_type', 'Af_kw', 'Af_v', 'Af_m', 'Af_h', 'Fc_v', 'Fc_m', 'Fc_h', 'Fox' ]


class WasteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteModel
        fields = '__all__'


class ElectricityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricityModel
        fields = '__all__'


class HeatingModelEmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeatingModelEmission
        fields = '__all__'
