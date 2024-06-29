from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from reporting.models import FuelModel, WasteModel, ElectricityModel, HeatingModelEmission, Result, \
    HomeHeatingModelEmissions, RefrigerantModelEmissions, TransportModelEmissions
from .serializers import FuelModelSerializer, WasteModelSerializer, ElectricityModelSerializer, \
    HeatingModelEmissionSerializer, HomeHeatingEmissionSerializer, RefrigerantEmissionSerializer, CarSerializer, \
    TransportModelSerializer, ResultSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.decorators import action


@method_decorator(login_required, name='dispatch')
class FuelModelViewSet(viewsets.ModelViewSet):
    queryset = FuelModel.objects.all()
    serializer_class = FuelModelSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(commit=False)
            instance.user = request.user

            try:
                Af_v = float(instance.Af_v)
            except ValueError:
                return Response({'error': 'Invalid input for Af_v'}, status=status.HTTP_400_BAD_REQUEST)

            start_date = instance.start_date
            end_date = instance.end_date

            if start_date and end_date and end_date < start_date:
                return Response({'error': 'End date must be bigger than start date'},
                                status=status.HTTP_400_BAD_REQUEST)

            if instance.fuel == 'Petrol' and Af_v:
                instance.Af_m = Af_v * instance.get_density_for_fuel()
                instance.Af_h = Af_v * 32000
                instance.Fc_v = 2.31
                instance.Fc_m = 2.3
                instance.Fc_h = 2.31
                instance.Fox = 0.99
            elif instance.fuel == 'Diesel Oil' and Af_v:
                instance.Af_m = Af_v * instance.get_density_for_fuel()
                instance.Af_h = Af_v * 34000
                instance.Fc_v = 2.68
                instance.Fc_m = 2.7
                instance.Fc_h = 2.68
                instance.Fox = 0.99
            elif instance.fuel == 'LPG' and Af_v:
                instance.Af_m = Af_v * instance.get_density_for_fuel()
                instance.Af_h = Af_v * 35000
                instance.Fc_v = 1.96
                instance.Fc_m = 1.6
                instance.Fc_h = 1.96
                instance.Fox = 0.995
            elif instance.fuel == 'Coal' and Af_v:
                instance.Af_m = Af_v * instance.get_density_for_coal()
                instance.Af_h = Af_v * 25000  # Assuming a typical calorific value for coal
                instance.Fc_v = instance.get_coal_content_per_volume()
                instance.Fc_m = instance.get_coal_content_per_mass()
                instance.Fc_h = 25.8
                instance.Fox = 0.98

            instance.save()
            result, created = Result.objects.get_or_create(user=request.user, start_date=instance.start_date,
                                                           end_date=instance.end_date)
            result.fuel.add(instance)
            result.save()
            response_serializer = self.get_serializer(instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def view_fuel_emissions(self, request, pk=None):
        emission = self.get_object()
        if emission.calculate_fuel_co2_emissions() < 1000:
            grade = "Low Emissions"
        elif emission.calculate_fuel_co2_emissions() < 3000:
            grade = "Moderate Emissions"
        elif emission.calculate_fuel_co2_emissions() < 6000:
            grade = "High Emissions"
        else:
            grade = "Very High Emissions"

        data = {
            'emission': FuelModelSerializer(emission).data,
            'grade': grade,
        }
        return Response(data)


@method_decorator(login_required, name='dispatch')
class WasteModelViewSet(viewsets.ModelViewSet):
    queryset = WasteModel.objects.all()
    serializer_class = WasteModelSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(commit=False)
            instance.user = request.user

            start_date = instance.start_date
            end_date = instance.end_date

            if start_date and end_date and end_date < start_date:
                return Response({'error': 'End date must be bigger than start date'},
                                status=status.HTTP_400_BAD_REQUEST)

            instance.save()
            result, created = Result.objects.get_or_create(user=request.user, start_date=instance.start_date,
                                                           end_date=instance.end_date)
            result.waste.add(instance)
            result.save()
            response_serializer = self.get_serializer(instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def view_waste_emissions(self, request, pk=None):
        emission = self.get_object()
        if emission.calculate_co2_emissions_from_waste() < 1000:
            grade = "Low Emissions"
        elif emission.calculate_waste_emissions() < 3000:
            grade = "Moderate Emissions"
        elif emission.calculate_waste_emissions() < 6000:
            grade = "High Emissions"
        else:
            grade = "Very High Emissions"

        data = {
            'emission': WasteModelSerializer(emission).data,
            'grade': grade,
        }
        return Response(data)


@method_decorator(login_required, name='dispatch')
class ElectricityModelViewSet(viewsets.ModelViewSet):
    queryset = ElectricityModel.objects.all()
    serializer_class = ElectricityModelSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(commit=False)
            instance.user = request.user

            start_date = instance.start_date
            end_date = instance.end_date

            if start_date and end_date and end_date < start_date:
                return Response({'error': 'End date must be bigger than start date'},
                                status=status.HTTP_400_BAD_REQUEST)

            instance.save()
            result, created = Result.objects.get_or_create(user=request.user, start_date=instance.start_date,
                                                           end_date=instance.end_date)
            result.electricity.add(instance)
            result.save()
            response_serializer = self.get_serializer(instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def view_electricity_emissions(self, request, pk=None):
        emission = self.get_object()
        if emission.calculate_co2_emissions_from_electricity() < 1000:
            grade = "Low Emissions"
        elif emission.calculate_co2_emissions_from_electricity() < 3000:
            grade = "Moderate Emissions"
        elif emission.calculate_co2_emissions_from_electricity() < 6000:
            grade = "High Emissions"
        else:
            grade = "Very High Emissions"

        data = {
            'emission': ElectricityModelSerializer(emission).data,
            'grade': grade,
        }
        return Response(data)


@method_decorator(login_required, name='dispatch')
class HeatingModelEmissionViewSet(viewsets.ModelViewSet):
    queryset = HeatingModelEmission.objects.all()
    serializer_class = HeatingModelEmissionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(commit=False)
            instance.user = request.user

            start_date = instance.start_date
            end_date = instance.end_date

            if start_date and end_date and end_date < start_date:
                return Response({'error': 'End date must be bigger than start date'},
                                status=status.HTTP_400_BAD_REQUEST)

            instance.save()
            result, created = Result.objects.get_or_create(user=request.user, start_date=instance.start_date,
                                                           end_date=instance.end_date)
            result.home_heating.add(instance)
            result.save()
            response_serializer = self.get_serializer(instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def view_home_heating_emissions(self, request, pk=None):
        emission = self.get_object()
        if emission.calculate_co2_emissions_from_home_heating_emissions() < 1000:
            grade = "Low Emissions"
        elif emission.calculate_home_heating_emissions() < 3000:
            grade = "Moderate Emissions"
        elif emission.calculate_home_heating_emissions() < 6000:
            grade = "High Emissions"
        else:
            grade = "Very High Emissions"

        data = {
            'emission': HeatingModelEmissionSerializer(emission).data,
            'grade': grade,
        }
        return Response(data)


@method_decorator(login_required, name='dispatch')
class HomeHeatingModelEmissionViewSet(viewsets.ModelViewSet):
    queryset = HomeHeatingModelEmissions.objects.all()
    serializer_class = HomeHeatingEmissionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(commit=False)
            instance.user = request.user

            start_date = instance.start_date
            end_date = instance.end_date

            if start_date and end_date and end_date < start_date:
                return Response({'error': 'End date must be bigger than start date'},
                                status=status.HTTP_400_BAD_REQUEST)

            instance.save()
            result, created = Result.objects.get_or_create(user=request.user, start_date=instance.start_date,
                                                           end_date=instance.end_date)
            result.home_heating.add(instance)
            result.save()
            response_serializer = self.get_serializer(instance)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def view_home_heating_emissions(self, request, pk=None):
        emission = self.get_object()
        if emission.calculate_co2_emissions_from_home_heating_emissions() < 1000:
            grade = "Low Emissions"
        elif emission.calculate_home_heating_emissions() < 3000:
            grade = "Moderate Emissions"
        elif emission.calculate_home_heating_emissions() < 6000:
            grade = "High Emissions"
        else:
            grade = "Very High Emissions"

        data = {
            'emission': HomeHeatingEmissionSerializer(emission).data,
            'grade': grade,
        }
        return Response(data)


class TransportModelEmissionsViewSet(viewsets.ModelViewSet):
    queryset = TransportModelEmissions.objects.all()
    serializer_class = TransportModelSerializer
    permission_classes = [IsAuthenticated]


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    #   @action(detail=False, methods=['get'])
    #   def view_results(self, request):
    #   results = Result.objects.all()
    #   data = ResultSerializer(results, many=True).data
    #   return Response(data)
