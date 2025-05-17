"""
Módulo para la creación de visualizaciones y gráficos.
Contiene funciones para crear diferentes tipos de gráficos utilizados en la aplicación.
"""

import json
import os

import plotly.express as px


def create_department_map(deaths_by_dept_map):
    """
    Crea un mapa coroplético de Colombia mostrando la mortalidad por departamento.
    
    Args:
        deaths_by_dept_map (pandas.DataFrame): DataFrame con nombres de departamentos y conteo de muertes.
        
    Returns:
        plotly.graph_objects.Figure: Figura del mapa coroplético.
    """
    # Crear una copia para no modificar el original
    deaths_by_dept_map = deaths_by_dept_map.copy()
    
    # Primero estandarizar nombres para facilitar el mapeo
    deaths_by_dept_map['DEPARTAMENTO'] = deaths_by_dept_map['DEPARTAMENTO'].str.upper()

    # Crear un mapeo comprensivo para hacer coincidir con el GeoJSON
    department_mapping = {
        'AMAZONAS': 'AMAZONAS',
        'ANTIOQUIA': 'ANTIOQUIA',
        'ARAUCA': 'ARAUCA',
        'ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA': 'SAN ANDRES',
        'ATLÁNTICO': 'ATLANTICO',
        'BARRANQUILLA D.E.': 'ATLANTICO',
        'BOGOTÁ, D.C.': 'BOGOTA D.C.',
        'BOGOTA D.C.': 'BOGOTA D.C.',
        'BOLÍVAR': 'BOLIVAR',
        'CARTAGENA D.T. Y C.': 'BOLIVAR',
        'BOYACÁ': 'BOYACA',
        'CALDAS': 'CALDAS',
        'CAQUETÁ': 'CAQUETA',
        'CASANARE': 'CASANARE',
        'CAUCA': 'CAUCA',
        'CESAR': 'CESAR',
        'CHOCÓ': 'CHOCO',
        'CÓRDOBA': 'CORDOBA',
        'CUNDINAMARCA': 'CUNDINAMARCA',
        'GUAINÍA': 'GUAINIA',
        'GUAVIARE': 'GUAVIARE',
        'HUILA': 'HUILA',
        'LA GUAJIRA': 'LA GUAJIRA',
        'MAGDALENA': 'MAGDALENA',
        'SANTA MARTA D.T. Y C.': 'MAGDALENA',
        'META': 'META',
        'NARIÑO': 'NARIÑO',
        'NORTE DE SANTANDER': 'NORTE DE SANTANDER',
        'PUTUMAYO': 'PUTUMAYO',
        'QUINDÍO': 'QUINDIO',
        'RISARALDA': 'RISARALDA',
        'SANTANDER': 'SANTANDER',
        'SUCRE': 'SUCRE',
        'TOLIMA': 'TOLIMA',
        'VALLE DEL CAUCA': 'VALLE DEL CAUCA',
        'BUENAVENTURA D.E.': 'VALLE DEL CAUCA',
        'VAUPÉS': 'VAUPES',
        'VICHADA': 'VICHADA'
    }

    # Aplicar el mapeo para estandarizar nombres de departamentos
    deaths_by_dept_map['DEPARTAMENTO'] = deaths_by_dept_map['DEPARTAMENTO'].replace(department_mapping)

    # Cargar archivo GeoJSON
    geo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'geo/departamentos.json')
    with open(geo_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    # Crear el mapa coroplético
    fig = px.choropleth(
        deaths_by_dept_map,
        geojson=geojson_data,
        locations='DEPARTAMENTO',
        featureidkey='properties.NOMBRE_DPT',
        color='TOTAL_DEATHS',
        color_continuous_scale="Reds",
        range_color=(0, deaths_by_dept_map['TOTAL_DEATHS'].max()),
        labels={'TOTAL_DEATHS': 'Número de Muertes'},
        title='Muertes Totales por Departamento en Colombia (2019)'
    )

    # Ajustar la vista del mapa para enfocarse en Colombia
    fig.update_geos(
        visible=False,
        showcountries=True,
        showcoastlines=True,
        showland=True,
        scope="south america",  # Establecer el alcance a Sudamérica
        center={"lat": 4.5709, "lon": -74.2973},  # Establecer el centro del mapa a un punto en Colombia
        projection_scale=5  # Ajustar la escala según sea necesario para hacer zoom en Colombia
    )

    # Actualizar diseño
    fig.update_layout(
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        height=700,  # Aumentar la altura para que el mapa sea más grande verticalmente
        coloraxis_colorbar=dict(
            title="Número de Muertes",
            thicknessmode="pixels",
            thickness=15,
            lenmode="pixels",
            len=300,
            yanchor="top",
            y=1,
            ticks="outside"
        ),
        title={
            'text': 'Muertes Totales por Departamento en Colombia (2019)',
            'x': 0.5,  # Centrar el título
            'xanchor': 'center'
        }
    )

    return fig


def create_monthly_deaths_chart(deaths_by_month):
    """
    Crea un gráfico de línea de muertes por mes con estilo mejorado.
    
    Args:
        deaths_by_month (pandas.DataFrame): DataFrame con datos de muertes por mes.
        
    Returns:
        plotly.graph_objects.Figure: Figura del gráfico de línea.
    """
    fig = px.line(
        deaths_by_month,
        x='MONTH_NAME',
        y='TOTAL_DEATHS',
        markers=True,
        labels={
            'MONTH_NAME': 'Mes',
            'TOTAL_DEATHS': 'Número de Muertes'
        },
        title='Muertes por Mes en Colombia (2019)'
    )

    # Personalizar el diseño
    fig.update_traces(
        line=dict(width=3, color='#6A5ACD'),
        marker=dict(size=10, color='#6A5ACD')
    )

    # Actualizar ejes
    fig.update_xaxes(
        title_text='Mes',
        tickangle=45,
        title_font=dict(size=14),
        tickfont=dict(size=12),
        gridcolor='#EEEEEE'
    )

    fig.update_yaxes(
        title_text='Número de Muertes',
        title_font=dict(size=14),
        tickfont=dict(size=12),
        gridcolor='#EEEEEE'
    )

    # Actualizar diseño general
    fig.update_layout(
        title={
            'text': 'Muertes por Mes en Colombia (2019)',
            'x': 0.5,  # Centrar el título
            'xanchor': 'center',
            'font': dict(size=18)
        },
        plot_bgcolor='white',
        hovermode='x unified',
        margin=dict(l=40, r=40, t=50, b=40)
    )

    return fig


def create_violent_cities_chart(top_violent_cities):
    """
    Crea un gráfico de barras horizontales para las ciudades más violentas.
    
    Args:
        top_violent_cities (pandas.DataFrame): DataFrame con datos de las ciudades más violentas.
        
    Returns:
        plotly.graph_objects.Figure: Figura del gráfico de barras.
    """
    fig = px.bar(
        top_violent_cities,
        y='MUNICIPIO',
        x='HOMICIDES',
        orientation='h',
        labels={
            'MUNICIPIO': 'Ciudad',
            'HOMICIDES': 'Número de Homicidios'
        },
        title='Ciudades con Mayor Número de Homicidios por Arma de Fuego (2019)',
        color='HOMICIDES',
        color_continuous_scale='Reds'
    )

    # Personalizar el diseño
    fig.update_traces(
        marker_line_width=0,
        hovertemplate='<b>%{y}</b><br>Homicidios: %{x}<extra></extra>'
    )

    # Actualizar ejes
    fig.update_xaxes(
        title_text='Número de Homicidios',
        title_font=dict(size=14),
        tickfont=dict(size=12),
        gridcolor='#EEEEEE'
    )

    fig.update_yaxes(
        title_text='Ciudad',
        title_font=dict(size=14),
        tickfont=dict(size=12),
        autorange="reversed"  # Para mostrar la ciudad con más homicidios en la parte superior
    )

    # Actualizar diseño general
    fig.update_layout(
        title={
            'text': 'Ciudades con Mayor Número de Homicidios por Arma de Fuego (2019)',
            'x': 0.5,  # Centrar el título
            'xanchor': 'center',
            'font': dict(size=18)
        },
        plot_bgcolor='white',
        coloraxis_showscale=False,
        margin=dict(l=40, r=40, t=50, b=40)
    )

    return fig


def create_lowest_mortality_chart(lowest_mortality_cities):
    """
    Crea un gráfico circular para las ciudades con menor mortalidad.
    
    Args:
        lowest_mortality_cities (pandas.DataFrame): DataFrame con datos de las ciudades con menor mortalidad.
        
    Returns:
        plotly.graph_objects.Figure: Figura del gráfico circular.
    """
    fig = px.pie(
        lowest_mortality_cities,
        values='DEATHS',
        names='MUNICIPIO',
        title='Ciudades con Menor Mortalidad (2019)',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Plasma_r
    )

    # Personalizar el diseño
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Muertes: %{value}<br>Porcentaje: %{percent}<extra></extra>'
    )

    # Actualizar diseño general
    fig.update_layout(
        title={
            'text': 'Ciudades con Menor Mortalidad (2019)',
            'x': 0.5,  # Centrar el título
            'xanchor': 'center',
            'font': dict(size=18)
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=40, r=40, t=50, b=40)
    )

    return fig


