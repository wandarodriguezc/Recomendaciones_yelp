from dash import dcc, html
import plotly.express as px
import polars as pl
from components.variables import highlighted_states, nombre_estados

df = pl.DataFrame({
    "State": highlighted_states,
    # Verde oscuro para los estados destacados
    "Color": ["#79b4b7"] * len(highlighted_states),
    # Nombres completos de los estados
    "Nombre": [nombre_estados[state] for state in highlighted_states]
}).to_pandas()  # Convertir a DataFrame de pandas

# Crear el mapa
fig = px.choropleth(df,  # Proporcionar el DataFrame completo
                    locations='State',
                    locationmode="USA-states",
                    color='Color',
                    scope="usa",
                    color_discrete_map="identity",
                    # Mostrar nombres completos en el hover
                    hover_data={'State': False, 'Nombre': True}
                    )

# Configurar el diseño del mapa
fig.update_layout(
    showlegend=False,  # Eliminar la leyenda
    paper_bgcolor='rgba(0,0,0,0)',
    clickmode='event+select',
    margin=dict(t=20, b=0, l=0, r=0),
    hoverlabel=dict(
        bgcolor='white',
        font_size=16,
        font_family='Arial',
        font_color='black',
        bordercolor='black'
    ),
)

# Añadir nombres de los estados
fig.update_geos(
    showlakes=True,
    bgcolor='rgba(0,0,0,0)',
    lakecolor='lightgray',
    showland=True,
    landcolor='lightgray',
    showocean=True,
    oceancolor='#79b4b7',
    showcoastlines=True,
    coastlinecolor='white',
    showframe=True,
    projection_type='albers usa',
    fitbounds="locations",
    visible=True,
)

config = {'displayModeBar': False}
mapa = html.Div([
    dcc.Graph(id='mapa',
              figure=fig,
              style={'width': '100%', 'height': '100%'},
              config=config
              )
], style={'width': '100%',
          'height': '50vh',
          'display': 'flex',
          'justify-content': 'center',
          'align-items': 'center'
          },
    id='container_mapa',
)
