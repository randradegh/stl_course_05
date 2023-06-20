##
# Análisis de accidentes de tránsito en la CDMX. Uso de streamlit, dataframes, pandas.
##
####
## Status: eb proceso
## Fecha revisión: 20220517
####

##
# Utilerías del proyecto
##
# Debe ser el primer comando

from utils import *
import pydeck as pdk
from pydeck.types import String

#st.image('images/wp3205208.jpg')
#st.markdown(my_footer, unsafe_allow_html=True)

header("9 casos de negocio con Streamlit")
st.subheader("Análisis de Accidentes de Tránsito en la CDMX. Parte 2.")
st.subheader("Introducción")

st.markdown("""
    El objetivo de esta app es revisar otros tipos de interacciones y de 
    gráficos para avanzar en el tema de manejo de los datos y su visualización 
    para la toma de decisiones.
""")

##
# Ejemplo de expander
##
with st.echo():
    with st.expander("Temas a revisar", expanded=True):
        st.write("""
            Revisaremos los expansores (_expander()_), más maneras de 
            seleccionar datos y gráficos, y la visualización de 
            datos geográficos.
        """)
        st.image("images/mapa_ejemplo.png")

with st.expander("Datos Geográficos", expanded=False):
     st.write("""
    ¿Qué son los Geodatos (_Geodata_)?
    Los geodatos, también conocidos como datos geográficos o datos geoespaciales, 
    se refieren a datos e información que tienen una asociación explícita o 
    implícita con una ubicación relativa a la Tierra.

    Los tipos comunes de datos geográficos incluyen archivos vectoriales, que constan 
    de vértices y rutas; archivos ráster, que se componen de píxeles y celdas de 
    cuadrícula; bases de datos geográficas, que cumple la función de albergar 
    vectores y rásteres; datos multitemporales, que adjuntan un componente 
    de tiempo a la información y **los que marcan una cierta ubicación en la 
    superficie de la tierra**, expresados por medio de coordenadas geográficas. 
    Usaremos de este último tipo en nuestros ejercicios.
    """)

st.write("""
    ---

    ### Temas a analizar
    - ¿A qué se refieren los geodatos en el _dataset_ de accidentes?
    - Análisis de los accidentes por zona y fecha
    - ¿En dónde hay mayor densidad de accidentes?
    - Otras preguntas.

    ### Carga de datos y contenido del _dataset_.
    
    Cargamos los datos usando el método read_csv() de Pandas.
    #### Carga de los datos
    En esta clase usaremos ocho campos (_features_) del gran _dataset_ 
    del INEGI.

    Contaremos con varios _features_ sobre los accidentes en la CDMX en el año 2020: **mes, día de la semana, 
    tipo de accidente (codificado), sexo del conductor(codificado), edad del conductor, 
    nombre de la alcadía, longitud y latitud** del lugar del evento.

    Usaremos esos datos para crear una interfaz interactiva que nos permita 
    analizar la distribución de los accidentes en función de alguna variable.

    Estos son los primeros 20 registros de nuestro _dataset_. Podemos 
    observar que ahora contamos con los datos geográficos mínimos: 
    longitud y latitud.
""")

df_8 = pd.read_csv("acc_8_campos.csv", sep='|')
st.write(df_8.head(20))

##
# Preparación de los datos
##

st.write("""
    #### Creación de Series
    Vamos a preparar los datos para los mecanismos de selección. De algunas 
    columnas de nuestro *dataframe* generaremos las series de opciones que 
    requerimos: meses, días de la semana, tipos de accidente y sexos. 
    Después, de los valores codificados del dataframe vamos a pasar a las 
    descripciones que nos indica la documentación del INEGI.

    Mostramos una de ellas como ejemplo:

    **Serie de Días de la Semana**
    """)

#with st.echo(code_location='above'):
    #st.write(type(df_8.diasemana))
    #st.write(type(df_8))
    #st.write(df_8.diasemana)

st.write("""Usando diccionarios de Python vamos a decodificar las series creadas para 
    contar con sus descripciones:
    """)


with st.echo(code_location='above'):

    ds_dict = {
        1: 'Lunes',
        2: 'Martes',
        3: 'Miércoles',
        4: 'Jueves',
        5: 'Viernes',
        6: 'Sábado',
        7: 'Domingo'
    }

    sexos_dict = {
        1: 'Hombre',
        2: 'Mujer',
        3: 'Se fugó'
    }

    tiposacc_dict = {
    1: 'Colisión con vehículo automotor',
    2: 'Colisión con peatón (atropellamiento)',
    3: 'Colisión con animal',
    4: 'Colisión con objeto fijo',
    5: 'Volcadura',
    6: 'Caída de pasajero',
    7: 'Salida del camino',
    8: 'Incendio',
    9: 'Colisión con ferrocarril',
    10: 'Colisión con motocicleta',
    11: 'Colisión con ciclista',
    12: 'Otro'
    }

    meses_dict = {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre'
    }

with st.echo(code_location='above'):
    
    meses_serie = pd.Series(meses_dict)
    ds_serie = pd.Series(ds_dict)
    tiposacc_serie = pd.Series(tiposacc_dict)
    sexos_serie = pd.Series(sexos_dict)
    
st.write("""
___
### Objetos de entrada (_input widgets_)
 """)