def create_age_histogram(deaths_by_age):
    """
    Crea un histograma de distribución de muertes por grupo de edad.
    
    Args:
        deaths_by_age (pandas.DataFrame): DataFrame con datos de muertes por grupo de edad.
        
    Returns:
        plotly.graph_objects.Figure: Figura del histograma.
    """
    fig = px.bar(
        deaths_by_age,
        x='AGE_GROUP',
        y='COUNT',
        labels={
            'AGE_GROUP': 'Grupo de Edad',
            'COUNT': 'Número de Muertes'
        },
        title='Distribución de Muertes por Grupo de Edad (2019)',
        color='COUNT',
        color_continuous_scale='Viridis'
    )

    # Personalizar el diseño
    fig.update_traces(
        marker_line_width=0,
        hovertemplate='<b>%{x}</b><br>Muertes: %{y}<extra></extra>'
    )

    # Actualizar ejes
    fig.update_xaxes(
        title_text='Grupo de Edad',
        title_font=dict(size=14),
        tickfont=dict(size=10),
        tickangle=45,
        gridcolor='#EEEEEE'
    )

    fig.update_yaxes(
        title_text='Número de Muertes',
        title_font=dict(size=14),
        tickfont=dict(size=12),
        gridcolor='#EEEEEE'
    )

    # Actualizar diseño general
    fig.update_layout(
        title={
            'text': 'Distribución de Muertes por Grupo de Edad (2019)',
            'x': 0.5,  # Centrar el título
            'xanchor': 'center',
            'font': dict(size=18)
        },
        plot_bgcolor='white',
        coloraxis_showscale=False,
        margin=dict(l=40, r=40, t=50, b=40)
    )

    return fig


