from django.shortcuts import render, redirect, HttpResponse
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, CategoryForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from reporting.models import FuelModel, WasteModel, ElectricityModel, HeatingModelEmission, HomeHeatingModelEmissions
from django.db.models import Sum, FloatField, F
import json
from datetime import datetime


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
        sum(waste.calculate_waste_emissions() for waste in user_waste_emissions.filter(waste_treatment=waste_treatment))
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

    # Prepare context for rendering
    context = {
        'total_emissions': total_emissions,
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
    }

    return render(request, 'dashboard.html', context=context)


def dashboard2(request):
    # Query to get all emissions records for the logged-in user
    user_emissions = FuelModel.objects.filter(user=request.user).order_by('start_date')

    # Calculate total emissions for the user
    total_emissions = user_emissions.aggregate(total_emissions=Sum('Af_v') * Sum('Fc_h') * Sum('Fox') * (44 / 12))

    # Grade the emissions
    if total_emissions['total_emissions'] < 1000:
        grade = "Low Emissions"
    elif total_emissions['total_emissions'] < 3000:
        grade = "Moderate Emissions"
    elif total_emissions['total_emissions'] < 6000:
        grade = "High Emissions"
    else:
        grade = "Very High Emissions"

    # Prepare data for Highcharts
    categories = [emission.start_date.strftime('%Y-%m-%d') for emission in user_emissions]
    emissions_data = [emission.Af_v * emission.Fc_h * emission.Fox * (44 / 12) for emission in user_emissions]

    context = {
        'total_emissions': total_emissions['total_emissions'],
        'grade': grade,
        'categories': categories,
        'emissions_data': emissions_data,
    }
    return render(request, 'dashboard.html', context=context)
