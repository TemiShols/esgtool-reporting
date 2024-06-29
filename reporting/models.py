from django.db import models
from django.conf import settings
from .constants import FUEL_CHOICES, COAL_TYPE, Vehicle, VEHICLE_EMISSIONS_FACTORS, REFRIGERANT_CHOICES, \
    TYPE_OF_TRANSPORT

carbon_intensity_gco2_per_kwh = 400  # GCO2 https://ourworldindata.org/grapher/carbon-intensity-electricity also


# check https://www.iea.org/countries/nigeria


# scope1 = "Direct emissions from owned or controlled sources. This includes emissions from combustion in owned or
# controlled boilers, furnaces, vehicles, etc." scope2 = "Indirect emissions from the generation of purchased
# electricity, heat, or steam consumed by the reporting company." scope3 = "All other indirect emissions that occur
# in a company's value chain, including both upstream and downstream emissions. This can include emissions from waste
# disposal, business travel, employee commuting, and more."


class FuelModel(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    fuel = models.CharField(max_length=50, choices=FUEL_CHOICES)
    coal_type = models.CharField(max_length=30, choices=COAL_TYPE)
    Af_v = models.FloatField(null=True, blank=True)  # Volume of fuel consumed(litres)
    Af_m = models.FloatField(null=True, blank=True)  # Mass of fuel consumed
    Af_h = models.FloatField(null=True, blank=True)  # Heat content of fuel consumed
    Fc_v = models.FloatField(null=True, blank=True)  # Carbon content of fuel on a volume basis
    Fc_m = models.FloatField(null=True, blank=True)  # Carbon content of fuel on a mass basis
    Fc_h = models.FloatField(null=True, blank=True)  # Carbon content of fuel on a heating value basis
    Fox = models.FloatField(null=True, blank=True)  # Oxidation factor

    #   total_emissions_monthly = models.IntegerField(null=True, blank=True)
    #   total_carbon_emissions_monthly = models.IntegerField(null=True, blank=True)
    #   total_electricity_emissions_monthly = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.fuel

    def get_density_for_fuel(self):
        # Define a dictionary to store the density for each type of fuel
        fuel_density = {
            'Diesel Oil': 0.85,  # Example density for Diesel Oil (in kg/L)0.82 - 0.86
            'Gas': 0.70,  # Example density for Gas (in kg/L)0.50-0.58
            'Petrol': 0.75,  # Example density for Petrol (in kg/L)0.72-0.77
            # Add densities for other types of fuel as needed
        }

        fuel_value = str(self.fuel)  # Convert the CharField to a string
        return fuel_density.get(fuel_value, 0.0)

    def get_density_for_coal(self):
        # Define a dictionary to store the density for each type of fuel
        coal_density = {
            'Anthracite': 28.0,
            'Bituminous': 25.8,
            'Sub-bituminous': 26.2,
            'Lignite': 27.6
            # Add densities for other types of fuel as needed
        }

        fuel_value = str(self.fuel)  # Convert the CharField to a string
        return coal_density.get(fuel_value, 0.0)

    COAL_TYPE = {
        'Anthracite': 28.0,
        'Bituminous': 25.8,
        'Sub-bituminous': 26.2,
        'Lignite': 27.6
    }

    def get_coal_content_per_volume(self):
        coal_type = str(self.coal_type)
        return self.COAL_TYPE.get(coal_type, )

    def get_coal_content_per_mass(self):
        coal_type = str(self.coal_type)
        return self.COAL_TYPE.get(coal_type, )

        # Method to calculate CO2 emissions

    def calculate_fuel_co2_emissions(self):
        Af_v_value = float(self.Af_v)  # Convert the field value to a float
        Fc_h_value = float(self.Fc_h)  # Convert the field value to a float
        Fox_value = float(self.Fox)  # Convert the field value to a float

        """Let's break down the formula: 
        Af_v_value: The volume of fuel consumed. 
        Fc_h_value: The carbon content of the fuel on a heating value basis, expressed as kilograms of carbon per 
        gigajoule (kgC/GJ) or pounds of carbon per million British thermal units (lbsC/MMBtu).
        Fox_value: The oxidation factor, which accounts for the fraction of carbon in the fuel that is fully oxidized 
        during combustion.
        (44 / 12): This factor converts the mass of carbon to the mass of CO2 by considering the molecular weights of 
        carbon (12) and CO2 (44). When carbon is oxidized, it combines with oxygen to form CO2, and the mass ratio of 
        CO2 to carbon is 44/12.

        The formula is consistent with the IPCC (Intergovernmental Panel on Climate Change) guidelines for 
        calculating CO2 emissions from fuel combustion based on the heating value approach. It's a commonly used 
        approach in greenhouse gas inventories and carbon footprint calculations.

        """

        E = Af_v_value * Fc_h_value * Fox_value * (44 / 12)  # Calculation based on volume
        return E  # kgCO2

        # Method to calculate the heat content of fuel consumed
        # Hv = Calorific value (i.e., heat content) of fuel on a
        # volume basis (e.g., million Btu/ft3 or GJ/L) Hm = Calorific value(i.e., heat content) of fuel on a mass basis(
        # e.g., million Btu / short ton or GJ / metricton)
        # Hm = Calorific value(i.e., heat content) of fuel on a mass basis

    def calculate_heat_content(self, Hv):
        Af_h = float(self.Af_v) * Hv  # Calculation based on volume
        # Perform the other calculation based on mass
        return Af_h


class WasteModel(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    waste_mass = models.FloatField()
    waste_treatment = models.CharField(max_length=50, choices=[
        ('Composting', 'Composting'),
        ('Anaerobic Digestion', 'Anaerobic Digestion'),
        ('Incineration', 'Incineration'),
        ('Landfill', 'Landfill'),
    ])
    #   source_of_waste = models.CharField(max_length=255)
    #   destination_of_waste = models.CharField(max_length=255)
    distance_travelled = models.FloatField()
    vehicle_type = models.CharField(max_length=50, choices=Vehicle, null=True, blank=True)
    # Fields for composting(all provided in the pdf paper i.e calculation of GHG emissions from waste and waste to
    # energy projects)
    compost_ch4_emissions_factor = models.FloatField(default=0.004)
    compost_n2o_emissions_factor = models.FloatField(default=0.0003)

    # Fields for anaerobic digestion
    ad_ch4_emissions_factor = models.FloatField(default=0.001)
    ad_ch4_share_in_biogas = models.FloatField(default=0.6)
    ad_co2_share_in_biogas = models.FloatField(default=0.35)

    # Fields for incineration
    incineration_fossil_carbon_content = models.FloatField(default=0.4)
    incineration_methane_emissions_factor = models.FloatField(default=0.0000002)
    incineration_nitrous_oxide_emissions_factor = models.FloatField(default=0.00005)

    # Fields for landfill
    landfill_methane_correction_factor = models.FloatField(default=0.4)
    landfill_volumetric_ch4_fraction = models.FloatField(default=0.5)
    landfill_oxidation_factor = models.FloatField(default=0.1)
    landfill_ch4_recovery_percentage = models.FloatField(default=0.375)  # 37.5% is the midpoint of the 0-75% range
    landfill_collected_methane_flared = models.FloatField(default=0.5)
    landfill_flare_efficiency = models.FloatField(default=0.9)
    landfill_collected_methane_electricity = models.FloatField(default=0.25)
    landfill_methane_lcv = models.FloatField(default=48)
    landfill_gas_engine_efficiency = models.FloatField(default=0.5)
    landfill_co2_emissions_from_operations = models.FloatField(default=1.2)

    #   def calculate_distance(self):
    #   origin = self.source_of_waste
    #   destination = self.destination_of_waste

    #   origin = get_geocode(origin)
    #   destination = get_geocode(destination)

    #   if not origin or not destination:
    #   return {'error': 'Unable to geocode the given addresses.'}

    #   distance = geodesic(origin, destination).kilometers

    #   return distance

    #   def calculate_transport_emissions(self):
    #   if self.source_of_waste and self.destination_of_waste and self.vehicle_type:
    #   try:
    #   distance = self.calculate_distance()
    #   except ValueError as e:
    #   return {'error':e}
    #   vehicle_type = str(self.vehicle_type)
    #   emissions_factor = VEHICLE_EMISSIONS_FACTORS.get(vehicle_type, 0)
    #   if isinstance(distance, dict):
    #   return {'error': 'Unable to geocode the given addresses.'}
    #   transport_emissions = distance * emissions_factor
    #   return transport_emissions
    #   return 0

    def calculate_transport_emissions(self):
        if self.distance_travelled and self.vehicle_type:
            distance = float(self.distance_travelled)
            vehicle_type = str(self.vehicle_type)
            emissions_factor = VEHICLE_EMISSIONS_FACTORS.get(vehicle_type, 0)
            transport_emissions = distance * emissions_factor
            return transport_emissions

    def calculate_co2_emissions_from_waste(self):
        waste_mass = self.waste_mass
        compost_ch4_emissions_factor = self.compost_ch4_emissions_factor
        compost_n2o_emissions_factor = self.compost_n2o_emissions_factor
        ad_ch4_emissions_factor = self.ad_ch4_emissions_factor
        ad_ch4_share_in_biogas = self.ad_ch4_share_in_biogas
        ad_co2_share_in_biogas = self.ad_co2_share_in_biogas
        incineration_fossil_carbon_content = self.incineration_fossil_carbon_content
        incineration_methane_emissions_factor = self.incineration_methane_emissions_factor
        incineration_nitrous_oxide_emissions_factor = self.incineration_nitrous_oxide_emissions_factor
        landfill_collected_methane_flared = self.landfill_collected_methane_flared
        landfill_flare_efficiency = self.landfill_flare_efficiency
        landfill_collected_methane_electricity = self.landfill_collected_methane_electricity
        landfill_methane_lcv = self.landfill_methane_lcv
        landfill_gas_engine_efficiency = self.landfill_gas_engine_efficiency
        landfill_co2_emissions_from_operations = self.landfill_co2_emissions_from_operations
        landfill_methane_correction_factor = self.landfill_methane_correction_factor
        landfill_volumetric_ch4_fraction = self.landfill_volumetric_ch4_fraction
        landfill_ch4_recovery_percentage = self.landfill_ch4_recovery_percentage
        landfill_oxidation_factor = self.landfill_oxidation_factor

        if self.waste_treatment == 'Composting':
            ch4_emissions = float(waste_mass) * float(compost_ch4_emissions_factor)
            n2o_emissions = float(waste_mass) * float(compost_n2o_emissions_factor)
            total_emissions = ch4_emissions + (n2o_emissions * 310)

        elif self.waste_treatment == 'AnaerobicDigestion':
            ch4_emissions = float(waste_mass) * float(ad_ch4_emissions_factor)
            ch4_share_in_biogas = float(ad_ch4_share_in_biogas)
            co2_share_in_biogas = float(ad_co2_share_in_biogas)
            total_emissions = (ch4_emissions * 21) + (
                    (float(waste_mass) - ch4_emissions) * co2_share_in_biogas * 44 / 12)

        elif self.waste_treatment == 'Incineration':
            fossil_carbon_content = float(waste_mass) * float(incineration_fossil_carbon_content)
            ch4_emissions = float(waste_mass) * float(incineration_methane_emissions_factor)
            n2o_emissions = float(waste_mass) * float(incineration_nitrous_oxide_emissions_factor)
            total_emissions = (fossil_carbon_content * 91.7) + (ch4_emissions * 21) + (n2o_emissions * 310)

        elif self.waste_treatment == 'Landfill':
            # Methane correction factor (MCF)
            # This factor is used to estimate the methane generation potential of the waste.
            # The MCF ranges from 0.4 to 1.0.
            mcf = float(landfill_methane_correction_factor)
            # Volumetric CH4 fraction in landfill gas (F)
            # This fraction represents the methane content in the landfill gas.
            # The F factor ranges from 40% to 60%.
            f = float(landfill_volumetric_ch4_fraction)
            # Volume of CH4 recovered per year for energy use or flaring (RG)
            # This parameter represents the volume of methane recovered for energy use or flaring.
            # The RG factor can be between 0% and 75% of the total CH4 produced.
            rg = float(landfill_ch4_recovery_percentage)
            # Fraction of CH4 released that is oxidised below surface within the site (OX)
            # This factor represents the fraction of methane that is oxidized within the landfill site.
            # The OX factor ranges from 0% to 10%.
            ox = float(landfill_oxidation_factor)
            collected_methane_flared = float(landfill_collected_methane_flared)
            flare_efficiency = float(landfill_flare_efficiency)
            collected_methane_electricity = float(landfill_collected_methane_electricity)
            methane_lcv = float(landfill_methane_lcv)
            gas_engine_efficiency = float(landfill_gas_engine_efficiency)
            co2_emissions_from_operations = float(landfill_co2_emissions_from_operations)

            flared_methane_emissions = collected_methane_flared * (mcf * f * rg * 21 * (1 - flare_efficiency))
            electricity_generated_emissions = collected_methane_electricity * (
                    mcf * f * rg * 21 * (gas_engine_efficiency / 100))

            ghg_emissions = (mcf * f * (
                    1 - rg - ox) * 21) + co2_emissions_from_operations + flared_methane_emissions + electricity_generated_emissions

            # Convert methane emissions to CO2 equivalent using the methane LCV
            methane_co2_equiv = flared_methane_emissions + electricity_generated_emissions
            co2_equiv = methane_co2_equiv * (methane_lcv / 48)  # 48 MJ/kg is the LCV of methane

            ghg_emissions += co2_equiv

            total_emissions = ghg_emissions

        else:
            total_emissions = 0
        transport_emissions = self.calculate_transport_emissions()
        total_emissions += transport_emissions
        return total_emissions


class ElectricityModel(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    Af_kw = models.FloatField(null=True, blank=True)  # Electricity consumption in kilowatt-hours (kWh)

    def calculate_co2_emissions_from_electricity(self):
        """
        Calculate CO2 emissions from electricity consumption.

        Args:
        - electricity_consumption_kwh (float): Electricity consumption in kilowatt-hours (kWh).
        - carbon_intensity_gco2_per_kwh (float): Carbon intensity of electricity in grams of CO2 per kWh (gCO2/kWh).

        Returns:
        - co2_emissions_kg (float): CO2 emissions in kilograms (kg).
        """
        # Calculate CO2 emissions
        co2_emissions_kg = float(self.Af_kw) * (carbon_intensity_gco2_per_kwh / 1000)  # Convert grams to kilograms

        return co2_emissions_kg


class HeatingModelEmission(models.Model):  # CHP
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    fuel = models.CharField(max_length=50, choices=FUEL_CHOICES)
    fuel_volume = models.FloatField(default=15.0)
    steam_output = models.FloatField(help_text="Steam output in GJ")
    electricity_output = models.FloatField(help_text="Electricity output in GJ")
    steam_efficiency = models.FloatField(default=0.8, help_text="Steam efficiency as a decimal")
    electricity_efficiency = models.FloatField(default=0.35, help_text="Electricity efficiency as a decimal")

    def get_density_for_fuel(self):
        # Define a dictionary to store the density for each type of fuel
        fuel_density = {
            'Diesel Oil': 0.85,  # Example density for Diesel Oil (in kg/L)0.82 - 0.86
            'Gas': 0.70,  # Example density for Gas (in kg/L)0.50-0.58
            'Petrol': 0.75,  # Example density for Petrol (in kg/L)0.72-0.77
            'LPG': 0.54,  # Example density for LPG (in kg/L)
            'Coal': 1.25,
        }

        fuel_value = str(self.fuel)  # Convert the CharField to a string
        return fuel_density.get(fuel_value, 0.0)

    def calculate_total_emissions(self):
        if self.fuel_volume is not None:
            Af_v_value = float(self.fuel_volume)  # Volume of fuel consumed (litres)
            if self.fuel == 'Petrol':
                Fc_h_value = 2.31
                Fox_value = 0.99
            elif self.fuel == 'Diesel Oil':
                Fc_h_value = 2.68
                Fox_value = 0.99
            elif self.fuel == 'LPG':
                Fc_h_value = 1.96
                Fox_value = 0.995
            elif self.fuel == 'Coal':
                Fc_h_value = 25.8
                Fox_value = 0.98
            else:
                raise ValueError("Invalid fuel type")

            # Calculation based on volume
            E = Af_v_value * Fc_h_value * Fox_value * (44 / 12)

            return E

        raise ValueError("Missing necessary fields to calculate emissions")

    def calculate_co2_emissions_from_heating(self):
        total_emissions = self.calculate_total_emissions()
        H = float(self.steam_output)
        P = float(self.electricity_output)
        eH = float(self.steam_efficiency)
        eP = float(self.electricity_efficiency)
        ET = total_emissions

        EH = ET * H / (H + P * (eH / eP))
        EP = ET - EH

        steam_emission_rate = EH / H
        electricity_emission_rate = EP / P

        data = {
            'steam_emissions': EH,
            'electricity_emissions': EP,
            'steam_emission_rate': steam_emission_rate,
            'electricity_emission_rate': electricity_emission_rate,
            'total_emissions': EH + EP
        }
        return data

    def return_total_emissions(self):
        result = self.calculate_co2_emissions_from_heating()
        return result['total_emissions']

    def __str__(self):
        return f"HeatingModelEmission from {self.start_date} to {self.end_date}"


FUEL_TYPE = (
    ('Coal', 'Coal'),
    ('Petroleum', 'Petroleum'),
    ('LPG', 'LPG'),
    ('Geothermal', 'Geothermal'),
    ('Hydroelectricity', 'Hydroelectricity'),
    ('Nuclear', 'Nuclear'),
    ('Solar', 'Solar'),
    ('Wind', 'Wind'),
    ('Diesel Oil', 'Diesel Oil'),
)


class HomeHeatingModelEmissions(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    room_size = models.FloatField()  # square meters
    fuel = models.CharField(max_length=50, choices=FUEL_TYPE)
    fuel_volume = models.FloatField()  # litres

    def get_carbon_intensity(self):  # https://mlco2.github.io/codecarbon/methodology.html#carbon-intensity
        intensity = {
            'Coal': 995,
            'Petroleum': 816,
            'LPG': 743,
            'Geothermal': 38,
            'Hydroelectricity': 26,
            'Nuclear': 29,
            'Solar': 48,
            'Wind': 26,
            'Diesel Oil': 830
        }
        fuel_type = str(self.fuel)
        return intensity.get(fuel_type, 0.0)

    def calculate_co2_emissions_from_home_heating_emissions(self):
        emissions = float(self.fuel_volume) * self.get_carbon_intensity() / 1000 * float(self.room_size)
        return emissions  # KGCO2


class TransportModelEmissions(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    cars = models.ManyToManyField('Car')

    def calculate_transportation_emission(self):
        total = 0
        for car in self.cars.all():
            total += car.calculate_car_co2_emission()
        return total


# Regrigeration/AC equipment # https://ghgprotocol.org/calculation-tools-and-guidance

class RefrigerantModelEmissions(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    refrigerant = models.CharField(max_length=50, choices=[(r[0], r[0]) for r in REFRIGERANT_CHOICES])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    charge_amount_kg = models.FloatField()  # the initial charge of refrigerant in kilograms.
    leak_rate = models.FloatField()  # expected annual leak rate as a percentage.
    annual_top_up_kg = models.FloatField()  # amount of refrigerant added annually to top up for leaks.
    disposal_recovery_kg = models.FloatField()  # amount of refrigerant recovered during the disposal of the equipment.
    retirement_recovery_kg = models.FloatField(null=True, blank=True)  # amount of refrigerant recovered when the

    # equipment is retired.

    def get_gwp(self):
        for refrigerant in REFRIGERANT_CHOICES:
            if refrigerant[0] == self.refrigerant:
                return refrigerant[1]
        return 0

    def calculate_refrigerant_emissions(self):
        installation_emissions = float(self.charge_amount_kg) * float(self.leak_rate)
        use_emissions = float(self.annual_top_up_kg)
        disposal_emissions = float(self.charge_amount_kg) - float(self.disposal_recovery_kg)
        retirement_emissions = float(self.charge_amount_kg) - float(self.retirement_recovery_kg)

        total_emissions_kg = installation_emissions + use_emissions + disposal_emissions + retirement_emissions
        total_emissions_tonnes = total_emissions_kg / 1000  # Convert to tonnes
        co2_equivalent_emissions = total_emissions_tonnes * self.get_gwp()

        return co2_equivalent_emissions

    def __str__(self):
        return self.refrigerant


class Result(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    result_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    fuel = models.ManyToManyField(FuelModel)
    electricity = models.ManyToManyField(ElectricityModel)
    waste = models.ManyToManyField(WasteModel)
    chp = models.ManyToManyField(HeatingModelEmission)
    home_heating = models.ManyToManyField(HomeHeatingModelEmissions)
    transport = models.ManyToManyField(TransportModelEmissions)
    refrigerant = models.ManyToManyField(RefrigerantModelEmissions)


class Car(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=25)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    registration_number = models.CharField(max_length=9)
    type = models.CharField(max_length=55, choices=TYPE_OF_TRANSPORT)
    mileage = models.CharField(max_length=7)
    fuel_type = models.CharField(max_length=50, choices=FUEL_CHOICES)
    fuel_quantity = models.FloatField()

    def __str__(self):
        return self.name

    def get_density_for_fuel(self, fuel_type):
        # Define a dictionary to store the density for each type of fuel
        fuel_density = {
            'Diesel Oil': 0.85,  # Example density for Diesel Oil (in kg/L)0.82 - 0.86
            'Gas': 0.70,  # Example density for Gas (in kg/L)0.50-0.58
            'Petrol': 0.75,  # Example density for Petrol (in kg/L)0.72-0.77
            # Add densities for other types of fuel as needed
        }

        return fuel_density.get(fuel_type, 0.0)

    def calculate_car_co2_emission(self):
        distance = float(self.mileage)
        quantity = float(self.fuel_quantity)

        Fc_h_value = 0
        Fox_value = 0
        co2_emissions_based_on_distance = 0

        if self.fuel_type == 'Diesel Oil':
            Fc_h_value = 2.68
            Fox_value = 0.99
            if self.type == 'passenger_car':
                co2_emissions_based_on_distance = distance * 0.368
            elif self.type == 'light_duty_truck':
                co2_emissions_based_on_distance = distance * 0.501
            elif self.type == 'medium_heavy_duty_truck':
                co2_emissions_based_on_distance = distance * 1.456
        elif self.fuel_type == 'Petrol':
            Fc_h_value = 2.31
            Fox_value = 0.99
            if self.type == 'passenger_car':
                co2_emissions_based_on_distance = distance * 0.368
            elif self.type == 'light_duty_truck':
                co2_emissions_based_on_distance = distance * 0.501
            elif self.type == 'medium_heavy_duty_truck':
                co2_emissions_based_on_distance = distance * 1.456
        elif self.fuel_type == 'LPG':
            Fc_h_value = 1.96
            Fox_value = 0.995
            if self.type == 'passenger_car':
                co2_emissions_based_on_distance = distance * 0.368
            elif self.type == 'light_duty_truck':
                co2_emissions_based_on_distance = distance * 0.501
            elif self.type == 'medium_heavy_duty_truck':
                co2_emissions_based_on_distance = distance * 1.456

        co2_emission_based_on_fuel = self.get_density_for_fuel(self.fuel_type) * quantity * Fc_h_value * Fox_value * (
                    44 / 12)
        total_co2_emissions = co2_emissions_based_on_distance + co2_emission_based_on_fuel
        return total_co2_emissions
