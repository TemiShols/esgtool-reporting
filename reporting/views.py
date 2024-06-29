from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .forms import EmissionFuelForm, EmissionsWasteForm, EmissionsElectricityForm, EmissionsChpHeatingForm, \
    EmissionsHeatingForm, RefrigerantEmissionsForm, CarForm
from django.contrib.auth.decorators import login_required
from .models import FuelModel, ElectricityModel, WasteModel, HeatingModelEmission, HomeHeatingModelEmissions, \
    TransportModelEmissions, Result, RefrigerantModelEmissions, Car
from django.contrib import messages
from authentication.models import CustomUser


@login_required()
def calculate_fuel_emissions(request):
    #   print(request.user.pk)
    if request.method == 'POST':
        form = EmissionFuelForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            user = CustomUser.objects.get(pk=request.user.pk)
            instance.user = user

            try:
                Af_v = float(instance.Af_v)
            except ValueError:
                return render(request, 'fuel_emissions_form.html', {'form': form, 'error': 'Invalid input for Af_v'})

            start_date = instance.start_date
            end_date = instance.end_date

            if start_date and end_date and end_date < start_date:
                return render(request, 'fuel_emissions_form.html',
                              {'form': form, 'error': 'End date must be bigger than start date'})

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

            #   instance.total_emissions_monthly = instance.calculate_co2_emissions()
            # instance.total_electricity_emissions_monthly = instance.calculate_co2_emissions_from_electricity()
            # instance.total_carbon_emissions_monthly = instance.total_emissions_monthly +
            # instance.total_electricity_emissions_monthly
            print(instance.fuel)
            instance.save()
            fuels = FuelModel.objects.filter(user=request.user).select_related('user').order_by('time_created')
            print(len(fuels))
            result, created = Result.objects.get_or_create(user=request.user, start_date=instance.start_date,
                                                           end_date=instance.end_date)
            if created:
                result.fuel.add(instance)
                result.save()
            if request.headers.get('Hx-Request'):
                return render(request, 'fuelmodel-partial.html', {'fuels': fuels})
            else:
                context = {
                    'form': form,
                    'fuels': fuels
                }

            return render(request, 'fuel_emissions_form.html', context)
    else:
        form = EmissionFuelForm()
    messages.success(request, form.errors)
    fuels = FuelModel.objects.filter(user=request.user).select_related('user').order_by('start_date')
    return render(request, 'fuel_emissions_form.html', {'form': form, 'fuels': fuels})


@login_required()
def calculate_waste_emissions(request):
    if request.method == 'POST':
        form = EmissionsWasteForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            user = CustomUser.objects.get(pk=request.user.pk)
            instance.user = user
            start_date = instance.start_date
            end_date = instance.end_date

            if start_date and end_date and end_date < start_date:
                return render(request, 'waste_emission_form.html',
                              {'form': form, 'error': 'End date must be bigger than start date'})

            instance.save()
            wasted = WasteModel.objects.filter(user=request.user).select_related('user').order_by('time_created')
            result, created = Result.objects.get_or_create(user=request.user, start_date=instance.start_date,
                                                           end_date=instance.end_date)
            if created:
                result.waste.add(instance)
                result.save()
            if request.headers.get('Hx-Request'):
                return render(request, 'wastemodel-partial.html', {'wasted': wasted})
            else:
                context = {
                    'form': form,
                    'wasted': wasted
                }

            return render(request, 'waste_emission_form.html', context)
    else:
        form = EmissionsWasteForm()
    messages.success(request, form.errors)
    wasted = WasteModel.objects.filter(user=request.user).select_related('user').order_by('time_created')
    context = {
        'form': form,
        'wasted': wasted
    }
    return render(request, 'waste_emission_form.html', context)


