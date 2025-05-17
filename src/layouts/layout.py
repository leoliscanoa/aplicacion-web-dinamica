"""
Módulo para la definición de los componentes de layout de la aplicación.
Contiene funciones para crear las diferentes secciones del layout.
"""

from dash import html, dcc
from src.utils.utils import create_filter_card, card_style, title_style, button_style, filter_area_style

def create_header():
    """
    Crea el encabezado de la aplicación con un título principal en una tarjeta con estilos innovadores.

    Returns:
        html.Div: Componente de encabezado con título.
    """
    return html.Div([
        html.Div([
            html.H1('📊 Análisis de Mortalidad en Colombia (2019)',
                   style={**title_style, 'margin': '0', 'padding': '20px'})
        ], style={
            'backgroundColor': 'white',
            'borderRadius': '15px',
            'boxShadow': '0 10px 25px rgba(0,0,0,0.1)',
            'margin': '20px 0',
            'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
            'border': '1px solid #e0e0e0'
        })
    ])

def create_map_section(map_fig, manners_of_death, months, genders):
    """
    Crea la sección del mapa con filtros.

    Args:
        map_fig (plotly.graph_objects.Figure): Figura del mapa.
        manners_of_death (list): Lista de maneras de muerte para el filtro.
        months (list): Lista de meses para el filtro.
        genders (list): Lista de géneros para el filtro.

    Returns:
        html.Div: Componente de sección de mapa con filtros.
    """
    return html.Div([
        # Contenedor principal con estilo de tarjeta
        html.Div([
            html.H3("Muertes por Departamento", 
                    style={**title_style, 'marginBottom': '20px'}),

            # Mapa primero
            html.Div([
                dcc.Loading(
                    id="loading-map",
                    type="circle",
                    children=dcc.Graph(id='map-graph', figure=map_fig, style={'height': '700px'})
                )
            ]),

            # Filtros abajo
            html.Div([
                html.H4("Filtros", style={'marginBottom': '15px', 'color': '#2c3e50', 'textAlign': 'center'}),

                # Contenedor horizontal para los filtros
                html.Div([
                    # Filtro de Manera de Muerte
                    create_filter_card("Manera de Muerte", 'map-manner-filter', manners_of_death),

                    # Filtro de Mes
                    create_filter_card("Mes", 'map-month-filter', months),

                    # Filtro de Género
                    create_filter_card("Género", 'map-gender-filter', genders),

                ], style={'display': 'flex', 'flexDirection': 'row', 'gap': '15px', 'justifyContent': 'space-between'})
            ], style={'padding': '15px', 'backgroundColor': '#f5f5f5', 'borderRadius': '10px', 
                      'boxShadow': '0 2px 5px rgba(0,0,0,0.1)', 'marginTop': '20px'})

        ], style={**card_style, 'padding': '20px'})

    ], style={'marginBottom': '40px'})

def create_monthly_deaths_section(monthly_deaths_fig, departments, genders):
    """
    Crea la sección de muertes mensuales con filtros.

    Args:
        monthly_deaths_fig (plotly.graph_objects.Figure): Figura del gráfico de muertes mensuales.
        departments (list): Lista de departamentos para el filtro.
        genders (list): Lista de géneros para el filtro.

    Returns:
        html.Div: Componente de sección de muertes mensuales con filtros.
    """
    return html.Div([
        html.Div([
            dcc.Loading(
                id="loading-monthly-deaths",
                type="circle",
                children=dcc.Graph(id='monthly-deaths-graph', figure=monthly_deaths_fig)
            )
        ]),
        html.Div([
            html.H5('Filtros', style={'marginTop': '10px', 'fontWeight': 'bold', 'color': '#2c3e50', 'textAlign': 'center'}),
            html.Div([
                create_filter_card("Departamento", 'monthly-dept-filter', departments),
                create_filter_card("Género", 'monthly-gender-filter', genders)
            ], style={'display': 'flex', 'gap': '10px', 'justifyContent': 'space-between'})
        ], style=filter_area_style)
    ], style=card_style)

def create_age_histogram_section(age_histogram_fig, departments, genders):
    """
    Crea la sección de histograma de edad con filtros.

    Args:
        age_histogram_fig (plotly.graph_objects.Figure): Figura del histograma de edad.
        departments (list): Lista de departamentos para el filtro.
        genders (list): Lista de géneros para el filtro.

    Returns:
        html.Div: Componente de sección de histograma de edad con filtros.
    """
    return html.Div([
        html.Div([
            dcc.Loading(
                id="loading-age-histogram",
                type="circle",
                children=dcc.Graph(id='age-histogram', figure=age_histogram_fig)
            )
        ]),
        html.Div([
            html.H5('Filtros', style={'marginTop': '10px', 'fontWeight': 'bold', 'color': '#2c3e50', 'textAlign': 'center'}),
            html.Div([
                create_filter_card("Departamento", 'age-dept-filter', departments),
                create_filter_card("Género", 'age-gender-filter', genders)
            ], style={'display': 'flex', 'gap': '10px', 'justifyContent': 'space-between'}),
        ], style=filter_area_style)
    ], style=card_style)

