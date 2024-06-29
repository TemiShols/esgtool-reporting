from rest_framework import serializers
from reporting.models import FuelModel, WasteModel, ElectricityModel, HeatingModelEmission, HomeHeatingModelEmissions, \
    RefrigerantModelEmissions, Car, TransportModelEmissions, Result
from authentication.api.serializers import CustomUserSerializer


class FuelModelSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = FuelModel
        fields = ['user', 'start_date', 'end_date', 'fuel', 'coal_type', 'Af_v', 'Af_m', 'Af_h', 'Fc_v',
                  'Fc_m', 'Fc_h', 'Fox', 'user', ]


class WasteModelSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = WasteModel
        fields = ('start_date', 'end_date', 'waste_treatment', 'waste_mass', 'user',)


class ElectricityModelSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = ElectricityModel
        fields = ('start_date', 'end_date', 'Af_kw', 'user',)


class HeatingModelEmissionSerializer(serializers.ModelSerializer):  # CHP
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = HeatingModelEmission
        fields = ('start_date', 'end_date', 'steam_output', 'electricity_output', 'user',)


class RefrigerantEmissionSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = RefrigerantModelEmissions
        fields = ('start_date', 'end_date', 'refrigerant', 'charge_amount_kg', 'charge_amount_kg', 'leak_rate',
                  'annual_top_up_kg', 'disposal_recovery_kg', 'retirement_recovery_kg', 'user',)


class HomeHeatingEmissionSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = HomeHeatingModelEmissions
        fields = ('start_date', 'end_date', 'room_size', 'fuel', 'fuel_volume', 'user',)


class CarSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    co2_emission = serializers.SerializerMethodField('get_co2_emission')

    class Meta:
        model = Car
        fields = ['name', 'start_date', 'mend_date', 'registration_number', 'type', 'mileage', 'fuel_type',
                  'fuel_quantity', 'co2_emission']

    def get_co2_emission(self, obj):
        return obj.calculate_car_co2_emission()


class TransportModelSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True, read_only=True)
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = TransportModelEmissions
        fields = ['id', 'user', 'start_date', 'end_date', 'cars']


class ResultSerializer(serializers.ModelSerializer):
    fuel = FuelModelSerializer(many=True)
    electricity = ElectricityModelSerializer(many=True)
    waste = WasteModelSerializer(many=True)
    chp = HeatingModelEmissionSerializer(many=True)
    home_heating = HomeHeatingEmissionSerializer(many=True)
    transport = TransportModelSerializer(many=True)
    refrigerant = RefrigerantEmissionSerializer(many=True)

    class Meta:
        model = Result
        fields = ['user', 'start_date', 'end_date', 'result_updated', 'date_created', 'fuel', 'electricity', 'waste',
                  'chp', 'home_heating', 'transport', 'refrigerant']


class TransportSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    cars = CarSerializer(many=True)
    total_emission = serializers.SerializerMethodField()

    class Meta:
        model = TransportModelEmissions
        fields = ('start_date', 'end_date', 'cars', 'user', 'total_emission',)

    def get_total_emission(self, obj):
        return obj.calculate_transportation_emission()

    def create(self, validated_data):
        cars_data = validated_data.pop('cars')
        transport_model_emission = TransportModelEmissions.objects.create(**validated_data)
        for car_data in cars_data:
            car, created = Car.objects.get_or_create(**car_data)
            transport_model_emission.cars.add(car)
        return transport_model_emission

    def update(self, instance, validated_data):
        cars_data = validated_data.pop('cars')
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()

        instance.cars.clear()
        for car_data in cars_data:
            car, created = Car.objects.get_or_create(**car_data)
            instance.cars.add(car)

        return instance
