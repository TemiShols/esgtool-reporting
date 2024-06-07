from django.urls import path
from .views import calculate_fuel_emissions, view_fuel_emissions, calculate_waste_emissions, calculate_electricity_emissions, view_electricity_emissions,\
                    view_waste_emissions, calculate_chp_emissions,view_chp_emissions, calculate_home_heat_emissions, view_home_heating_emissions, \
                    calculate_transport_emissions, calculate_refrigerant_emissions, view_transport_emissions, view_results

urlpatterns = [
    path('calculate-fuel=emissions/', calculate_fuel_emissions, name='calculate_fuel_emissions'),
    path('calculate-waste=emissions/', calculate_waste_emissions, name='calculate_waste_emissions'),
    path('calculate-electricity=emissions/', calculate_electricity_emissions, name='calculate_electricity_emissions'),
    path('calculate-heating=emissions/', calculate_home_heat_emissions, name='calculate_home_heat_emissions'),
    path('calculate-chp=emissions', calculate_chp_emissions, name='calculate_chp_emissions'),
    path('calculate-refrigerant-=emissions', calculate_refrigerant_emissions, name='calculate_refrigerant_emissions'),
    path('calculate-transport=emissions', calculate_transport_emissions, name='calculate_transport_emissions'),
    path('view-waste=emissions/<int:pk>', view_waste_emissions, name='view_waste_emissions'),
    path('view-chp=emissions/<int:pk>', view_chp_emissions, name='view_chp_emissions'),
    path('view-emissions/<int:pk>', view_fuel_emissions, name='view_emissions'),
    path('view-electricity=emissions/<int:pk>', view_electricity_emissions, name='view_electricity_emissions'),
    path('view-home-heating-emissions/<int:pk>', view_home_heating_emissions, name='view_home_heating_emissions'),
    path('view-transport-emissions/<int:pk>', view_transport_emissions, name='view_transport_emissions'),
    path('results', view_results, name='results'),
]
