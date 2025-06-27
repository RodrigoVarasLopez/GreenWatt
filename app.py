import streamlit as st
import requests
import matplotlib.pyplot as plt

# Configuración de página
st.set_page_config(page_title="Generación eléctrica en España", layout="centered")
st.title("🔌 Generación Eléctrica por Tecnología - REE (e-sios)")

# Ingresar token de la API
api_token = st.text_input("🔑 Introduce tu API Token de e-sios:", type="password")

# Tecnologías y sus IDs en la API
tecnologias = {
    'Hidráulica': 12,
    'Nuclear': 6,
    'Eólica': 5,
    'Solar fotovoltaica': 4,
    'Carbón': 16,
    'Ciclo combinado': 20,
    'Cogeneración': 22
}
sostenibles = ['Eólica', 'Solar fotovoltaica', 'Hidráulica']

# Función para obtener datos de la API
@st.cache_data
def obtener_datos(api_token):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Token token={api_token}'
    }

    datos = {}
    for nombre, id_tec in tecnologias.items():
        url = f'https://api.esios.ree.es/indicators/{id_tec}'
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                valores = r.json()['indicator']['values']
                datos[nombre] = valores[-1]['value'] if valores else 0
            else:
                datos[nombre] = 0
        except:
            datos[nombre] = 0
    return datos

# Mostrar resultados si hay token
if api_token:
    datos = obtener_datos(api_token)

    st.subheader("⚡ Producción actual (MW)")
    st.dataframe(datos)

    # Visualización
    colores = ['green' if t in sostenibles else 'gray' for t in datos]
    fig, ax = plt.subplots()
    ax.bar(datos.keys(), datos.values(), color=colores)
    ax.set_ylabel("Potencia (MW)")
    ax.set_title("Generación por Tecnología")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.info("Las tecnologías verdes son: Eólica, Solar fotovoltaica e Hidráulica.")
else:
    st.warning("Introduce tu API Token para obtener datos.")
