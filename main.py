from dash import Dash, html, Input, Output, State
import polars as pl
from components.component_left import mapa
from components.component_right import return_state_map
from components.component_left_panel import panel
from functions.retorna_recomendaciones import retorna_recomendaciones

business = pl.read_parquet('data/df_business.parquet')

panel_loaded: bool = False

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    title="Recomendaciones Yelp",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server  # Necesario para Hugging Face


app.config.suppress_callback_exceptions = True


app.layout = html.Div([
    html.Div([
        html.Label("Seleccione el Estado", id='title_map'),
        mapa,
        html.Div([panel], id='left_panel')
    ], id="left_container", className='containers'),
    html.Div([], id="right_container", className='containers')
], id="work_container")


@app.callback(
    Output('drop-ciudades', 'options'),
    Output('drop-ciudades', 'value'),
    Output('drop-ciudades', 'disabled'),
    Output('btn', 'disabled'),
    Input('mapa', 'clickData'),
    Input('mapa', 'selectedData'),
    prevent_initial_call=True,
)
def display_panel(click_data, selected: dict):
    if selected:
        estado = click_data['points'][0]['location']
        mask = business['Estado'] == estado
        lista_ciudades = business.filter(mask)['Ciudad'].unique().to_list()
        lista_ciudades.sort()
        return (lista_ciudades, lista_ciudades[0], False, False)
    else:
        return ([""], "", True, True)


@app.callback(
    Output('right_container', 'children'),
    Output("store_btn", "data"),
    Input('mapa', 'clickData'),
    Input('btn', 'n_clicks'),
    Input('mapa', 'selectedData'),
    State('drop-ciudades', 'value'),
    State('drop-kilometros', 'value'),
    State('drop-usuarios', 'value'),
    State("store_btn", "data"),
    State("tabla_caracteristicas", "selectedRows"),
    State("tabla_categorias", "selectedRows"),
    prevent_initial_call=True,
    suppress_callback_exceptions=True
)
def update_mapa_estado(click_data: dict,
                       n_clicks: int | None,
                       selected: dict,
                       ciudad: str,
                       kilometros: str,
                       usuario: str,
                       data: dict,
                       selected_caracteristicas: list | None,
                       selected_categorias: list | None):
    btn = data.get("btn")
    if not selected:
        return (None, data)

    if not n_clicks or n_clicks == btn:
        return (None, data)

    if n_clicks > btn:
        btn += 1
        data["btn"] = btn
        estado = click_data['points'][0]['location']
        kms = int(kilometros[:3]) if kilometros[:1] == "1" else int(kilometros[:2])
        if selected_categorias == []:
            categorias = []
        else:
            categorias = [selected_categorias[i]['Categoría'] for i in range(len(selected_categorias))]
        if selected_caracteristicas == []:
            caracteristicas = []
        else:
            caracteristicas = [selected_caracteristicas[i]['Característica'] for i in range(len(selected_caracteristicas))]

        recomendaciones, latitud, longitud = retorna_recomendaciones(
            km=kms, ciudad=ciudad, usuario=usuario, caracteristicas=caracteristicas, categorias=categorias, estado=estado
        )

        mapa_estado = return_state_map(ciudad=ciudad, latitud=latitud, longitud=longitud,
                                       recomendaciones=recomendaciones, km=kms)
        return (mapa_estado, data)
    # return (None, data)


if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=8080)
