from dash import dcc, html
import dash_ag_grid as dag
import polars as pl
from components.variables import lista_categorias, lista_caracteristicas
from components.component_left_drops import drop_kilometros, drop_ciudades, drop_usuarios

# df_business = pl.read_parquet('data/df_business.parquet')

panel = html.Div([
    dcc.Store(id="store_btn", data={"btn": 0}),
    html.Div([
        html.Label("Seleciona Categorías", className='mini_titles'),
        dag.AgGrid(
            id='tabla_categorias',
            rowData=lista_categorias,
            columnDefs=[
                {'headerName': 'Categorías',
                    'field': 'Categoría',
                    'checkboxSelection': True,
                    "headerCheckboxSelection": True}
            ],
            className="ag-theme-alpine-dark",
            columnSize="sizeToFit",
            dashGridOptions={
                'rowSelection': 'multiple',
                "animateRows": False
            },
            style={
                'width': '100%',
                'height': '90%',
            },
        ),

    ], id='categorias'),
    html.Div([
        html.Label("Seleciona Características", className='mini_titles'),
        dag.AgGrid(
            id='tabla_caracteristicas',
            rowData=lista_caracteristicas,
            columnDefs=[
                {'headerName': 'Características',
                    'field': 'Característica',
                    'checkboxSelection': True,
                    "headerCheckboxSelection": True}
            ],
            className="ag-theme-alpine-dark",
            columnSize="sizeToFit",
            dashGridOptions={
                'rowSelection': 'multiple',
                "animateRows": False
            },
            style={
                'width': '100%',
                'height': '90%',
            },
        ),
    ], id='caracteristicas'),
    html.Div([
        html.Div([
            html.Div([
                html.Label('Selecciona la Ciudad', className='mini_titles'),
                drop_ciudades,
            ], id='container-drop1'),
            html.Div([
                html.Label('Distancia Máxima', className='mini_titles'),
                drop_kilometros,
            ], id='container-drop2')
        ], id='drops'),
        html.Div([
            html.Label('Codigo de Usuario', className='mini_titles'),
            drop_usuarios,
        ], id='container-drop-usuario'),
        # html.Div([], id='respuesta'),
        html.Div([html.Button('Recomendar', id='btn', disabled=True)], id='botones')
    ], id='estado_kms')
], id='panel')
