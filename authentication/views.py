from django.shortcuts import render, redirect
from reporting.helper import kg_to_mtco2
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, CategoryForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from reporting.models import FuelModel, WasteModel, ElectricityModel, HeatingModelEmission, HomeHeatingModelEmissions, TransportModelEmissions
from django.db.models import Sum, FloatField, F
import json


def home(request):
    return render(request, 'index.html', {})


@csrf_protect
def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        credential = authenticate(request, username=email, password=password)
        if credential is not None:
            user = CustomUser.objects.get(email=email)
            if user.is_authenticated:
                login(request, credential)
                return redirect('dashboard')
            else:
                messages.success(request, 'Please confirm your login details ')
                return redirect('login')
        else:
            messages.success(request, 'Invalid Username/Password')
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return redirect('login')


@csrf_protect
def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user_cred = form.save(commit=False)
            user_cred.save()
            logged = login(request, user_cred)
            print(logged)
            return render(request, 'categories.html', {})
    else:

        form = UserRegisterForm()
    context = {'form': form}
    messages.error(request, form.errors)
    return render(request, 'signUp.html', context)


#   @login_required()
#   def change_password(request):
#       if request.method == 'POST':
#           form = PasswordChangeForm(data=request.POST, user=request.user)
#           if form.is_valid():
#               form.save()
#               update_session_auth_hash(request, form.user)
#               messages.success(request, 'Password changed successfully')
#               return redirect('dashboard')

#           else:
#               form = PasswordChangeForm(user=request.user)
#           context = {'form': form}
#           return render(request, 'change_password.html', context)

@login_required()
def select_category(request):
    if request.method == 'POST':
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('dashboard')
        else:
            form = CategoryForm()
        context = {'form': form}
        return render(request, 'categories.html', context)
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request, 'categories.html', context)


def dashboard(request):
    user = request.user

    # Fuel Emissions
    user_fuel_emissions = FuelModel.objects.filter(user=user)
    fuel_total_emissions = user_fuel_emissions.aggregate(
        total_emissions=Sum(
            F('Af_v') * F('Fc_h') * F('Fox') * (44 / 12),
            output_field=FloatField()
        )
    )['total_emissions'] or 0  # Default to 0 if None
    fuel_categories = list(user_fuel_emissions.values_list('fuel', flat=True).distinct())
    fuel_emissions_data = [
        user_fuel_emissions.filter(fuel=fuel).aggregate(
            emissions=Sum(F('Af_v') * F('Fc_h') * F('Fox') * (44 / 12), output_field=FloatField())
        )['emissions'] or 0 for fuel in fuel_categories  # Default to 0 if None
    ]

    # Waste Emissions
    user_waste_emissions = WasteModel.objects.filter(user=user)
    waste_total_emissions = sum(
        waste.calculate_co2_emissions_from_waste() or 0 for waste in user_waste_emissions)  # Default to 0 if None
    waste_categories = list(user_waste_emissions.values_list('waste_treatment', flat=True).distinct())
    waste_emissions_data = [
        sum(waste.calculate_co2_emissions_from_waste() or 0 for waste in
            user_waste_emissions.filter(waste_treatment=waste_treatment))
        for waste_treatment in waste_categories  # Default to 0 if None
    ]

    # Electricity Emissions
    user_electricity_emissions = ElectricityModel.objects.filter(user=user)
    electricity_total_emissions = sum(
        electricity.calculate_co2_emissions_from_electricity() or 0 for electricity in
        user_electricity_emissions)  # Default to 0 if None
    electricity_categories = list(user_electricity_emissions.values_list('start_date', flat=True).distinct())
    electricity_categories_str = [date.strftime('%Y-%m-%d') for date in electricity_categories]
    electricity_emissions_data = [
        sum(electricity.calculate_co2_emissions_from_electricity() or 0 for electricity in
            user_electricity_emissions.filter(start_date=start_date))
        for start_date in electricity_categories  # Default to 0 if None
    ]

    # Heating Emissions
    user_heating_emissions = HeatingModelEmission.objects.filter(user=user)

    def get_heating_total_emissions(heating):
        emissions = heating.calculate_co2_emissions_from_heating()
        return emissions.get('total_emissions', 0)  # Extract 'total_emissions' from the dictionary

    heating_total_emissions = sum(
        get_heating_total_emissions(heating) for heating in user_heating_emissions)  # Default to 0 if None
    heating_categories = list(user_heating_emissions.values_list('start_date', flat=True).distinct())
    heating_categories_str = [date.strftime('%Y-%m-%d') for date in heating_categories]
    heating_emissions_data = [
        sum(get_heating_total_emissions(heating) for heating in user_heating_emissions.filter(start_date=start_date))
        for start_date in heating_categories  # Default to 0 if None
    ]

    # Home Heating Emissions
    user_home_heating_emissions = HomeHeatingModelEmissions.objects.filter(user=user)
    home_heating_total_emissions = sum(
        home_heating.calculate_co2_emissions_from_home_heating_emissions() or 0 for home_heating in
        user_home_heating_emissions)  # Default to 0 if None
    home_heating_categories = list(user_home_heating_emissions.values_list('fuel', flat=True).distinct())
    home_heating_emissions_data = [
        sum(home_heating.calculate_co2_emissions_from_home_heating_emissions() or 0 for home_heating in
            user_home_heating_emissions.filter(fuel=fuel))
        for fuel in home_heating_categories  # Default to 0 if None
    ]

    # Transport Emissions
    user_transport_emissions = TransportModelEmissions.objects.filter(user=user)
    transport_total_emissions = sum(
        transport.calculate_transportation_emission() or 0 for transport in user_transport_emissions
    )  # Default to 0 if None
    transport_categories = list(user_transport_emissions.values_list('start_date', flat=True).distinct())
    transport_categories_str = [date.strftime('%Y-%m-%d') for date in transport_categories]
    transport_emissions_data = [
        sum(transport.calculate_transportation_emission() or 0 for transport in
            user_transport_emissions.filter(start_date=start_date))
        for start_date in transport_categories  # Default to 0 if None
    ]

    # Combine total emissions from all models
    total_emissions = sum(filter(None, [
        fuel_total_emissions,
        waste_total_emissions,
        electricity_total_emissions,
        heating_total_emissions,
        home_heating_total_emissions,
        transport_total_emissions
    ]))

    # Prepare context for rendering
    #   Plot a graph to show which of the sector emits more carbon. So that will be having a bar chart or pie chart to\
    #   show the sector with the highest emissions
    context = {
        'total_emissions': round(kg_to_mtco2(total_emissions), 2),
        'fuel_categories': json.dumps(fuel_categories),
        'fuel_emissions_data': json.dumps(fuel_emissions_data),
        'waste_categories': json.dumps(waste_categories),
        'waste_emissions_data': json.dumps(waste_emissions_data),
        'electricity_categories': json.dumps(electricity_categories_str),
        'electricity_emissions_data': json.dumps(electricity_emissions_data),
        'heating_categories': json.dumps(heating_categories_str),
        'heating_emissions_data': json.dumps(heating_emissions_data),
        'home_heating_categories': json.dumps(home_heating_categories),
        'home_heating_emissions_data': json.dumps(home_heating_emissions_data),
        'transport_categories': json.dumps(transport_categories_str),
        'transport_emissions_data': json.dumps(transport_emissions_data),
    }

    return render(request, 'dashboard.html', context=context)
