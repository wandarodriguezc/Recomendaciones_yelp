from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import polars as pl

# from components.variables import state_coords

columnas = ['Negocio', 'Estado', 'Ciudad', 'Direción', 'Latitud', 'Longitud', 'Lunes',
            'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo', 'Distancia']


def return_state_map(ciudad: str, km: int, latitud: float, longitud: float,
                     recomendaciones: pl.DataFrame) -> dcc.Graph:

    recomendaciones = recomendaciones[columnas]
    recomendaciones = recomendaciones.rename({'Direción': 'Dirección'})

    # Crear la columna de texto para el hover
    recomendaciones = recomendaciones.with_columns(
        (pl.col("Negocio") + "<br>" +
         pl.col("Dirección")
         + "<br>Lunes: " + pl.col("Lunes")
         + "<br>Martes: " + pl.col("Martes")
         + "<br>Miércoles: " + pl.col("Miercoles")
         + "<br>Jueves: " + pl.col("Jueves")
         + "<br>Viernes: " + pl.col("Viernes")
         + "<br>Sábado: " + pl.col("Sabado")
         + "<br>Domingo: " + pl.col("Domingo")
         + "<br>Distancia: " + pl.col("Distancia").cast(pl.String) + " Kms"
         + "<br>Latitud: " + pl.col("Latitud").cast(pl.String)
         + "<br>Longitud: " + pl.col("Longitud").cast(pl.String)).alias("hover_text")
    )

    df2 = pl.DataFrame({'Ciudad': [ciudad], 'Latitud': [
                       latitud], 'Longitud': [longitud]})

    # Crear el círculo
    theta = np.linspace(0, 2 * np.pi, 100)
    # 1 grado de latitud ~ 111 km
    circle_lat = latitud + (km / 111) * np.cos(theta)
    circle_lon = longitud + \
        (km / (111 * np.cos(np.radians(latitud)))) * np.sin(theta)

    fig = px.scatter_mapbox(
        df2,
        lat="Latitud",
        lon="Longitud",
        hover_name="Ciudad",
        size_max=15,
        # center=state_coords[estado]
        center={"lat": latitud, "lon": longitud}
    )

    fig.add_trace(go.Scattermapbox(
        lat=circle_lat,
        lon=circle_lon,
        mode='lines',
        fill='toself',
        fillcolor='rgba(0, 0, 255, 0.1)',  # Color de la sombra
        line=dict(color='blue')
    ))

    # Añadir puntos rojos para las recomendaciones
    fig.add_trace(go.Scattermapbox(
        lat=recomendaciones['Latitud'],
        lon=recomendaciones['Longitud'],
        mode='markers',
        marker=dict(size=8, color='red'),
        text=recomendaciones['hover_text'],
        hoverinfo='text'
    ))

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(
        hoverlabel=dict(
            font_size=16,
            font_color="white",
            # bgcolor="black"
        ),
        showlegend=False
    )

    fig.update_layout(clickmode='event+select')

    fig.update_layout(mapbox_zoom=8)
    config = {'displayModeBar': False}
    mapa_estado = dcc.Graph(id='mapa_estado',
                            figure=fig,
                            config=config,
                            style={'width': '100%', 'height': '100%'})

    return mapa_estado