@login_required()
def calculate_electricity_emissions(request):
    if request.method == 'POST':
        form = EmissionsElectricityForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            user = CustomUser.objects.get(pk=request.user.pk)
            instance.user = user

            try:
                Af_v = float(instance.Af_kw)
            except ValueError:
                return render(request, 'electricity_emissions_form.html',
                              {'form': form, 'error': 'Invalid input for Af_v'})

            start_date = instance.start_date
            end_date = instance.end_date

            if start_date and end_date and end_date < start_date:
                return render(request, 'electricity_emissions_form.html',
                              {'form': form, 'error': 'End date must be bigger than start date'})

            instance.save()
            electrics = ElectricityModel.objects.filter(user=request.user).select_related('user').order_by(
                'time_created')
            result, created = Result.objects.get_or_create(user=request.user, start_date=instance.start_date,
                                                           end_date=instance.end_date)
            if created:
                result.electricity.add(instance)
                result.save()
            if request.headers.get('Hx-Request'):
                return render(request, 'electricitymodel-partial.html', {'electrics': electrics})
            else:
                context = {
                    'form': form,
                    'electrics': electrics
                }

            return render(request, 'electricity_emissions_form.html', context)
    else:
        form = EmissionsElectricityForm()
    messages.success(request, form.errors)
    electrics = ElectricityModel.objects.filter(user=request.user).select_related('user').order_by('time_created')
    context = {
        'form': form,
        'electrics': electrics
    }
    return render(request, 'electricity_emissions_form.html', context)


@login_required()
def calculate_chp_emissions1(request):
    #   print(request.user.pk)
    if request.method == 'POST':
        form = EmissionsChpHeatingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            user = CustomUser.objects.get(pk=request.user.pk)
            instance.user = user

            start_date = instance.start_date
            end_date = instance.end_date

            if start_date and end_date and end_date < start_date:
                return render(request, 'chp_emissions_form.html',
                              {'form': form, 'error': 'End date must be bigger than start date'})

            instance.save()
            chps = HeatingModelEmission.objects.filter(user=request.user).select_related('user').order_by(
                'time_created')
            result, created = Result.objects.get_or_create(user=request.user, start_date=instance.start_date,
                                                           end_date=instance.end_date)
            if created:
                result.chp.add(instance)
                result.save()
            if request.headers.get('Hx-Request'):
                return render(request, 'chpmodel-partial.html', {'chps': chps})
            else:
                context = {
                    'form': form,
                    'chps': chps
                }

            return render(request, 'chp_emissions_form.html', context)
    else:
        form = EmissionsChpHeatingForm()
    messages.success(request, form.errors)
    chps = HeatingModelEmission.objects.filter(user=request.user).select_related('user').order_by('time_created')
    context = {
        'form': form,
        'chps': chps
    }
    return render(request, 'chp_emissions_form.html', {'form': context})


@login_required()
def calculate_home_heat_emissions(request):
    #   print(request.user.pk)
    if request.method == 'POST':
        form = EmissionsHeatingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            user = CustomUser.objects.get(pk=request.user.pk)
            instance.user = user

            start_date = instance.start_date
            end_date = instance.end_date

            if start_date and end_date and end_date < start_date:
                return render(request, 'heating_emission_form.html',
                              {'form': form, 'error': 'End date must be bigger than start date'})

            instance.save()
            heatings = HomeHeatingModelEmissions.objects.filter(user=request.user).select_related('user').order_by(
                'time_created')
            result, created = Result.objects.get_or_create(user=request.user, start_date=instance.start_date,
                                                  end_date=instance.end_date)
            if created:
                result.home_heating.add(instance)
                result.save()
            if request.headers.get('Hx-Request'):
                return render(request, 'heatingmodel-partial.html', {'heatings': heatings})
            else:
                context = {
                    'form': form,
                    'heatings': heatings
                }

            return render(request, 'heating_emissions_form.html', context)
    else:
        form = EmissionsChpHeatingForm()
    messages.success(request, form.errors)
    heatings = HomeHeatingModelEmissions.objects.filter(user=request.user).select_related('user').order_by(
        'time_created')
    context = {
        'form': form,
        'heatings': heatings
    }
    return render(request, 'heating_emission_form.html', context)


@login_required()
def calculate_refrigerant_emissions(request):
    if request.method == 'POST':
        form = RefrigerantEmissionsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            refrigerants = RefrigerantModelEmissions.objects.filter(user=request.user).select_related('user').order_by(
                'time_created')
            result, created = Result.objects.get_or_create(user=request.user, start_date=instance.start_date,
                                                  end_date=instance.end_date)
            if created:
                result.refrigerant.add(instance)
                result.save()
            if request.headers.get('Hx-Request'):
                return render(request, 'refrigerantmodel-partial.html', {'refrigerants': refrigerants})
            else:
                context = {
                    'form': form,
                    'refrigerants': refrigerants
                }

            return render(request, 'refrigerant_emission_form.html', context)
    else:
        form = RefrigerantEmissionsForm()
    messages.success(request, form.errors)
    refrigerants = RefrigerantModelEmissions.objects.filter(user=request.user).select_related('user').order_by(
        'time_created')
    context = {
        'form': form,
        'refrigerants': refrigerants
    }

    return render(request, 'refrigerant_emission_form.html', context)