st.write("""
    Con los _widgets_, Streamlit le permite incorporar interactividad 
    directamente en sus aplicaciones con botones, controles deslizantes, 
    entradas de texto y más.

    Revisaremos algunos de esos _widgets_ como ejemplo de las prestaciones 
    de _streamlit

    **Ejemplos de uso de _widgets**
""")
with st.echo(code_location='above'):
    st.write("- Radio Button")
    # selectbox, slider, date_input, time_imput, ckecbox

    feature = st.radio(
        "Seleccione una serie a visualizar: ",
        ('Días de la semana', 'Tipos de Accidentes', 'Meses', 'Sexos')
        )

    if feature == 'Días de la semana':
        st.write(feature)
        st.write(ds_serie)
    elif feature == 'Tipos de Accidentes':
        st.write(feature)
        st.write(tiposacc_serie)
    elif feature == 'Meses':
        st.write(feature)
        st.write(meses_serie)
    elif feature == 'Sexos':
        st.write(sexos_serie)

with st.echo(code_location='above'):
    st.write("- Select Box")

    feature = st.selectbox(
     "Seleccione una serie a visualizar: ",
     ('Días de la semana', 'Tipos de Accidentes', 'Meses', 'Sexos'))

    st.write('Usted seleccionó:', feature)

    if feature == 'Días de la semana':
        st.write(feature)
        st.write(ds_serie)
    elif feature == 'Tipos de Accidentes':
        st.write(feature)
        st.write(tiposacc_serie)
    elif feature == 'Meses':
        st.write(feature)
        st.write(meses_serie)
    elif feature == 'Sexos':
        st.write(sexos_serie)
    
with st.echo(code_location='above'):
    st.write("- Check Box")
    agree = st.checkbox('¿Vamos a un descanso?')

    if agree:
        st.write('¡Fabuloso!')
    else:
        st.write('¡A trabajar!')

with st.echo(code_location='above'):
    st.write("- Slider")

    age = st.slider('¿Qué edad tienes?', 12, 100, 25)
    
    st.write('Tengo', age, 'años')

    values = st.slider(
        'Seleccione un rango de valores',
        0.0, 100.0, (25.0, 75.0))
    st.write('Valores:', values)

    from datetime import time
    appointment = st.slider(
        "Programe su cita:",
        value=(time(11, 30), time(12, 45)))
    st.write("Tiene una cita a las:", appointment)

    from datetime import datetime
    start_time = st.slider(
        "¿Cuándo inició?",
        min_value = datetime(2022, 1, 1, 19, 30),
        max_value = datetime(2023, 12, 31, 11, 51),
        format="MM/DD/YY - hh:mm")
    st.write("Hora de inicio:", start_time)

st.write("""
___
### Gráfico con interacción del usuario
""")
st.subheader("¿Dónde hay más densidad de accidentes?")
st.write("El siguiente mapa muestra los accidentes por Alcaldía.")

with st.echo(code_location='bellow'):
    # Selección de la alcadía a visualizar
    alcaldia = st.selectbox(
        "Seleccione la alcaldía que desea visualizar: ",
        (df_8.nomgeo.sort_values().unique()))

    st.success(f"""
        Usted seleccionó la alcaldía **{alcaldia}**.
    """)
    
    map_data = df_8.query(f"nomgeo == '{alcaldia}'")[['longitud', 'latitud']]    
        
    st.write(
    """
        #### Configuración del mapa

        Definimos la localización del centro del mapa
    """)

    
    sel_latitud = map_data.latitud.mean()
    sel_longitud = map_data.longitud.mean()


st.write(sel_latitud)

st.write(sel_longitud)

st.write(map_data)

st.write("""
    **Capas (Layers)**

    Configura una capa deck.gl para renderizar en un mapa. Los parámetros 
    pasados aquí serán específicos para la capa particular deck.gl que elija usar.
    """)
    
with st.echo(code_location='above'):
    

    layer = pdk.Layer(
        "HeatmapLayer",
        #colorRange= [[0, 172, 105], [244, 161, 0], [247, 100, 0], [232, 21, 0], [227, 0, 89], [105, 0, 99]],
        colorRange= [[244, 161, 0],[169,50,38]],
        # Actualmento con los colores por omisión.
        data=map_data,
        get_position='[longitud, latitud]',
        aggregation=String('MEAN'),
        pickable=True
    )

st.write("""
    **Ver estado (ViewState)**

    Se utiliza para establecer la ubicación precisa del punto de vista de 
    un usuario en los datos, como el nivel de zoom de un usuario
    """
    )

with st.echo(code_location='bellow'):
    
    view_state = pdk.ViewState(
        latitude=sel_latitud,
        longitude=sel_longitud,
        zoom=9,
        pitch=0
    )

st.write("""
    **Plataforma (Deck)**

    Se utiliza para escribir datos en un widget en, guardarlo en HTML y 
    configurar algunos parámetros globales de una visualización, 
    como su tamaño o información sobre herramientas.

    ** Mapa**

    En el siguiente mapa se muestran la densidad de accidentes de tráfico. 
    
    La zona roja es la de mayor y la amarilla la de menor densidad.
""")

with st.echo(code_location='above'):
    st.write("""
    Mapa
    
    En el siguiente mapa se muestran la densidad de accidentes de tráfico. 
    
    La zona roja es la de mayor y la amarilla la de menor densidad.
    """)
    m = st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state, 
        layers=[layer]))

    