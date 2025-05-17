"""
Módulo para la carga y procesamiento de datos de mortalidad.
Contiene funciones para cargar los datos desde archivos CSV y procesarlos para su visualización.
"""

import pandas as pd
import os

# Constantes
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/')
from src.utils.utils import MONTH_NAMES

def load_data():
    """
    Carga y retorna los conjuntos de datos necesarios para la aplicación.

    Returns:
        tuple: Tupla con tres DataFrames (df_mortality, df_codes, df_divipola)

    Raises:
        FileNotFoundError: Si alguno de los archivos no se encuentra en el directorio de datos.
        Exception: Si ocurre algún otro error durante la carga de los archivos.
    """
    try:
        df_mortality = pd.read_csv(f'{DATA_PATH}NoFetal2019.csv')
        df_codes = pd.read_csv(f'{DATA_PATH}CodigosDeMuerte.csv', delimiter=';')
        df_divipola = pd.read_csv(f'{DATA_PATH}Divipola.csv', delimiter=';')

        print("Archivos cargados exitosamente.")
        return df_mortality, df_codes, df_divipola

    except FileNotFoundError:
        print(
            "Error: Asegúrese de que los archivos ('NoFetal2019.csv', 'CodigosDeMuerte.csv', 'Divipola.csv') estén en el directorio de datos.")
        exit()
    except Exception as e:
        print(f"Ocurrió un error durante la carga de archivos: {e}")
        exit()


def process_data_for_department_map(df_mortality, df_divipola):
    """
    Procesa los datos para la visualización del mapa de departamentos.

    Args:
        df_mortality (DataFrame): DataFrame con los datos de mortalidad.
        df_divipola (DataFrame): DataFrame con los datos de división política de Colombia.

    Returns:
        DataFrame: DataFrame con el conteo de muertes por departamento.
    """
    # Combinar datos de mortalidad con divipola para obtener nombres de departamentos
    df_mortality_with_dept = df_mortality.merge(
        df_divipola[['COD_DANE', 'COD_DEPARTAMENTO', 'DEPARTAMENTO']],
        on='COD_DANE',
        how='left'
    )

    # Contar muertes por departamento
    deaths_by_dept = df_mortality_with_dept.groupby('DEPARTAMENTO').size().reset_index(name='TOTAL_DEATHS')

    return deaths_by_dept


def process_data_for_monthly_deaths(df_mortality):
    """
    Procesa los datos para el gráfico de línea de muertes mensuales.

    Args:
        df_mortality (DataFrame): DataFrame con los datos de mortalidad.

    Returns:
        DataFrame: DataFrame con el conteo de muertes por mes.
    """
    # Contar muertes por mes
    deaths_by_month = df_mortality.groupby('MES').size().reset_index(name='TOTAL_DEATHS')
    deaths_by_month = deaths_by_month.sort_values('MES')

    # Mapear números de mes a nombres de mes
    deaths_by_month['MONTH_NAME'] = deaths_by_month['MES'].map(MONTH_NAMES)

    return deaths_by_month


def process_data_for_violent_cities(df_mortality, df_divipola, df_codes=None, violent_types=None):
    """
    Procesa los datos para el gráfico de barras de las ciudades más violentas.
    Considera homicidios (filtrados por MANERA_MUERTE="Homicidio" y relacionados con sus descripciones).

    Args:
        df_mortality (DataFrame): DataFrame con los datos de mortalidad.
        df_divipola (DataFrame): DataFrame con los datos de división política de Colombia.
        df_codes (DataFrame, optional): DataFrame con los códigos de causas de muerte.
        violent_types (list, optional): Lista de tipos de muertes violentas a incluir.
                                       Si es None, incluye todos los tipos de homicidios.

    Returns:
        DataFrame: DataFrame con las 5 ciudades con más homicidios.
    """
    # Crear una copia del DataFrame para no modificar el original
    df = df_mortality.copy()

    # Filtrar solo los registros donde MANERA_MUERTE es "Homicidio"
    homicides = df[df['MANERA_MUERTE'] == 'Homicidio']

    # Si se proporcionan tipos específicos de homicidios, filtrar por ellos
    if violent_types and len(violent_types) > 0:
        # Filtrar solo por los tipos seleccionados
        homicides = homicides[homicides['COD_MUERTE'].isin(violent_types)]

    # Combinar con divipola para obtener nombres de ciudades
    homicides_with_city = homicides.merge(
        df_divipola[['COD_DANE', 'MUNICIPIO']],
        on='COD_DANE',
        how='left'
    )

    # Contar homicidios por ciudad
    homicides_by_city = homicides_with_city.groupby('MUNICIPIO').size().reset_index(name='HOMICIDES')

    # Obtener las 5 ciudades con más homicidios
    top_violent_cities = homicides_by_city.sort_values('HOMICIDES', ascending=False).head(5)

    return top_violent_cities


def process_data_for_lowest_mortality_cities(df_mortality, df_divipola):
    """
    Procesa los datos para el gráfico circular de ciudades con menor mortalidad.

    Args:
        df_mortality (DataFrame): DataFrame con los datos de mortalidad.
        df_divipola (DataFrame): DataFrame con los datos de división política de Colombia.

    Returns:
        DataFrame: DataFrame con las 10 ciudades con menor mortalidad.
    """
    # Combinar datos de mortalidad con divipola para obtener nombres de ciudades
    mortality_with_city = df_mortality.merge(
        df_divipola[['COD_DANE', 'MUNICIPIO']],
        on='COD_DANE',
        how='left'
    )

    # Contar muertes por ciudad
    deaths_by_city = mortality_with_city.groupby('MUNICIPIO').size().reset_index(name='DEATHS')

    # Obtener ciudades con al menos algunas muertes para evitar ceros
    deaths_by_city = deaths_by_city[deaths_by_city['DEATHS'] > 0]

    # Obtener 10 ciudades con menor mortalidad
    lowest_mortality_cities = deaths_by_city.sort_values('DEATHS').head(10)

    return lowest_mortality_cities


