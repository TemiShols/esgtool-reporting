# forms.py
from django import forms
from .models import FuelModel, WasteModel, ElectricityModel, HeatingModelEmission, HomeHeatingModelEmissions, TransportModelEmissions, RefrigerantModelEmissions


class EmissionFuelForm(forms.ModelForm):
    class Meta:
        model = FuelModel
        fields = ('start_date', 'end_date', 'fuel', 'coal_type', 'Af_v',)  # Include fields for fuel type, electricity
        # consumption, and fuel volume


class EmissionsWasteForm(forms.ModelForm):
    class Meta:
        model = WasteModel
        fields = ('start_date', 'end_date', 'waste_treatment', 'waste_mass', )


class EmissionsElectricityForm(forms.ModelForm):
    class Meta:
        model = ElectricityModel
        fields = ('start_date', 'end_date', 'Af_kw',)  # Include fields for fuel type, electricity
        # consumption, and fuel volume


class EmissionsChpHeatingForm(forms.ModelForm):
    class Meta:
        model = HeatingModelEmission
        fields = ('start_date', 'end_date', 'steam_output', 'electricity_output',)


class EmissionsHeatingForm(forms.ModelForm):
    class Meta:
        model = HomeHeatingModelEmissions
        fields = ('start_date', 'end_date', 'room_size', 'fuel', 'fuel_volume',)


class TransportEmissionsForm(forms.ModelForm):
    class Meta:
        model = TransportModelEmissions
        fields = ['start_date', 'end_date', 'type', 'source', 'destination']


class RefrigerantEmissionsForm(forms.ModelForm):
    class Meta:
        model = RefrigerantModelEmissions
        fields = ['start_date', 'end_date', 'name', 'refrigerant', 'charge_amount_kg', 'charge_amount_kg', 'leak_rate', 'annual_top_up_kg', 'disposal_recovery_kg', 'retirement_recovery_kg']

