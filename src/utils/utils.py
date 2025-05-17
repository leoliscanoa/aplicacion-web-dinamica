"""
Módulo de utilidades para la aplicación de análisis de mortalidad.
Contiene funciones de utilidad reutilizables en toda la aplicación.
"""

from dash import html, dcc

def create_filter_card(title, filter_id, options, multi=True):
    """
    Crea un componente de tarjeta de filtro con un título y un dropdown.

    Args:
        title (str): Título del filtro que se mostrará en la tarjeta.
        filter_id (str): ID único para el componente dropdown.
        options (list): Lista de opciones disponibles para el dropdown.
        multi (bool, optional): Indica si se permiten selecciones múltiples. Por defecto es True.

    Returns:
        html.Div: Componente de tarjeta de filtro con un dropdown.
    """
    return html.Div([
        html.H5(title, style={'marginBottom': '10px', 'fontWeight': 'bold', 'color': '#2c3e50', 'textAlign': 'center'}),
        dcc.Dropdown(
            id=filter_id,
            options=[{'label': opt, 'value': opt} for opt in options],
            multi=multi,
            placeholder=f'Seleccionar {title.lower()}...',
            style={'width': '100%', 'zIndex': '9999'}
        )
    ], style={'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '10px', 'marginBottom': '15px',
              'boxShadow': '0 4px 8px rgba(0,0,0,0.1)', 'flex': '1'})

# Estilo global para todos los dropdowns
dropdown_style = {
    'width': '100%',
    'zIndex': '9999',  # Valor muy alto para asegurar que aparezca por encima de otros elementos
}

# Constantes
MONTH_NAMES = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

# Estilos comunes para tarjetas
card_style = {
    'boxShadow': '0 4px 8px rgba(0,0,0,0.1)', 
    'borderRadius': '10px', 
    'backgroundColor': 'white', 
    'marginBottom': '30px',
    'overflow': 'visible'
}

# Estilos para títulos
title_style = {
    'textAlign': 'center', 
    'color': '#2c3e50', 
    'marginBottom': '20px',
    'fontFamily': 'Montserrat, Arial, sans-serif'
}

# Estilos para botones
button_style = {
    'backgroundColor': '#6A5ACD',
    'color': 'white',
    'padding': '5px 15px',
    'border': 'none',
    'borderRadius': '5px',
    'fontSize': '12px',
    'cursor': 'pointer'
}

# Estilos para área de filtros
filter_area_style = {
    'padding': '10px', 
    'backgroundColor': '#f8f9fa', 
    'borderRadius': '0 0 10px 10px'
}
