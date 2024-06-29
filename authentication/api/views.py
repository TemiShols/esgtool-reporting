from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (CustomUserSerializer, DashboardSerializer)
from reporting.models import FuelModel, WasteModel, ElectricityModel, HeatingModelEmission, HomeHeatingModelEmissions
from authentication.models import CustomUser
from django.db.models import Sum, F, FloatField


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Fuel Emissions
        user_fuel_emissions = FuelModel.objects.filter(user=user)
        fuel_total_emissions = user_fuel_emissions.aggregate(
            total_emissions=Sum(
                F('Af_v') * F('Fc_h') * F('Fox') * (44 / 12),
                output_field=FloatField()
            )
        )['total_emissions']
        fuel_categories = list(user_fuel_emissions.values_list('fuel', flat=True).distinct())
        fuel_emissions_data = [
            user_fuel_emissions.filter(fuel=fuel).aggregate(
                emissions=Sum(F('Af_v') * F('Fc_h') * F('Fox') * (44 / 12), output_field=FloatField())
            )['emissions'] for fuel in fuel_categories
        ]

        # Waste Emissions
        user_waste_emissions = WasteModel.objects.filter(user=user)
        waste_total_emissions = sum(waste.calculate_waste_emissions() for waste in user_waste_emissions)
        waste_categories = list(user_waste_emissions.values_list('waste_treatment', flat=True).distinct())
        waste_emissions_data = [
            sum(waste.calculate_waste_emissions() for waste in
                user_waste_emissions.filter(waste_treatment=waste_treatment))
            for waste_treatment in waste_categories
        ]

        # Electricity Emissions
        user_electricity_emissions = ElectricityModel.objects.filter(user=user)
        electricity_total_emissions = sum(
            electricity.calculate_co2_emissions_from_electricity() for electricity in user_electricity_emissions)
        electricity_categories = list(user_electricity_emissions.values_list('start_date', flat=True).distinct())
        electricity_categories_str = [date.strftime('%Y-%m-%d') for date in electricity_categories]
        electricity_emissions_data = [
            sum(electricity.calculate_co2_emissions_from_electricity() for electricity in
                user_electricity_emissions.filter(start_date=start_date))
            for start_date in electricity_categories
        ]

        # Heating Emissions
        user_heating_emissions = HeatingModelEmission.objects.filter(user=user)
        heating_total_emissions = sum(
            heating.calculate_total_emissions() for heating in user_heating_emissions
        )
        heating_categories = list(user_heating_emissions.values_list('start_date', flat=True).distinct())
        heating_categories_str = [date.strftime('%Y-%m-%d') for date in heating_categories]
        heating_emissions_data = [
            sum(
                heating.calculate_total_emissions() for heating in user_heating_emissions.filter(start_date=start_date)
            )
            for start_date in heating_categories
        ]

        # Home Heating Emissions
        user_home_heating_emissions = HomeHeatingModelEmissions.objects.filter(user=user)
        home_heating_total_emissions = sum(
            home_heating.calculate_home_heating_emissions() for home_heating in user_home_heating_emissions)
        home_heating_categories = list(user_home_heating_emissions.values_list('fuel', flat=True).distinct())
        home_heating_emissions_data = [
            sum(home_heating.calculate_home_heating_emissions() for home_heating in
                user_home_heating_emissions.filter(fuel=fuel))
            for fuel in home_heating_categories
        ]

        # Combine total emissions from all models
        total_emissions = sum(filter(None, [
            fuel_total_emissions,
            waste_total_emissions,
            electricity_total_emissions,
            heating_total_emissions,
            home_heating_total_emissions
        ]))

        data = {
            'total_emissions': total_emissions,
            'fuel_categories': fuel_categories,
            'fuel_emissions_data': fuel_emissions_data,
            'waste_categories': waste_categories,
            'waste_emissions_data': waste_emissions_data,
            'electricity_categories': electricity_categories_str,
            'electricity_emissions_data': electricity_emissions_data,
            'heating_categories': heating_categories_str,
            'heating_emissions_data': heating_emissions_data,
            'home_heating_categories': home_heating_categories,
            'home_heating_emissions_data': home_heating_emissions_data,
        }

        serializer = DashboardSerializer(data)
        return Response(serializer.data)