@login_required()
def calculate_chp_emissions(request):
    if request.method == 'POST':
        form = EmissionsChpHeatingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            user = CustomUser.objects.get(pk=request.user.pk)
            instance.user = user

            start_date = instance.start_date
            end_date = instance.end_date

            if start_date and end_date and end_date < start_date:
                return render(request, 'chp_emissions_form.html',
                              {'form': form, 'error': 'End date must be bigger than start date'})

            instance.save()
            chps = HeatingModelEmission.objects.filter(user=request.user).select_related('user').order_by(
                'time_created')
            result, created = Result.objects.get_or_create(user=request.user, start_date=instance.start_date,
                                                           end_date=instance.end_date)
            if created:
                result.chp.add(instance)
                result.save()
            if request.headers.get('Hx-Request'):
                return render(request, 'chpmodel-partial.html', {'chps': chps})
            else:
                context = {
                    'form': form,
                    'chps': chps
                }

            return render(request, 'chp_emissions_form.html', context)
    else:
        form = EmissionsChpHeatingForm()
    messages.success(request, form.errors)
    chps = HeatingModelEmission.objects.filter(user=request.user).select_related('user').order_by('time_created')
    context = {
        'form': form,
        'chps': chps
    }
    return render(request, 'chp_emissions_form.html', context)


@login_required()
def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            print(instance.calculate_car_co2_emission())

            # Unpack the tuple returned by get_or_create
            transport, created = TransportModelEmissions.objects.get_or_create(
                start_date=instance.start_date,
                end_date=instance.end_date,
                user=instance.user
            )
            # ignore the created as the car should be added to the transport instance either created or not.
            transport.cars.add(instance)

            #   cars = Car.objects.filter(user=request.user).select_related('user').order_by('time_created')
            transports = TransportModelEmissions.objects.filter(user=request.user).select_related('user')

            result, created = Result.objects.get_or_create(
                user=request.user,
                start_date=instance.start_date,
                end_date=instance.end_date
            )

            if created:
                result.transport.add(transport)
                result.save()

            if request.headers.get('Hx-Request'):
                return render(request, 'transportmodel-partial.html', {'transports': transports})
            else:
                context = {
                    'form': form,
                    'transports': transports
                }

            return render(request, 'create_car.html', context)
    else:
        form = CarForm()

    messages.success(request, form.errors)
    #   cars = Car.objects.filter(user=request.user).select_related('user').order_by('time_created')
    context = {
        'form': form,
        #   'cars': cars,
        'transports': TransportModelEmissions.objects.filter(user=request.user).select_related('user')
    }
    #   transports = TransportModelEmissions.objects.filter(user=request.user).select_related('user')
    return render(request, 'create_car.html', context)


#   def view_emissions1(request, pk):
#       emission = FuelModel.objects.get(pk=pk)
# total_emissions_chart = EmissionsModel.objects.values('fuel').annotate(total_emissions=Sum(
# 'calculate_co2_emissions')) moving_objects_data = EmissionsModel.objects.all().values('start_date',
# 'calculate_co2_emissions')
#       petrol_emissions = emission.calculate_fuel_co2_emissions()
#       electricity_emissions = emission.calculate_co2_emissions_from_electricity()
#       total_emissions = petrol_emissions + electricity_emissions
#       context = {
#           'petrol_emissions': petrol_emissions,
#           'electricity_emissions': electricity_emissions,
#           'total_emissions': total_emissions,
#       }
#       return render(request, 'fuel_result.html', context)

@login_required()
def view_fuel_emissions(request, pk):
    emission = FuelModel.objects.get(pk=pk)
    if emission.calculate_fuel_co2_emissions() < 1000:
        grade = "Low Emissions"
    elif emission.calculate_fuel_co2_emissions() < 3000:
        grade = "Moderate Emissions"
    elif emission.calculate_fuel_co2_emissions() < 6000:
        grade = "High Emissions"
    else:
        grade = "Very High Emissions"

    context = {
        'emission': emission,
        'grade': grade,
    }
    return render(request, 'fuel_result.html', context)


