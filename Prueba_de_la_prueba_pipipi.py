#paquetes
import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import plotly.express as px
import streamlit.components.v1 as components
#configuración de la pestaña
st.set_page_config(page_title="Recomendación musical", page_icon="🎵", layout="wide")

#diseño css y animación de los emojis flotantes
custom_css = """
<style>
/* Bordes laterales */
.stApp {
    border-left: 200px solid #F08784; /* Color del borde izquierdo */
    border-right: 200px solid #F08784; /* Color del borde derecho */
}

/* Animación de los emoji cayendo */
@keyframes falling {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100vh); }
}

/* Estilo de los emojis */
.falling-emoji {
    position: fixed;
    animation: falling 7s linear infinite;
    font-size: 3em;
}

/* posición o */
#emoji1 { left: 30px; }
#emoji2 { left: 120px; }
#emoji3 { right: 30px; }
#emoji4 { right: 120px; }c
</style>
"""

# Se agrega el diseño CSS a streamlit
st.markdown(custom_css, unsafe_allow_html=True)

# Aquí se agregan los emojis
st.markdown('<div class="falling-emoji" id="emoji1">🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji2">🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji3">🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji4">🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji1">🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji2">🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji3">🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji4">🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji1">🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji2">🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji3">🎵</div>', unsafe_allow_html=True)
st.markdown('<div class="falling-emoji" id="emoji4">🎵</div>', unsafe_allow_html=True)

#guarda datos para optimizar el rendimiento de la aplicación
@st.cache(allow_output_mutation=True)

#definimos la función load_data que 
def load_data():
    df = pd.read_csv("data/filtered_track_df.csv")#primero lee el csv
    df['genres'] = df.genres.apply(lambda x: [i[1:-1] for i in str(x)[1:-1].split(", ")])#tomamos la columna de genero y la transformamos en una cadena de texto, eliminamos los corchetes, definimos a la coma como separados y eliminamos las comillas.
    exploded_track_df = df.explode("genres")#separamos cada canción por genero
    return exploded_track_df #retorno a df para que ajá se pueda hacer varias veces y no se muera

#como temos varias caracteristicas, separamos los generos de las demás caracteristicas 
genre_names = ['Dance Pop', 'Electronic', 'Electropop', 'Hip Hop', 'Jazz', 'K-pop', 'Latin', 'Pop', 'Pop Rap', 'R&B', 'Rock']
audio_feats = ["acousticness", "danceability", "energy", "instrumentalness", "valence", "tempo"]

#le damos nombre a lo anterior
exploded_track_df = load_data()

#definimos una funciín
def n_neighbors_uri_audio(genre, start_year, end_year, test_feat):
    genre = genre.lower()#pasamos el genero a minusculas
    genre_data = exploded_track_df[(exploded_track_df["genres"]==genre) & (exploded_track_df["release_year"]>=start_year) & (exploded_track_df["release_year"]<=end_year)]#obtenemos solo las filas que coinciden con el genero espeficifado
    genre_data = genre_data.sort_values(by='popularity', ascending=False)[:500]#se ordenan por popularidad, genero y rango de año
#aquí empieza el entrenamiento
    #estas variables serán las canciones más cercanas (algo así como encontrar la vecindad, o los valores que más se acercan a lo que pedimos) a lo que pedimos (genero, popualridad, rango de año)
    neigh = NearestNeighbors()
    neigh.fit(genre_data[audio_feats].to_numpy())#

    n_neighbors = neigh.kneighbors([test_feat], n_neighbors=len(genre_data), return_distance=False)[0]
    #obtenemos los url de las canciones correspondientes
    uris = genre_data.iloc[n_neighbors]["uri"].tolist()
    # y las caracteristicas
    audios = genre_data.iloc[n_neighbors][audio_feats].to_numpy()
    return uris, audios #devielve los url y las caracteristicas

#titulo y demás
st.markdown("<h1 style='text-align: center; color: #F74B66; text-shadow: 3px 3px #808080;'> Modelo de recomendación de canciones </h1>", unsafe_allow_html=True)

st.markdown("A continuación se le pedirán ciertas características para hacer una predicción ")
st.markdown("##")

