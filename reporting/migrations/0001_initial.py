# Generated by Django 3.2.5 on 2024-05-31 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectricityModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('Af_kw', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FuelModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('fuel', models.CharField(choices=[('Diesel Oil', 'Diesel Oil'), ('LPG', 'LPG'), ('Petrol', 'Petrol'), ('Coal', 'Coal'), ('Other', 'Other')], max_length=50)),
                ('coal_type', models.CharField(choices=[('Anthracite', 'Anthracite'), ('Bituminous', 'Bituminous'), ('Sub-bituminous', 'Sub-bituminous'), ('Lignite', 'Lignite'), ('None', 'None')], max_length=30)),
                ('Af_kw', models.FloatField(blank=True, null=True)),
                ('Af_v', models.FloatField(blank=True, null=True)),
                ('Af_m', models.FloatField(blank=True, null=True)),
                ('Af_h', models.FloatField(blank=True, null=True)),
                ('Fc_v', models.FloatField(blank=True, null=True)),
                ('Fc_m', models.FloatField(blank=True, null=True)),
                ('Fc_h', models.FloatField(blank=True, null=True)),
                ('Fox', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HeatingModelEmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('steam_output', models.FloatField(help_text='Steam output in GJ')),
                ('electricity_output', models.FloatField(help_text='Electricity output in GJ')),
                ('steam_efficiency', models.FloatField(default=0.8, help_text='Steam efficiency as a decimal')),
                ('electricity_efficiency', models.FloatField(default=0.35, help_text='Electricity efficiency as a decimal')),
                ('fuel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='reporting.fuelmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HomeHeatingModelEmissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('room_size', models.FloatField()),
                ('fuel', models.CharField(choices=[('Coal', 'Coal'), ('Petroleum', 'Petroleum'), ('LPG', 'LPG'), ('Geothermal', 'Geothermal'), ('Hydroelectricity', 'Hydroelectricity'), ('Nuclear', 'Nuclear'), ('Solar', 'Solar'), ('Wind', 'Wind')], max_length=50)),
                ('fuel_volume', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RefrigerantModelEmissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('refrigerant', models.CharField(choices=[('HFC-23', 'HFC-23'), ('HFC-32', 'HFC-32'), ('HFC-125', 'HFC-125'), ('HFC-134a', 'HFC-134a'), ('HFC-143a', 'HFC-143a'), ('HFC-152a', 'HFC-152a'), ('HFC-236fa', 'HFC-236fa'), ('R-401A', 'R-401A'), ('R-401B', 'R-401B'), ('R-401C', 'R-401C'), ('R-402A', 'R-402A'), ('R-402B', 'R-402B'), ('R-403A', 'R-403A'), ('R-403B', 'R-403B'), ('R-404A', 'R-404A'), ('R-407A', 'R-407A'), ('R-407B', 'R-407B'), ('R-407C', 'R-407C'), ('R-407D', 'R-407D'), ('R-407E', 'R-407E'), ('R-408A', 'R-408A'), ('R-409A', 'R-409A'), ('R-409B', 'R-409B'), ('R-410A', 'R-410A'), ('R-410B', 'R-410B'), ('R-411A', 'R-411A'), ('R-411B', 'R-411B'), ('R-412A', 'R-412A'), ('R-413A', 'R-413A'), ('R-414A', 'R-414A'), ('R-414B', 'R-414B'), ('R-415A', 'R-415A'), ('R-415B', 'R-415B')], max_length=50)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('charge_amount_kg', models.FloatField()),
                ('leak_rate', models.FloatField()),
                ('annual_top_up_kg', models.FloatField()),
                ('disposal_recovery_kg', models.FloatField()),
                ('retirement_recovery_kg', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WasteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('waste_mass', models.FloatField()),
                ('waste_treatment', models.CharField(choices=[('Composting', 'Composting'), ('Anaerobic Digestion', 'Anaerobic Digestion'), ('Incineration', 'Incineration'), ('Landfill', 'Landfill')], max_length=50)),
                ('source_of_waste', models.CharField(max_length=255)),
                ('destination_of_waste', models.CharField(max_length=255)),
                ('vehicle_type', models.CharField(blank=True, choices=[('Truck', 'Truck'), ('Van', 'Van'), ('Other', 'Other')], max_length=50, null=True)),
                ('compost_ch4_emissions_factor', models.FloatField(default=0.004)),
                ('compost_n2o_emissions_factor', models.FloatField(default=0.0003)),
                ('ad_ch4_emissions_factor', models.FloatField(default=0.001)),
                ('ad_ch4_share_in_biogas', models.FloatField(default=0.6)),
                ('ad_co2_share_in_biogas', models.FloatField(default=0.35)),
                ('incineration_fossil_carbon_content', models.FloatField(default=0.4)),
                ('incineration_methane_emissions_factor', models.FloatField(default=2e-07)),
                ('incineration_nitrous_oxide_emissions_factor', models.FloatField(default=5e-05)),
                ('landfill_methane_correction_factor', models.FloatField(default=0.4)),
                ('landfill_volumetric_ch4_fraction', models.FloatField(default=0.5)),
                ('landfill_oxidation_factor', models.FloatField(default=0.1)),
                ('landfill_ch4_recovery_percentage', models.FloatField(default=0.375)),
                ('landfill_collected_methane_flared', models.FloatField(default=0.5)),
                ('landfill_flare_efficiency', models.FloatField(default=0.9)),
                ('landfill_collected_methane_electricity', models.FloatField(default=0.25)),
                ('landfill_methane_lcv', models.FloatField(default=48)),
                ('landfill_gas_engine_efficiency', models.FloatField(default=0.5)),
                ('landfill_co2_emissions_from_operations', models.FloatField(default=1.2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransportModelEmissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('type', models.CharField(choices=[('passenger_car', 'Passenger Car'), ('light_duty_truck', 'Light-duty Truck'), ('medium_heavy_duty_truck', 'Medium- and Heavy-duty Truck'), ('short_haul_air', 'Short Haul Air'), ('medium_haul_air', 'Medium Haul Air'), ('long_haul_air', 'Long Haul Air'), ('intercity_rail', 'Intercity Rail'), ('commuter_rail', 'Commuter Rail'), ('freight_rail', 'Freight Rail'), ('marine_shipping', 'Marine Shipping')], max_length=30)),
                ('mileage', models.CharField(blank=True, max_length=7, null=True)),
                ('source', models.CharField(blank=True, max_length=255, null=True)),
                ('destination', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result_updated', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('chp', models.ManyToManyField(to='reporting.HeatingModelEmission')),
                ('electricity', models.ManyToManyField(to='reporting.ElectricityModel')),
                ('fuel', models.ManyToManyField(to='reporting.FuelModel')),
                ('home_heating', models.ManyToManyField(to='reporting.HomeHeatingModelEmissions')),
                ('refrigerant', models.ManyToManyField(to='reporting.RefrigerantModelEmissions')),
                ('transport', models.ManyToManyField(to='reporting.TransportModelEmissions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('waste', models.ManyToManyField(to='reporting.WasteModel')),
            ],
        ),
    ]
