from django.contrib import admin
from .models import FuelModel, ElectricityModel, WasteModel, HeatingModelEmission, HomeHeatingModelEmissions, TransportModelEmissions, RefrigerantModelEmissions, Result


class FuelDataAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'fuel', 'Af_kw', 'Af_v', 'Af_m', 'Af_h', 'Fc_v', 'Fc_m', 'Fc_h', 'Fox',)


class WasteDataAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'waste_treatment', 'waste_mass',)


class ElectricityDataAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'Af_kw',)


class HeatingDataAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'steam_output', 'electricity_output',)


class HomeHeatingDataAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'room_size', 'fuel', 'fuel_volume',)


class TransportDataAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'type', 'mileage', 'source', 'destination')


class RefrigerantDataAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'refrigerant', 'annual_top_up_kg', 'charge_amount_kg', 'leak_rate')


class ResultDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_created', 'result_updated',)


admin.site.register(FuelModel, FuelDataAdmin)
admin.site.register(WasteModel, WasteDataAdmin)
admin.site.register(TransportModelEmissions, TransportDataAdmin)
admin.site.register(RefrigerantModelEmissions, RefrigerantDataAdmin)
admin.site.register(HeatingModelEmission, HeatingDataAdmin)
admin.site.register(HomeHeatingModelEmissions, HomeHeatingDataAdmin)
admin.site.register(ElectricityModel, ElectricityDataAdmin)
admin.site.register(Result, ResultDataAdmin)