def create_top_causes_section(top_causes_table):
    """
    Crea la sección de tabla de principales causas de muerte.

    Args:
        top_causes_table (dash_table.DataTable): Tabla de principales causas de muerte.

    Returns:
        html.Div: Componente de sección de tabla de principales causas de muerte.
    """
    return html.Div([
        html.H3("Principales Causas de Muerte", style={**title_style, 'marginBottom': '15px'}),
        dcc.Loading(
            id="loading-top-causes",
            type="circle",
            children=top_causes_table
        )
    ], style=card_style)

def create_violent_cities_section(violent_cities_fig, violent_types, genders):
    """
    Crea la sección de ciudades más violentas con filtros.

    Args:
        violent_cities_fig (plotly.graph_objects.Figure): Figura del gráfico de ciudades más violentas.
        violent_types (list): Lista de tipos de muertes violentas para el filtro.
        genders (list): Lista de géneros para el filtro.

    Returns:
        html.Div: Componente de sección de ciudades más violentas con filtros.
    """
    return html.Div([
        html.Div([
            dcc.Loading(
                id="loading-violent-cities",
                type="circle",
                children=dcc.Graph(id='violent-cities-graph', figure=violent_cities_fig)
            )
        ]),
        html.Div([
            html.H5('Filtros', style={'marginTop': '10px', 'fontWeight': 'bold', 'color': '#2c3e50', 'textAlign': 'center'}),
            html.Div([
                create_filter_card("Descripción de Homicidio", 'violent-manner-filter', violent_types),
                create_filter_card("Género", 'violent-gender-filter', genders)
            ], style={'display': 'flex', 'gap': '10px', 'justifyContent': 'space-between'}),
        ], style=filter_area_style)
    ], style=card_style)

def create_lowest_mortality_section(lowest_mortality_fig, genders):
    """
    Crea la sección de ciudades con menor mortalidad con filtros.

    Args:
        lowest_mortality_fig (plotly.graph_objects.Figure): Figura del gráfico de ciudades con menor mortalidad.
        genders (list): Lista de géneros para el filtro.

    Returns:
        html.Div: Componente de sección de ciudades con menor mortalidad con filtros.
    """
    return html.Div([
        html.Div([
            dcc.Loading(
                id="loading-lowest-mortality",
                type="circle",
                children=dcc.Graph(id='lowest-mortality-graph', figure=lowest_mortality_fig)
            )
        ]),
        html.Div([
            html.H5('Filtros', style={'marginTop': '10px', 'fontWeight': 'bold', 'color': '#2c3e50', 'textAlign': 'center'}),
            create_filter_card("Género", 'lowest-gender-filter', genders),
        ], style=filter_area_style)
    ], style=card_style)

def create_gender_dept_section(gender_dept_fig, manners_of_death, months):
    """
    Crea la sección de muertes por género y departamento con filtros.

    Args:
        gender_dept_fig (plotly.graph_objects.Figure): Figura del gráfico de muertes por género y departamento.
        manners_of_death (list): Lista de maneras de muerte para el filtro.
        months (list): Lista de meses para el filtro.

    Returns:
        html.Div: Componente de sección de muertes por género y departamento con filtros.
    """
    return html.Div([
        html.Div([
            dcc.Loading(
                id="loading-gender-dept",
                type="circle",
                children=dcc.Graph(id='gender-dept-graph', figure=gender_dept_fig)
            )
        ]),
        html.Div([
            html.H5('Filtros', style={'marginTop': '10px', 'fontWeight': 'bold', 'color': '#2c3e50', 'textAlign': 'center'}),
            html.Div([
                create_filter_card("Manera de Muerte", 'gender-dept-manner-filter', manners_of_death),
                create_filter_card("Mes", 'gender-dept-month-filter', months)
            ], style={'display': 'flex', 'gap': '10px', 'justifyContent': 'space-between'}),
        ], style=filter_area_style)
    ], style=card_style)