@login_required()
def view_electricity_emissions(request, pk):
    emission = ElectricityModel.objects.get(pk=pk)
    if emission.calculate_co2_emissions_from_electricity() < 1000:
        grade = "Low Emissions"
    elif emission.calculate_co2_emissions_from_electricity() < 3000:
        grade = "Moderate Emissions"
    elif emission.calculate_co2_emissions_from_electricity() < 6000:
        grade = "High Emissions"
    else:
        grade = "Very High Emissions"

    context = {
        'emission': emission,
        'grade': grade,
    }
    return render(request, 'electricity_result.html', context)


@login_required()
def view_waste_emissions(request, pk):
    emission = WasteModel.objects.get(pk=pk)
    if emission.calculate_co2_emissions_from_waste() < 1000:
        grade = "Low Emissions"
    elif emission.calculate_co2_emissions_from_waste() < 3000:
        grade = "Moderate Emissions"
    elif emission.calculate_co2_emissions_from_waste() < 6000:
        grade = "High Emissions"
    else:
        grade = "Very High Emissions"

    context = {
        'emission': emission,
        'emissions_result': round(emission.calculate_co2_emissions_from_waste(), 2),
        'grade': grade,
    }
    return render(request, 'waste_result.html', context)


@login_required()
def view_home_heating_emissions(request, pk):
    emission = HomeHeatingModelEmissions.objects.get(pk=pk)
    if emission.calculate_co2_emissions_from_home_heating_emissions() < 1000:
        grade = "Low Emissions"
    elif emission.calculate_co2_emissions_from_home_heating_emissions() < 3000:
        grade = "Moderate Emissions"
    elif emission.calculate_co2_emissions_from_home_heating_emissions() < 6000:
        grade = "High Emissions"
    else:
        grade = "Very High Emissions"

    context = {
        'emission': emission,
        'emissions_result': round(emission.calculate_co2_emissions_from_home_heating_emissions(), 2),
        'grade': grade,
    }
    return render(request, 'heating_result.html', context)


def get_heating_total_emissions(chp):
    emissions = chp.calculate_co2_emissions_from_heating()
    return emissions.get('total_emissions', 0)  # Extract 'total_emissions' from the dictionary


@login_required()
def view_chp_emissions(request, pk):
    emission = HeatingModelEmission.objects.get(pk=pk)
    if get_heating_total_emissions(emission) < 1000:
        grade = "Low Emissions"
    elif get_heating_total_emissions(emission) < 3000:
        grade = "Moderate Emissions"
    elif get_heating_total_emissions(emission) < 6000:
        grade = "High Emissions"
    else:
        grade = "Very High Emissions"
    result = emission.calculate_co2_emissions_from_heating()

    context = {
        'emission': emission,
        'total_emissions': round(result['total_emissions'], 2),
        'grade': grade,
    }
    return render(request, 'chp_result.html', context)


@login_required()
def view_transport_emissions(request, pk):
    emission = TransportModelEmissions.objects.get(pk=pk)
    emissions_result = emission.calculate_transportation_emission()

    # Determine total emissions based on the returned type
    if isinstance(emissions_result, dict):
        total_emissions = emissions_result.get('Total emissions', 0)
    else:
        total_emissions = emissions_result

    if total_emissions < 1000:
        grade = "Low Emissions"
    elif total_emissions < 3000:
        grade = "Moderate Emissions"
    elif total_emissions < 6000:
        grade = "High Emissions"
    else:
        grade = "Very High Emissions"

    context = {
        'emission': emission,
        'emissions_result': round(emissions_result, 2),
        'grade': grade,
    }
    return render(request, 'transport_result.html', context)


@login_required()
def view_refrigerant_emissions(request, pk):
    emission = RefrigerantModelEmissions.objects.get(pk=pk)
    emissions_result = emission.calculate_refrigerant_emissions()

    # Determine total emissions based on the returned type
    if isinstance(emissions_result, dict):
        total_emissions = emissions_result.get('Total emissions', 0)
    else:
        total_emissions = emissions_result

    if total_emissions < 1000:
        grade = "Low Emissions"
    elif total_emissions < 3000:
        grade = "Moderate Emissions"
    elif total_emissions < 6000:
        grade = "High Emissions"
    else:
        grade = "Very High Emissions"

    context = {
        'emission': emission,
        'emissions_result': round(emissions_result, 2),
        'grade': grade,
    }
    return render(request, 'refrigerant_result.html', context)


@login_required()
def view_results(request):
    results = Result.objects.all()
    context = {
        'results': results
    }
    return render(request, 'result_list.html', context)
