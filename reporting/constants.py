REFRIGERANT_CHOICES = (
    ('HFC-23', 11700),
    ('HFC-32', 650),
    ('HFC-125', 2800),
    ('HFC-134a', 1300),
    ('HFC-143a', 3800),
    ('HFC-152a', 140),
    ('HFC-236fa', 6300),
    ('R-401A', 18),
    ('R-401B', 15),
    ('R-401C', 21),
    ('R-402A', 1680),
    ('R-402B', 1064),
    ('R-403A', 1400),
    ('R-403B', 2730),
    ('R-404A', 3260),
    ('R-407A', 1770),
    ('R-407B', 2285),
    ('R-407C', 1526),
    ('R-407D', 1428),
    ('R-407E', 1363),
    ('R-408A', 1944),
    ('R-409A', 0),
    ('R-409B', 0),
    ('R-410A', 1725),
    ('R-410B', 1833),
    ('R-411A', 15),
    ('R-411B', 4),
    ('R-412A', 350),
    ('R-413A', 1774),
    ('R-414A', 0),
    ('R-414B', 0),
    ('R-415A', 25),
    ('R-415B', 105),
)

COAL_TYPE = (
    ('Anthracite', 'Anthracite'),
    ('Bituminous', 'Bituminous'),
    ('Sub-bituminous', 'Sub-bituminous'),
    ('Lignite', 'Lignite'),
    ('None', 'None'),
)

Vehicle = (
    ('Truck', 'Truck'),
    ('Van', 'Van'),
    ('Other', 'Other'),
)

# sources of the emission factors
VEHICLE_EMISSIONS_FACTORS = {
    'Truck': 1.456,  # https://www.ipcc-nggip.iges.or.jp/public/gp/bgp/2_4_Water-borne_Navigation.pdf
    'Van': 0.501,  # https://www.researchgate.net/figure/Referent-values-of-emission-factors-per-vehicle
    # -categories-g-pollutant-kg-fuel_tbl1_335455811
    'Other': 0.368,  # https://www.transportation.gov/sites/dot.gov/files/docs/emissions_analysis_of_freight.pdf
}

FUEL_CHOICES = (
    ('Diesel Oil', 'Diesel Oil'),
    ('LPG', 'LPG'),
    ('Petrol', 'Petrol'),
    ('Coal', 'Coal'),
    ('Other', 'Other'),
)

OXIDATION_FACTOR = (  # IPCC standard  Intergovernmental Panel on Climate Change
    (0.99, 0.99),
    (0.99, 0.99),
    (0.995, 0.995)
)
