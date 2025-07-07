import streamlit as st
import requests
import matplotlib.pyplot as plt

# Cargar token desde secrets
api_token = st.secrets["ESIOS_API_TOKEN"]

# Configuración de página
st.set_page_config(page_title="GreenWatt - Generación Eléctrica en España", layout="centered")
st.title("🔌 GreenWatt: Generación Eléctrica por Tecnología (REE - e-sios)")

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
        r = requests.get(url, headers=headers)
        st.write(f"{nombre} ({id_tec}) → Status {r.status_code}")
        if r.status_code == 200:
            json_data = r.json()
            st.write(f"{nombre}: {json_data['indicator']['short_name']}")
            valores = json_data['indicator']['values']
            if valores:
                datos[nombre] = valores[-1]['value']
            else:
                st.warning(f"No hay valores para {nombre}")
                datos[nombre] = 0
        else:
            st.error(f"Error {r.status_code} en {nombre}")
            datos[nombre] = 0
    return datos

# Mostrar resultados
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
    st.error("❌ Token no definido. Asegúrate de definirlo en el archivo `.env`")
