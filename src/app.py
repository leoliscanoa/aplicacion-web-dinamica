"""
Aplicación principal para el análisis de mortalidad en Colombia.
Este archivo integra todos los módulos y ejecuta la aplicación.
"""

import dash
from dash.dash_table import DataTable

from src.callbacks.callbacks import register_callbacks
# Importar módulos de la aplicación
from src.data_processing.data_loader import load_data, process_data_for_department_map, process_data_for_monthly_deaths, \
    process_data_for_age_histogram, process_data_for_violent_cities, process_data_for_lowest_mortality_cities, \
    process_data_for_top_causes, process_data_for_gender_department
from src.layouts.layout import create_layout
from src.utils.utils import MONTH_NAMES
from src.visualizations.charts import create_department_map, create_monthly_deaths_chart, create_age_histogram, \
    create_violent_cities_chart, create_lowest_mortality_chart, create_gender_department_chart

# Inicializar la aplicación Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Cargar datos
df_mortality, df_codes, df_divipola = load_data()

# Procesar datos para visualizaciones iniciales
deaths_by_dept = process_data_for_department_map(df_mortality, df_divipola)
deaths_by_month = process_data_for_monthly_deaths(df_mortality)
deaths_by_age = process_data_for_age_histogram(df_mortality)
top_violent_cities = process_data_for_violent_cities(df_mortality, df_divipola)
lowest_mortality_cities = process_data_for_lowest_mortality_cities(df_mortality, df_divipola)
top_causes = process_data_for_top_causes(df_mortality, df_codes)
deaths_by_dept_gender = process_data_for_gender_department(df_mortality, df_divipola)

# Crear visualizaciones iniciales
map_fig = create_department_map(deaths_by_dept)
monthly_deaths_fig = create_monthly_deaths_chart(deaths_by_month)
age_histogram_fig = create_age_histogram(deaths_by_age)
violent_cities_fig = create_violent_cities_chart(top_violent_cities)
lowest_mortality_fig = create_lowest_mortality_chart(lowest_mortality_cities)
gender_dept_fig = create_gender_department_chart(deaths_by_dept_gender)

# Crear tabla de principales causas de muerte
top_causes_table = DataTable(
    id='top-causes-table',
    columns=[
        {'name': 'Código', 'id': 'Código'},
        {'name': 'Descripción', 'id': 'Descripción'},
        {'name': 'Total de Casos', 'id': 'Total de Casos'}
    ],
    data=top_causes.to_dict('records'),
    style_header={
        'backgroundColor': '#6A5ACD',
        'color': 'white',
        'fontWeight': 'bold',
        'textAlign': 'center',
        'border': '1px solid #ddd'
    },
    style_cell={
        'textAlign': 'left',
        'padding': '10px',
        'border': '1px solid #ddd',
        'height': 'auto',
        'fontSize': '13px',
        'fontFamily': 'Arial, sans-serif'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#f5f5f5'
        }
    ],
    style_table={
        'overflowX': 'auto',
        'borderRadius': '5px'
    },
    sort_action='native',
    filter_action='native',
    page_size=10
)

# Obtener listas para filtros
departments = sorted(deaths_by_dept['DEPARTAMENTO'].dropna().unique())
manners_of_death = sorted(df_mortality['MANERA_MUERTE'].dropna().unique())
months = [month for _, month in sorted([(k, v) for k, v in MONTH_NAMES.items()], key=lambda x: x[0])]
gender_mapping = {1: 'Masculino', 2: 'Femenino', 3: 'Indeterminado'}
genders = list(gender_mapping.values())

# Configurar el layout de la aplicación
app.layout = create_layout(
    map_fig, 
    monthly_deaths_fig, 
    age_histogram_fig, 
    top_causes_table, 
    violent_cities_fig, 
    lowest_mortality_fig, 
    gender_dept_fig,
    departments, 
    manners_of_death, 
    months, 
    genders
)

# Registrar callbacks
register_callbacks(app, df_mortality, df_divipola, gender_mapping)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