def process_data_for_top_causes(df_mortality, df_codes):
    """
    Procesa los datos para la tabla de principales causas de muerte.

    Args:
        df_mortality (DataFrame): DataFrame con los datos de mortalidad.
        df_codes (DataFrame): DataFrame con los códigos de causas de muerte.

    Returns:
        DataFrame: DataFrame con las 10 principales causas de muerte.
    """
    # Combinar datos de mortalidad con códigos para obtener descripciones de causas
    mortality_with_codes = df_mortality.merge(
        df_codes[['Código de la CIE-10 cuatro caracteres', 'Descripcion  de códigos mortalidad a cuatro caracteres']],
        left_on='COD_MUERTE',
        right_on='Código de la CIE-10 cuatro caracteres',
        how='left'
    )

    # Contar muertes por causa
    deaths_by_cause = mortality_with_codes.groupby([
        'COD_MUERTE', 'Descripcion  de códigos mortalidad a cuatro caracteres'
    ]).size().reset_index(name='TOTAL')

    # Obtener las 10 principales causas
    top_causes = deaths_by_cause.sort_values('TOTAL', ascending=False).head(10)

    # Renombrar columnas para mayor claridad
    top_causes = top_causes.rename(columns={
        'COD_MUERTE': 'Código',
        'Descripcion  de códigos mortalidad a cuatro caracteres': 'Descripción',
        'TOTAL': 'Total de Casos'
    })

    return top_causes


def process_data_for_age_histogram(df_mortality):
    """
    Procesa los datos para el histograma de distribución por edad.

    Args:
        df_mortality (DataFrame): DataFrame con los datos de mortalidad.

    Returns:
        DataFrame: DataFrame con el conteo de muertes por grupo de edad.
    """
    # Crear una copia del DataFrame para no modificar el original
    df = df_mortality.copy()

    # Definir grupos de edad
    age_bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 150]
    age_labels = [
        '0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44',
        '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84',
        '85-89', '90-94', '95-99', '100+'
    ]

    # Asignar grupos de edad
    df['AGE_GROUP'] = pd.cut(df['GRUPO_EDAD1'], bins=age_bins, labels=age_labels, right=False)

    # Contar muertes por grupo de edad
    deaths_by_age = df.groupby('AGE_GROUP').size().reset_index(name='COUNT')

    return deaths_by_age


def get_homicide_codes_with_descriptions(df_mortality, df_codes):
    """
    Obtiene los códigos de muerte por homicidio con sus descripciones.

    Args:
        df_mortality (DataFrame): DataFrame con los datos de mortalidad.
        df_codes (DataFrame): DataFrame con los códigos de causas de muerte.

    Returns:
        dict: Diccionario con códigos de homicidio como claves y descripciones como valores.
        list: Lista de tuplas (código, descripción) para usar en filtros.
    """
    # Filtrar solo los registros donde MANERA_MUERTE es "Homicidio"
    homicides = df_mortality[df_mortality['MANERA_MUERTE'] == 'Homicidio']

    # Obtener códigos únicos de homicidio
    unique_homicide_codes = homicides['COD_MUERTE'].unique()

    # Relacionar códigos con descripciones
    homicide_codes_with_desc = df_codes[df_codes['Código de la CIE-10 cuatro caracteres'].isin(unique_homicide_codes)]

    # Crear diccionario de código -> descripción
    code_to_desc = dict(zip(
        homicide_codes_with_desc['Código de la CIE-10 cuatro caracteres'],
        homicide_codes_with_desc['Descripcion  de códigos mortalidad a cuatro caracteres']
    ))

    # Crear lista de tuplas (código, descripción) para usar en filtros
    code_desc_list = [{'label': f"{code} - {desc}", 'value': code} for code, desc in code_to_desc.items()]

    return code_desc_list


def process_data_for_gender_department(df_mortality, df_divipola):
    """
    Procesa los datos para el gráfico de muertes por género y departamento.

    Args:
        df_mortality (DataFrame): DataFrame con los datos de mortalidad.
        df_divipola (DataFrame): DataFrame con los datos de división política de Colombia.

    Returns:
        DataFrame: DataFrame con el conteo de muertes por género y departamento.
    """
    # Combinar datos de mortalidad con divipola para obtener nombres de departamentos
    df_mortality_with_dept = df_mortality.merge(
        df_divipola[['COD_DANE', 'COD_DEPARTAMENTO', 'DEPARTAMENTO']],
        on='COD_DANE',
        how='left'
    )

    # Mapear códigos de género a nombres
    gender_mapping = {1: 'Masculino', 2: 'Femenino', 3: 'Indeterminado'}
    df_mortality_with_dept['GENDER'] = df_mortality_with_dept['SEXO'].map(gender_mapping)

    # Contar muertes por departamento y género
    deaths_by_dept_gender = df_mortality_with_dept.groupby(['DEPARTAMENTO', 'GENDER']).size().reset_index(name='COUNT')

    return deaths_by_dept_gender
