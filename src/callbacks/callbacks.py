"""
Módulo para la definición de los callbacks de la aplicación.
Contiene funciones para actualizar las visualizaciones en respuesta a las interacciones del usuario.
"""

from dash import Input, Output
from src.data_processing.data_loader import process_data_for_department_map, process_data_for_monthly_deaths, process_data_for_age_histogram, process_data_for_violent_cities, process_data_for_lowest_mortality_cities, process_data_for_gender_department
from src.visualizations.charts import create_department_map, create_monthly_deaths_chart, create_age_histogram, create_violent_cities_chart, create_lowest_mortality_chart, create_gender_department_chart
from src.utils.utils import MONTH_NAMES

def register_callbacks(app, df_mortality, df_divipola, gender_mapping, df_codes=None):
    """
    Registra todos los callbacks de la aplicación.

    Args:
        app (dash.Dash): Instancia de la aplicación Dash.
        df_mortality (pandas.DataFrame): DataFrame con los datos de mortalidad.
        df_divipola (pandas.DataFrame): DataFrame con los datos de división política de Colombia.
        gender_mapping (dict): Diccionario que mapea códigos de género a nombres.
    """

    # --- Callback para el Mapa ---
    @app.callback(
        Output('map-graph', 'figure'),
        [Input('map-manner-filter', 'value'),
         Input('map-month-filter', 'value'),
         Input('map-gender-filter', 'value')]
    )
    def update_map(selected_manners, selected_months, selected_genders):
        """
        Actualiza el mapa de departamentos según los filtros seleccionados.

        Args:
            selected_manners (list): Lista de maneras de muerte seleccionadas.
            selected_months (list): Lista de meses seleccionados.
            selected_genders (list): Lista de géneros seleccionados.

        Returns:
            plotly.graph_objects.Figure: Figura actualizada del mapa.
        """
        # Crear una copia del DataFrame original
        filtered_df = df_mortality.copy()

        # Aplicar filtros si se han seleccionado
        if selected_manners and len(selected_manners) > 0:
            filtered_df = filtered_df[filtered_df['MANERA_MUERTE'].isin(selected_manners)]

        if selected_months and len(selected_months) > 0:
            month_to_num = {v: k for k, v in MONTH_NAMES.items()}
            selected_month_nums = [month_to_num[month] for month in selected_months]
            filtered_df = filtered_df[filtered_df['MES'].isin(selected_month_nums)]

        if selected_genders and len(selected_genders) > 0:
            gender_to_code = {v: k for k, v in gender_mapping.items()}
            selected_gender_codes = [gender_to_code[gender] for gender in selected_genders]
            filtered_df = filtered_df[filtered_df['SEXO'].isin(selected_gender_codes)]

        # Procesar datos filtrados
        filtered_deaths_by_dept = process_data_for_department_map(filtered_df, df_divipola)

        # Crear visualización actualizada
        updated_map_fig = create_department_map(filtered_deaths_by_dept)

        return updated_map_fig


    # --- Callback para Muertes por Mes ---
    @app.callback(
        Output('monthly-deaths-graph', 'figure'),
        [Input('monthly-dept-filter', 'value'),
         Input('monthly-gender-filter', 'value')]
    )
    def update_monthly_chart(selected_depts, selected_genders):
        """
        Actualiza el gráfico de muertes mensuales según los filtros seleccionados.

        Args:
            selected_depts (list): Lista de departamentos seleccionados.
            selected_genders (list): Lista de géneros seleccionados.

        Returns:
            plotly.graph_objects.Figure: Figura actualizada del gráfico de muertes mensuales.
        """
        # Crear una copia del DataFrame original
        filtered_df = df_mortality.copy()

        # Combinar con divipola para obtener nombres de departamentos
        if selected_depts and len(selected_depts) > 0:
            # Primero añadir la columna DEPARTAMENTO
            filtered_df = filtered_df.merge(
                df_divipola[['COD_DANE', 'COD_DEPARTAMENTO', 'DEPARTAMENTO']],
                on='COD_DANE',
                how='left'
            )
            # Luego filtrar por departamento
            filtered_df = filtered_df[filtered_df['DEPARTAMENTO'].isin(selected_depts)]

        if selected_genders and len(selected_genders) > 0:
            gender_to_code = {v: k for k, v in gender_mapping.items()}
            selected_gender_codes = [gender_to_code[gender] for gender in selected_genders]
            filtered_df = filtered_df[filtered_df['SEXO'].isin(selected_gender_codes)]

        # Procesar datos filtrados
        filtered_deaths_by_month = process_data_for_monthly_deaths(filtered_df)

        # Crear visualización actualizada
        updated_monthly_deaths_fig = create_monthly_deaths_chart(filtered_deaths_by_month)

        return updated_monthly_deaths_fig


    # --- Callback para Distribución por Edad ---
    @app.callback(
        Output('age-histogram', 'figure'),
        [Input('age-dept-filter', 'value'),
         Input('age-gender-filter', 'value')]
    )
    def update_age_histogram(selected_depts, selected_genders):
        """
        Actualiza el histograma de edad según los filtros seleccionados.

        Args:
            selected_depts (list): Lista de departamentos seleccionados.
            selected_genders (list): Lista de géneros seleccionados.

        Returns:
            plotly.graph_objects.Figure: Figura actualizada del histograma de edad.
        """
        # Crear una copia del DataFrame original
        filtered_df = df_mortality.copy()

        # Combinar con divipola para obtener nombres de departamentos
        if selected_depts and len(selected_depts) > 0:
            # Primero añadir la columna DEPARTAMENTO
            filtered_df = filtered_df.merge(
                df_divipola[['COD_DANE', 'COD_DEPARTAMENTO', 'DEPARTAMENTO']],
                on='COD_DANE',
                how='left'
            )
            # Luego filtrar por departamento
            filtered_df = filtered_df[filtered_df['DEPARTAMENTO'].isin(selected_depts)]

        if selected_genders and len(selected_genders) > 0:
            gender_to_code = {v: k for k, v in gender_mapping.items()}
            selected_gender_codes = [gender_to_code[gender] for gender in selected_genders]
            filtered_df = filtered_df[filtered_df['SEXO'].isin(selected_gender_codes)]

        # Procesar datos filtrados
        filtered_deaths_by_age = process_data_for_age_histogram(filtered_df)

        # Crear visualización actualizada
        updated_age_histogram_fig = create_age_histogram(filtered_deaths_by_age)

        return updated_age_histogram_fig


    # --- Callback para Ciudades más Violentas ---
    @app.callback(
        Output('violent-cities-graph', 'figure'),
        [Input('violent-manner-filter', 'value'),
         Input('violent-gender-filter', 'value')]
    )
    def update_violent_cities_chart(selected_violent_types, selected_genders):
        """
        Actualiza el gráfico de ciudades más violentas según los filtros seleccionados.

        Args:
            selected_violent_types (list): Lista de descripciones de tipos de homicidios seleccionados.
            selected_genders (list): Lista de géneros seleccionados.

        Returns:
            plotly.graph_objects.Figure: Figura actualizada del gráfico de ciudades más violentas.
        """
        # Crear una copia del DataFrame original
        filtered_df = df_mortality.copy()

        # Aplicar filtro de género si se ha seleccionado
        if selected_genders and len(selected_genders) > 0:
            gender_to_code = {v: k for k, v in gender_mapping.items()}
            selected_gender_codes = [gender_to_code[gender] for gender in selected_genders]
            filtered_df = filtered_df[filtered_df['SEXO'].isin(selected_gender_codes)]

        # Extraer los códigos de muerte de las descripciones seleccionadas
        selected_codes = []
        if selected_violent_types and len(selected_violent_types) > 0:
            for desc in selected_violent_types:
                # Extraer el código de la descripción (formato: "X994 - Descripción")
                code = desc.split(' - ')[0]
                selected_codes.append(code)

        # Procesar datos filtrados, pasando los códigos de homicidios seleccionados
        filtered_violent_cities = process_data_for_violent_cities(filtered_df, df_divipola, df_codes, selected_codes)

        # Crear visualización actualizada
        updated_violent_cities_fig = create_violent_cities_chart(filtered_violent_cities)

        return updated_violent_cities_fig


    # --- Callback para Ciudades con Menor Mortalidad ---
    @app.callback(
        Output('lowest-mortality-graph', 'figure'),
        [Input('lowest-gender-filter', 'value')]
    )
    def update_lowest_mortality_chart(selected_genders):
        """
        Actualiza el gráfico de ciudades con menor mortalidad según los filtros seleccionados.

        Args:
            selected_genders (list): Lista de géneros seleccionados.

        Returns:
            plotly.graph_objects.Figure: Figura actualizada del gráfico de ciudades con menor mortalidad.
        """
        # Crear una copia del DataFrame original
        filtered_df = df_mortality.copy()

        # Aplicar filtros si se han seleccionado
        if selected_genders and len(selected_genders) > 0:
            gender_to_code = {v: k for k, v in gender_mapping.items()}
            selected_gender_codes = [gender_to_code[gender] for gender in selected_genders]
            filtered_df = filtered_df[filtered_df['SEXO'].isin(selected_gender_codes)]

        # Procesar datos filtrados
        filtered_lowest_mortality = process_data_for_lowest_mortality_cities(filtered_df, df_divipola)

        # Crear visualización actualizada
        updated_lowest_mortality_fig = create_lowest_mortality_chart(filtered_lowest_mortality)

        return updated_lowest_mortality_fig


    # --- Callback para Muertes por Género y Departamento ---
    @app.callback(
        Output('gender-dept-graph', 'figure'),
        [Input('gender-dept-manner-filter', 'value'),
         Input('gender-dept-month-filter', 'value')]
    )
    def update_gender_dept_chart(selected_manners, selected_months):
        """
        Actualiza el gráfico de muertes por género y departamento según los filtros seleccionados.

        Args:
            selected_manners (list): Lista de maneras de muerte seleccionadas.
            selected_months (list): Lista de meses seleccionados.

        Returns:
            plotly.graph_objects.Figure: Figura actualizada del gráfico de muertes por género y departamento.
        """
        # Crear una copia del DataFrame original
        filtered_df = df_mortality.copy()

        # Aplicar filtros si se han seleccionado
        if selected_manners and len(selected_manners) > 0:
            filtered_df = filtered_df[filtered_df['MANERA_MUERTE'].isin(selected_manners)]

        if selected_months and len(selected_months) > 0:
            month_to_num = {v: k for k, v in MONTH_NAMES.items()}
            selected_month_nums = [month_to_num[month] for month in selected_months]
            filtered_df = filtered_df[filtered_df['MES'].isin(selected_month_nums)]

        # Procesar datos filtrados
        filtered_deaths_by_dept_gender = process_data_for_gender_department(filtered_df, df_divipola)

        # Crear visualización actualizada
        updated_gender_dept_fig = create_gender_department_chart(filtered_deaths_by_dept_gender)

        return updated_gender_dept_fig
