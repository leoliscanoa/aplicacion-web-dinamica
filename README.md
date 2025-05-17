# Análisis de Mortalidad en Colombia (2019)

Una aplicación web interactiva para analizar los datos de mortalidad en Colombia durante el año 2019. Construida con Dash y Plotly para una visualización de datos dinámica y responsiva.


## Tabla de Contenidos

- [Características](#características)
- [Visualizaciones](#visualizaciones)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
  - [Elementos Clave](#elementos-clave)
- [Despliegue](#despliegue)
  - [Despliegue en Render.com](#despliegue-en-rendercom)
- [Solución de Problemas](#solución-de-problemas)
  - [Problemas Comunes](#problemas-comunes)
- [Licencia](#licencia)
- [Autores](#autores)
- [Referencias](#referencias)

## Características

- **Visualización Interactiva**: Mapas, gráficos y tablas interactivos para explorar datos de mortalidad
- **Filtrado Dinámico**: Filtros en tiempo real para análisis personalizado por departamento, género, mes y manera de muerte
- **Análisis Multidimensional**: Explorar patrones de mortalidad desde diferentes perspectivas
- **Diseño Responsivo**: Interfaz adaptable para diferentes dispositivos y tamaños de pantalla
- **Datos Completos**: Análisis basado en datos oficiales de Medicina Legal Colombia 2019

## Visualizaciones

El dashboard incluye las siguientes visualizaciones:

1. **Mapa de Mortalidad por Departamento**: Mapa coroplético que muestra la distribución geográfica de muertes en Colombia
2. **Tendencia Mensual de Muertes**: Gráfico de línea que muestra la evolución de muertes a lo largo del año
3. **Distribución por Edad**: Histograma que muestra la distribución de muertes por grupos de edad
4. **Top 10 Ciudades con Mayor Tasa de Homicidio**: Gráfico de barras con las ciudades más violentas
5. **Top 10 Ciudades con Menor Tasa de Mortalidad**: Gráfico circular con las ciudades con menor mortalidad
6. **Distribución por Género en Departamentos**: Gráfico de barras agrupadas que compara muertes por género en diferentes departamentos
7. **Principales Causas de Muerte**: Tabla de datos con las causas más comunes de mortalidad

## Requisitos

- Python 3.9 o superior
- Dash 3.0.0 o superior
- Plotly 6.0.0 o superior
- Pandas 2.0.0 o superior
- Gunicorn 20.1.0 (para despliegue)

## Instalación

1. Crear un entorno virtual:
```
python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
```


2. Instalar las dependencias:
```
pip install -r requirements.txt
```


## Uso

1. Ejecutar la aplicación localmente:
```
python app.py
```


2. Abrir un navegador y acceder a:
```
http://127.0.0.1:5000/
```


3. Navegar por el dashboard:
   - Utilizar los filtros para personalizar las visualizaciones
   - Interactuar con los gráficos para ver información detallada
   - Explorar diferentes perspectivas de los datos de mortalidad

## Estructura del Proyecto

```
mortality-analysis-dashboard/
├── app.py                      # Punto de entrada de la aplicación
├── requirements.txt            # Dependencias del proyecto
├── render.yaml                 # Configuración para despliegue en Render.com
├── README.md                   # Documentación del proyecto
├── src/                        # Código fuente principal
│   ├── __init__.py
│   ├── callbacks/              # Callbacks para interactividad
│   │   ├── __init__.py
│   │   └── callbacks.py        # Definición de callbacks de Dash
│   ├── data_processing/        # Procesamiento de datos
│   │   ├── __init__.py
│   │   └── data_loader.py      # Funciones para cargar y procesar datos
│   ├── geo/                    # Datos geográficos
│   │   └── departamentos.json  # GeoJSON de departamentos de Colombia
│   ├── layouts/                # Componentes de interfaz
│   │   ├── __init__.py
│   │   └── layout.py           # Definición del layout del dashboard
│   ├── utils/                  # Utilidades
│   │   ├── __init__.py
│   │   └── utils.py            # Funciones de utilidad reutilizables
│   └── visualizations/         # Componentes de visualización
│       ├── __init__.py
│       └── charts.py           # Funciones para crear gráficos
└── data/                       # Archivos de datos
    ├── NoFetal2019.csv         # Datos de mortalidad
    ├── CodigosDeMuerte.csv     # Códigos de causas de muerte
    └── Divipola.csv            # Códigos DIVIPOLA (geografía Colombia)
```


### Elementos Clave

- **app.py**: Punto de entrada que configura la aplicación Dash y registra los callbacks
- **data_loader.py**: Contiene funciones para cargar y procesar los datos de mortalidad
- **layout.py**: Define la estructura visual del dashboard y sus componentes
- **callbacks.py**: Implementa la lógica de interactividad para los filtros y gráficos
- **charts.py**: Contiene funciones para crear las visualizaciones con Plotly
- **utils.py**: Proporciona funciones de utilidad como la creación de componentes reutilizables

## Despliegue

### Despliegue en Render.com

1. Crear una cuenta en [Render.com](https://render.com/) si aún no tienes una

2. Conectar tu repositorio de GitHub a Render:
   - En el dashboard de Render, haz clic en "New" > "Web Service"
   - Conecta tu cuenta de GitHub y selecciona el repositorio

3. Configurar el servicio web:
   - **Name**: mortality-analysis-dashboard (o el nombre que prefieras)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

4. Ajustar variables de entorno:
   - **PYTHON_VERSION**: 3.9.1

5. Hacer clic en "Create Web Service" y esperar a que se complete el despliegue

## Solución de Problemas

### Problemas Comunes

1. **Error de módulo no encontrado**:
   - Asegúrate de que la estructura del proyecto es correcta
   - Verifica que todos los archivos `__init__.py` existan en los directorios correspondientes
   - Si el error ocurre en el despliegue, revisa la configuración de `app.py`

2. **Problemas al cargar los datos**:
   - Verifica que los archivos CSV estén en la carpeta `data/`
   - Asegúrate de que los nombres de los archivos coincidan con los esperados en `data_loader.py`

3. **Los filtros no funcionan correctamente**:
   - Revisa los IDs de los componentes en `layout.py` y `callbacks.py` para asegurar que coincidan
   - Verifica que las funciones de callback estén correctamente registradas

4. **Problemas con el mapa de Colombia**:
   - Asegúrate de que el archivo GeoJSON esté correctamente ubicado en `src/geo/`
   - Verifica que los nombres de departamentos en los datos coincidan con los del GeoJSON

## Licencia
Este repositorio está licenciado bajo [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](http://creativecommons.org/licenses/by-nc-sa/4.0/).
### Eres libre de:
- **Compartir** — copiar y redistribuir el material en cualquier medio o formato
- **Adaptar** — remezclar, transformar y construir a partir del material

### Bajo los siguientes términos:
- **Atribución** — Debes dar crédito de manera adecuada, proporcionar un enlace a la licencia e indicar si se han realizado cambios.
- **NoComercial** — No puedes utilizar el material con fines comerciales.
- **CompartirIgual** — Si remezclas, transformas o creas a partir del material, debes distribuir tus contribuciones bajo la misma licencia.

Ver el archivo [LICENSE.txt](LICENSE.txt) para más detalles.

## Autores
- Bechara, Hermes (hacordoba77@unisalle.edu.co)
- Liscano, Andrés (aliscano20@unisalle.edu.co)
- Montealegre, Efrain (emontealegre19@unisalle.edu.co)

## Referencias
- Dash. (s.f.). Dash Documentation. Recuperado el 17 de mayo de 2025, de https://dash.plotly.com/
- Plotly. (s.f.). Plotly Python Graphing Library. Recuperado el 17 de mayo de 2025, de https://plotly.com/python/
- Render. (s.f.). Deploy a Python Application. Recuperado el 17 de mayo de 2025, de https://render.com/docs/deploy-python