def create_announcement_section():
    """
    Crea un bloque de anuncio indicando que el dashboard es solo para fines educativos.

    Returns:
        html.Div: Componente de anuncio.
    """
    return html.Div([
        html.Div([
            html.H4("Aviso Importante", style={'color': '#2c3e50', 'marginBottom': '10px', 'textAlign': 'center'}),
            html.P("Este dashboard es solo para fines educativos y de visualización.", 
                  style={'fontSize': '16px', 'textAlign': 'center'})
        ], style={'padding': '15px', 'backgroundColor': '#f8d7da', 'borderRadius': '10px', 
                 'border': '1px solid #f5c6cb', 'color': '#721c24'}),
        html.Div([
            html.H4("Autores", style={**title_style, 'marginBottom': '15px'}),
            html.Ul([
                html.Li("- Bechara, Hermes", style={'fontSize': '16px', 'marginBottom': '5px'}),
                html.Li("- Liscano, Andrés", style={'fontSize': '16px', 'marginBottom': '5px'}),
                html.Li("- Montealegre, Efraín", style={'fontSize': '16px', 'marginBottom': '5px'})
            ], style={'listStyleType': 'none', 'padding': '0', 'margin': '0'})
        ], style={**card_style, 'padding': '20px', 'marginBottom': '20px'})
    ], style={'marginBottom': '20px'})

def create_data_sources_section():
    """
    Crea una sección para descargar las fuentes de datos.

    Returns:
        html.Div: Componente de sección de fuentes de datos.
    """
    return html.Div([
        html.H4("Fuentes de Datos", style={**title_style, 'marginBottom': '15px'}),
        html.P("Descargue los datos utilizados en este dashboard:", style={'marginBottom': '15px'}),
        html.Div([
            html.A(
                html.Button("Datos de Mortalidad", style={**button_style, 'marginRight': '10px'}),
                href="/data/NoFetal2019.csv", download="NoFetal2019.csv"
            ),
            html.A(
                html.Button("Códigos de Muerte", style={**button_style, 'marginRight': '10px'}),
                href="/data/CodigosDeMuerte.csv", download="CodigosDeMuerte.csv"
            ),
            html.A(
                html.Button("Datos Divipola", style=button_style),
                href="/data/Divipola.csv", download="Divipola.csv"
            )
        ], style={'display': 'flex', 'justifyContent': 'center'})
    ], style={**card_style, 'padding': '20px', 'marginBottom': '20px'})

def create_layout(map_fig, monthly_deaths_fig, age_histogram_fig, top_causes_table, 
                 violent_cities_fig, lowest_mortality_fig, gender_dept_fig,
                 departments, manners_of_death, months, genders, violent_types=None):
    """
    Crea el layout completo de la aplicación.

    Args:
        map_fig (plotly.graph_objects.Figure): Figura del mapa.
        monthly_deaths_fig (plotly.graph_objects.Figure): Figura del gráfico de muertes mensuales.
        age_histogram_fig (plotly.graph_objects.Figure): Figura del histograma de edad.
        top_causes_table (dash_table.DataTable): Tabla de principales causas de muerte.
        violent_cities_fig (plotly.graph_objects.Figure): Figura del gráfico de ciudades más violentas.
        lowest_mortality_fig (plotly.graph_objects.Figure): Figura del gráfico de ciudades con menor mortalidad.
        gender_dept_fig (plotly.graph_objects.Figure): Figura del gráfico de muertes por género y departamento.
        departments (list): Lista de departamentos para los filtros.
        manners_of_death (list): Lista de maneras de muerte para los filtros.
        months (list): Lista de meses para los filtros.
        genders (list): Lista de géneros para los filtros.
        violent_types (list, optional): Lista de tipos de muertes violentas para el filtro de ciudades más violentas.

    Returns:
        html.Div: Layout completo de la aplicación.
    """
    return html.Div([
        # Header
        create_header(),

        # Map Section
        create_map_section(map_fig, manners_of_death, months, genders),

        # Resto de gráficos en dos columnas con filtros individuales
        html.Div([
            # Columna izquierda
            html.Div([
                # Panel de muertes por mes con filtros
                create_monthly_deaths_section(monthly_deaths_fig, departments, genders),

                # Panel de distribución por edad con filtros
                create_age_histogram_section(age_histogram_fig, departments, genders),

                # Panel de principales causas de muerte
                create_top_causes_section(top_causes_table)

            ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top'}),

            # Columna derecha
            html.Div([
                # Panel de ciudades más violentas con filtros
                create_violent_cities_section(violent_cities_fig, violent_types, genders),

                # Panel de ciudades con menor mortalidad con filtros
                create_lowest_mortality_section(lowest_mortality_fig, genders),

                # Panel de muertes por género y departamento con filtros
                create_gender_dept_section(gender_dept_fig, manners_of_death, months)

            ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '2%'})

        ], style={'marginBottom': '40px'}),

        # Data Sources Section
        create_data_sources_section(),

        # Announcement Section
        create_announcement_section(),
    ])
