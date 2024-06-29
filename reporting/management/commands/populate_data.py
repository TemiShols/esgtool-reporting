import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from reporting.models import (
    FuelModel, WasteModel, ElectricityModel, HeatingModelEmission,
    HomeHeatingModelEmissions, TransportModelEmissions, RefrigerantModelEmissions, Result, Car
)
from authentication.models import CustomUser


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Create a sample user
        user, created = CustomUser.objects.get_or_create(
            email='sampleuser@example.com',
            defaults={
                'first_name': 'Sample',
                'last_name': 'User',
                'company_name': 'Sample Company',
                'personal_telephone': '123456789',
                'office_telephone': '987654321',
                'address': '123 Sample Street'
            }
        )
        if created:
            user.set_password('password')
            user.save()

        # Populate FuelModel
        for i in range(5):
            FuelModel.objects.create(
                user=user,
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30),
                Af_v=random.uniform(0.5, 2.0),
                Fc_h=random.uniform(0.5, 2.0),
                Fox=random.uniform(0.5, 2.0),
                fuel=random.choice(['Diesel Oil', 'Petrol', 'LPG']),
                coal_type='None'
            )

        # Populate WasteModel
        for i in range(5):
            WasteModel.objects.create(
                user=user,
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30),
                waste_mass=random.uniform(100, 500),
                waste_treatment=random.choice(['Composting', 'Anaerobic Digestion', 'Incineration', 'Landfill']),
                distance_travelled=random.uniform(25, 200),
                vehicle_type=random.choice(['Truck', 'Van', 'Other'])
            )

        # Populate ElectricityModel
        for i in range(5):
            ElectricityModel.objects.create(
                user=user,
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30),
                Af_kw=random.uniform(1000, 5000)
            )

        # Populate HeatingModelEmission (CHP)
        for i in range(5):
            fuel = FuelModel.objects.order_by('?').first()
            HeatingModelEmission.objects.create(
                user=user,
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30),
                fuel=fuel,
                steam_output=random.uniform(10, 50),
                electricity_output=random.uniform(10, 50)
            )

        # Populate HomeHeatingModelEmissions
        for i in range(5):
            HomeHeatingModelEmissions.objects.create(
                user=user,
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30),
                fuel=random.choice(
                    ['Coal', 'Petroleum', 'LPG', 'Geothermal', 'Hydroelectricity', 'Nuclear', 'Solar', 'Wind', 'Diesel Oil']
                ),
                room_size=random.uniform(3, 5),
                fuel_volume=random.uniform(500, 1500)
            )

        # Create Car instances
        car_types = ['passenger_car', 'light_duty_truck', 'medium_heavy_duty_truck']
        fuel_types = ['Diesel Oil', 'Petrol', 'LPG']
        cars = []
        for i in range(10):  # Creating 10 cars
            car = Car.objects.create(
                user=user,
                name=f'Car {i + 1}',
                registration_number=f'ABC{i + 1:03}',
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30),
                type=random.choice(car_types),
                mileage=f'{random.uniform(10, 200):.2f}',
                fuel_type=random.choice(fuel_types),
                fuel_quantity=random.uniform(10, 100)
            )
            cars.append(car)

        # Populate TransportModelEmissions with cars
        for i in range(5):
            transport_model_emissions = TransportModelEmissions.objects.create(
                user=user,
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30),
            )
            transport_model_emissions.cars.set(random.sample(cars, k=3))  # Associate 3 random cars with each transport emission
            transport_model_emissions.save()

        # Populate RefrigerantModelEmissions
        for i in range(5):
            RefrigerantModelEmissions.objects.create(
                user=user,
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30),
                refrigerant=random.choice(
                    ['R-407A', 'R-407B', 'R-407C', 'R-407D', 'R-407E', 'R-408A', 'R-409A', 'R-409B']
                ),
                charge_amount_kg=random.uniform(10, 150),
                leak_rate=random.uniform(10, 150),
                annual_top_up_kg=random.uniform(10, 150),
                disposal_recovery_kg=random.uniform(10, 150),
                retirement_recovery_kg=random.uniform(10, 150),
            )

        # Create a Result instance and associate models
        result, created = Result.objects.get_or_create(
            user=user,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=30)
        )
        result.fuel.set(FuelModel.objects.filter(user=user))
        result.waste.set(WasteModel.objects.filter(user=user))
        result.electricity.set(ElectricityModel.objects.filter(user=user))
        result.chp.set(HeatingModelEmission.objects.filter(user=user))
        result.home_heating.set(HomeHeatingModelEmissions.objects.filter(user=user))
        result.transport.set(TransportModelEmissions.objects.filter(user=user))
        result.refrigerant.set(RefrigerantModelEmissions.objects.filter(user=user))
        result.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data'))