def create_gender_department_chart(deaths_by_dept_gender):
    """
    Crea un gráfico de barras agrupadas para muertes por género y departamento.
    
    Args:
        deaths_by_dept_gender (pandas.DataFrame): DataFrame con datos de muertes por género y departamento.
        
    Returns:
        plotly.graph_objects.Figure: Figura del gráfico de barras agrupadas.
    """
    # Obtener los 10 departamentos con más muertes
    top_depts = deaths_by_dept_gender.groupby('DEPARTAMENTO')['COUNT'].sum().nlargest(10).index.tolist()
    
    # Filtrar el DataFrame para incluir solo esos departamentos
    filtered_df = deaths_by_dept_gender[deaths_by_dept_gender['DEPARTAMENTO'].isin(top_depts)]
    
    # Crear el gráfico de barras agrupadas
    fig = px.bar(
        filtered_df,
        x='DEPARTAMENTO',
        y='COUNT',
        color='GENDER',
        barmode='group',
        labels={
            'DEPARTAMENTO': 'Departamento',
            'COUNT': 'Número de Muertes',
            'GENDER': 'Género'
        },
        title='Muertes por Género en los 10 Departamentos Principales (2019)',
        color_discrete_map={
            'Masculino': '#3366CC',
            'Femenino': '#FF6699',
            'Indeterminado': '#66CCCC'
        }
    )
    
    # Personalizar el diseño
    fig.update_traces(
        marker_line_width=0,
        hovertemplate='<b>%{x}</b><br>Género: %{color}<br>Muertes: %{y}<extra></extra>'
    )
    
    # Actualizar ejes
    fig.update_xaxes(
        title_text='Departamento',
        title_font=dict(size=14),
        tickfont=dict(size=10),
        tickangle=45,
        gridcolor='#EEEEEE'
    )
    
    fig.update_yaxes(
        title_text='Número de Muertes',
        title_font=dict(size=14),
        tickfont=dict(size=12),
        gridcolor='#EEEEEE'
    )
    
    # Actualizar diseño general
    fig.update_layout(
        title={
            'text': 'Muertes por Género en los 10 Departamentos Principales (2019)',
            'x': 0.5,  # Centrar el título
            'xanchor': 'center',
            'font': dict(size=18)
        },
        plot_bgcolor='white',
        legend_title_text='Género',
        margin=dict(l=40, r=40, t=50, b=40)
    )
    
    return fig