import polars as pl
import numpy as np
import pickle
import joblib
import math

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

# DATA, MODELO y MATRICES DE CARACTERISTICAS
df_user_ids = pl.read_parquet('data/df_user_ids.parquet')
new_row = pl.DataFrame({"user_id_int": [0], "user_id": ["USUARIO NUEVO"]})
df_user_ids = df_user_ids.vstack(new_row)

df_business = pl.read_parquet('data/df_business.parquet')
columns_business = df_business.columns

categorias_yelp = pl.read_parquet('data/categorias_yelp.parquet')

data_coordenadas = joblib.load('data/ciudades_dash.joblib')

# ***********************************  MODELO SOLO FUNCIONA EN LINUX
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/user_features.pkl', 'rb') as f:
    user_features = pickle.load(f)

with open('model/item_features.pkl', 'rb') as f:
    item_features = pickle.load(f)
# ******************************************************************************


def distancia_haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia entre dos localidades dadas sus latitudes y longitudes.

    Parámetros:
    lat1 (float): Latitud de la primera localidad (en grados).
    lon1 (float): Longitud de la primera localidad (en grados).
    lat2 (float): Latitud de la segunda localidad (en grados).
    lon2 (float): Longitud de la segunda localidad (en grados).

    Retorna:
    float: Distancia entre las dos localidades en kilómetros.
    """
    # Radio de la Tierra en kilómetros
    radio_tierra = 6371

    # Convertir grados a radianes
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferencias entre latitudes y longitudes
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    # Fórmula de Haversine
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * \
        math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distancia = radio_tierra * c

    return distancia


def retorna_recomendaciones(
        km: int,
        estado: str,
        ciudad: str,
        usuario: str,
        caracteristicas: list,
        categorias: list
):

    # *********************************** USAR SOLO EN LINUX
    mask = df_user_ids['user_id'] == usuario
    user_id = df_user_ids.filter(mask)['user_id_int'][0]
    # ******************************************************

    # CALCULANDO LAS COORDENADAS PROMEDIO DE LA CIUDAD
    data = data_coordenadas[orden_estados[estado]]
    df_coordenadas = pl.DataFrame(data)
    mask = df_coordenadas['City'] == ciudad
    latitud_1 = df_coordenadas.filter(mask)['Latitude'][0]
    longitud_1 = df_coordenadas.filter(mask)['Longitude'][0]

    # OBTENIENDO SOLO LOS NEGOCIOS DE LAS CATEGORIAS SELECCIONADAS
    if len(categorias) > 0:
        mask = categorias_yelp['category_general'].is_in(categorias)
        lista_negocios = categorias_yelp.filter(
            mask)['business_id'].unique().to_list()
        mask = df_business['business_id'].is_in(lista_negocios)
        df_business_seleccionados = df_business.filter(mask)

    # FILTRANDO SEGUN LAS CARACTERISTICAS ESCOGIDAS
    if len(caracteristicas) > 0 and len(categorias) > 0:
        for caracteristica in caracteristicas:
            mask = df_business_seleccionados[caracteristica] == 1
            df_business_seleccionados = df_business_seleccionados.filter(mask)
    elif len(caracteristicas) > 0 and len(categorias) == 0:
        for caracteristica in caracteristicas:
            mask = df_business[caracteristica] == 1
            df_business_seleccionados = df_business.filter(mask)

    if len(caracteristicas) == 0 and len(categorias) == 0:
        df_business_seleccionados = df_business[columns_business]

    # FILTRANDO POR EL ESTADO Y TOMANDO EN CUENTA CUANDO HAY VECINOS
    if estado == 'MO':
        lista_estados = ['MO', 'TN', 'IL']
    elif estado == 'TN':
        lista_estados = ['TN', 'MO']
    elif estado == 'IL':
        lista_estados = ['IL', 'MO', 'IN']
    elif estado == 'IN':
        lista_estados = ['IN', 'IL']
    elif estado in ['PA', 'DE']:
        lista_estados = ['PA', 'DE']
    else:
        lista_estados = [estado]

    mask = df_business_seleccionados['Estado'].is_in(lista_estados)
    df_business_seleccionados = df_business_seleccionados.filter(mask)

    # CALCULANDO DISTANCIAS
    df_business_seleccionados = df_business_seleccionados.with_columns(
        pl.struct(["Latitud", "Longitud"])
        .map_elements(lambda row: round(distancia_haversine(latitud_1, longitud_1, row["Latitud"], row["Longitud"]), 2), return_dtype=pl.Float64)
        .alias("Distancia")
    )

    # FILTRANDO POR DISTANCIA
    mask = df_business_seleccionados['Distancia'] <= km
    df_business_seleccionados = df_business_seleccionados.filter(mask)

    # APLICANDO PROCEDIMIENTO STANDAR DE LIGHTFM PARA OBTENER RECOMENDACIONES
    #  ***************** SOLO CORRE EN LINUX *************************
    business_id_list = df_business_seleccionados['business_id_int'].to_list()
    mask = df_user_ids['user_id'] == usuario
    user_id = df_user_ids.filter(mask)['user_id_int'][0]
    top_n = 5
    scores = model.predict(user_id, business_id_list, item_features=item_features,
                           user_features=user_features, num_threads=5)
    top_items = np.argsort(-scores)[:top_n]
    recomendations = [business_id_list[i] for i in top_items]

    # OBTENIENDO LAS RECOMENDACIONES
    mask = df_business_seleccionados['business_id_int'].is_in(recomendations)
    df_business_seleccionados = df_business_seleccionados.filter(mask)

    return df_business_seleccionados, latitud_1, longitud_1