#hacemos que el usuario elija un genero
#botones de genero, Dance pop por defenco
st.markdown("***Elija el género***")
genre = st.radio(
    "",
    genre_names, index=genre_names.index("Dance Pop"))
#le pedimos al usuario que elija las caracteristicas, le mostramos sliders con datos por defecto
with st.container():
    col1, col2,col3,col4 = st.columns((2,0.5,2,0.5))
    with col1:
        st.markdown("***Elija las características:***")
        start_year, end_year = st.slider(
            'Seleccione el rango del año',
            1990, 2019, (1990, 2019)
        )
        acousticness = st.slider(
            'Acústica',
            0.0, 1.0, 1.0)
        instrumentalness = st.slider(
            'Instrumentabilidad',
            0.0, 1.0, 1.0)
        danceability = st.slider(
            'Bailabilidad',
            0.0, 1.0, 1.0)
    with col3:
        energy = st.slider(
            'Energía',
            0.0, 1.0, 1.0)
        valence = st.slider(
            'Valencia',
            0.0, 1.0, 1.0)
        tempo = st.slider(
            'Tiempo',
            0.0, 244.0, 244.0)


#mostramos 4 canciones
tracks_per_page = 4
test_feat = [acousticness, danceability, energy, instrumentalness, valence, tempo]#carateristicas
uris, audios = n_neighbors_uri_audio(genre, start_year, end_year, test_feat)#guarda el erl y las caracteristicas de las canciones basadas en el resultado del entrenamiento

#una lista que almacene las canciones
tracks = []
for uri in uris:#bucle
    track = """<iframe src="https://open.spotify.com/embed/track/{}" width="260" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri) #hacemos los cuadros para las canciones
    tracks.append(track) #lista de cadenas de cada pista

#al principio de código incdicamos que se guarden los datos/cache. aquí recordamos los valores que teemos para que no haya problema entre las iteraciones y la aplicación no se muera
if 'previous_inputs' not in st.session_state: 
    st.session_state['previous_inputs'] = [genre, start_year, end_year] + test_feat

#creamos una lista que contengan los datos que queremos 
current_inputs = [genre, start_year, end_year] + test_feat
#verificamos que los valores actuales no sean iguales a los anteriores, si eso es verdadero entonces:
if current_inputs != st.session_state['previous_inputs']:
    if 'start_track_i' in st.session_state:
        st.session_state['start_track_i'] = 0
    st.session_state['previous_inputs'] = current_inputs #actualizamos la lista de los datos que queremos

if 'start_track_i' not in st.session_state:
    st.session_state['start_track_i'] = 0

#dividimos la página
with st.container():
    col1, col2, col3 = st.columns([2,1,2])
    #si no queremos obtener los mismos resultados hacemos el procedimiento de nuevo
    if st.button("Más recomendaciones"):
        if st.session_state['start_track_i'] < len(tracks):
            st.session_state['start_track_i'] += tracks_per_page
    current_tracks = tracks[st.session_state['start_track_i']: st.session_state['start_track_i'] + tracks_per_page]
    current_audios = audios[st.session_state['start_track_i']: st.session_state['start_track_i'] + tracks_per_page]
#mostramos las canciones
    if st.session_state['start_track_i'] < len(tracks):
        for i, (track, audio) in enumerate(zip(current_tracks, current_audios)):
            if i%2==0:#dos columnas
                with col1:#indices pares
                    components.html(#lo mostramos en streamlit
                        track,
                        height=400,
                    )
                    with st.expander("Características"):#mostramos las características
                        df = pd.DataFrame(dict(
                        r=audio[:5],
                        theta=audio_feats[:5]))
                        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
                        fig.update_layout(height=400, width=340)
                        st.plotly_chart(fig)
        
            else: #lo mismo pero para la otra columna
                with col3:
                    components.html(
                        track,
                        height=400,
                    )
                    with st.expander("Características"):
                        df = pd.DataFrame(dict(
                            r=audio[:5],
                            theta=audio_feats[:5]))
                        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
                        fig.update_layout(height=400, width=340)
                        st.plotly_chart(fig)

    else:#en caso de que ninguna cancion se acerque a lo que el usuario pide
        st.write("No hay canciones para recomendar :c")
