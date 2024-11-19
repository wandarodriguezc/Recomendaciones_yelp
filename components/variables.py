orden_estados = {
    'AZ': 0,
    'CA': 1,
    'DE': 2,
    'FL': 3,
    'ID': 4,
    'IL': 5,
    'IN': 6,
    'LA': 7,
    'MO': 8,
    'NV': 9,
    'PA': 10,
    'TN': 11
}

nombre_estados = {
    'AZ': "Arizona",
    'CA': "California",
    'DE': "Delaware",
    'FL': "Florida",
    'ID': "Idaho",
    'IL': "Illinois",
    'IN': "Indiana",
    'LA': "Louisiana",
    'MO': "Missouri",
    'NV': "Nevada",
    'PA': "Pennsylvania",
    'TN': "Tennessee"
}


# Lista de estados de interés
highlighted_states = ['AZ', 'CA', 'DE', 'FL',
                      'ID', 'IL', 'IN', 'LA', 'MO', 'NV', 'PA', 'TN']
rest_of_states = ["AL", "AK", "AR", "CO", "CT", "DC", "GA", "HI", "IA", "KS", "KY", "ME", "MD",
                  "MA", "MI", "MN", "MS", "MT", "NE", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
                  "OK", "OR", "RI", "SC", "SD", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


# Coordenadas centrales para cada estado
state_coords = {
    'CA': {'lat': 36.7783, 'lon': -119.4179},
    'AZ': {'lat': 34.0489, 'lon': -111.0937},
    'DE': {'lat': 38.9108, 'lon': -75.5277},
    'FL': {'lat': 27.9944, 'lon': -81.7603},
    'ID': {'lat': 44.0682, 'lon': -114.7420},
    'IL': {'lat': 40.6331, 'lon': -89.3985},
    'IN': {'lat': 40.2672, 'lon': -86.1349},
    'LA': {'lat': 30.9843, 'lon': -91.9623},
    'MO': {'lat': 37.9643, 'lon': -91.8318},
    'NV': {'lat': 38.8026, 'lon': -116.4194},
    'PA': {'lat': 41.2033, 'lon': -77.1945},
    'TN': {'lat': 35.5175, 'lon': -86.5804}
}


prueba_ciudades = {
    'AZ': "Tucson",
    'CA': "Santa Barbara",
    'DE': "New Castle",
    'FL': "Tampa",
    'ID': "Garden City",
    'IL': "Columbia",
    'IN': "Indianapolis",
    'LA': "Harvey",
    'MO': "Saint Louis",
    'NV': "Virginia City",
    'PA': "Philadelphia",
    'TN': "Springfield"
}

lista_categorias = [
    {'Categoría': 'JAPONESA - ASIATICA'},
    {'Categoría': 'BARES - CERVECERIAS - TAPAS'},
    {'Categoría': 'RESTAURANTES GENERALES'},
    {'Categoría': 'MEDITERRANEA'},
    {'Categoría': 'PIZZERIAS'},
    {'Categoría': 'GRILL - ASADOS - CARNES'},
    {'Categoría': 'MEXICANA'},
    {'Categoría': 'COMIDA RAPIDA'},
    {'Categoría': 'CAFETERIAS - COMIDAS LIGERAS'},
    {'Categoría': 'COCINA INTERNACIONAL'},
    {'Categoría': 'DIETA - VEGANA - ENSALADAS'}
]

diccionario_renombres = {'BusinessAcceptsCreditCards': 'Acepta Tarjeta Credito',
                         'RestaurantsDelivery': 'Servicio de Delivery',
                         'RestaurantsTakeOut': 'Servicio para llevar',
                         'WheelchairAccessible': 'Accesibilidad para Sillas de Rueda',
                         'BikeParking': 'Parqueadero de Bicicletas',
                         'GoodForKids': 'Apropiado para niños',
                         'DogsAllowed': 'Acepta Mascotas'
                         }

lista_caracteristicas = [
    {'Característica': 'ACEPTA TARJETA DE CREDITO'},
    {'Característica': 'SERVICIO DE DELIVERY'},
    {'Característica': 'SERVICIO PARA LLEVAR'},
    {'Característica': 'ACCESIBILIDAD SILLAS DE RUEDA'},
    {'Característica': 'ESTACIONAMIENTO BICICLETAS'},
    {'Característica': 'APROPIADO PARA NIÑOS'},
    {'Característica': 'ACEPTA MASCOTAS'}
]
