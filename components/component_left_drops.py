from dash import html, dcc
import polars as pl

df_user_ids = pl.read_parquet('data/df_user_ids.parquet')

usuarios = df_user_ids['user_id'].to_list()[:100]
usuarios.append('USUARIO NUEVO')

distancias = ['25 Kilométros', '37 Kilometros', '50 Kilometros']

drop_kilometros = html.Div(
    dcc.Dropdown(
        id="drop-kilometros",
        options=distancias,
        value=distancias[0],
        className="custom-dropdown",
        style={
            "backgroundColor": "#344643",
            "fontSize": 16,
            "color": "#f8efd9",
            "border-radius": "1vh",
        },
    ),
)


# def retorna_drop_ciudades(ciudades: list):
ciudades = [""]
drop_ciudades = html.Div(
    dcc.Dropdown(
        id="drop-ciudades",
        options=ciudades,
        value=ciudades[0],
        disabled=True,
        className="custom-dropdown",
        style={
            "backgroundColor": "#344643",
            "fontSize": 16,
            "color": "#f8efd9",
            "border-radius": "1vh",
        },
    ),
)


drop_usuarios = html.Div(
    dcc.Dropdown(
        id="drop-usuarios",
        options=usuarios,
        value=usuarios[0],
        # className="custom-dropdown",
        style={
            "backgroundColor": "#344643",
            "fontSize": 16,
            "color": "#f8efd9",
            "border-radius": "1vh",
        },
    ),
)
