import streamlit as st
import requests
import matplotlib.pyplot as plt

# Cargar token desde secrets (debes definirlo como ESIOS_API_TOKEN en Streamlit Cloud)
api_token = st.secrets["ESIOS_API_TOKEN"]

# Configuración de la página
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

# Función para obtener los datos de la API de e-sios
@st.cache_data
def obtener_datos(api_token):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': api_token  # CORRECTA AUTENTICACIÓN
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
                datos[nombre] = f"Error {r.status_code}"
        except Exception as e:
            datos[nombre] = f"Error: {e}"
    return datos

# Mostrar resultados
datos = obtener_datos(api_token)

st.subheader("⚡ Producción actual (MW)")
st.write("Datos en tiempo real desde la API de Red Eléctrica de España (e-sios).")
st.dataframe(datos)

# Visualización gráfica
# Solo pintar valores numéricos
valores_numericos = {k: v for k, v in datos.items() if isinstance(v, (int, float))}
colores = ['green' if t in sostenibles else 'gray' for t in valores_numericos]

fig, ax = plt.subplots()
ax.bar(valores_numericos.keys(), valores_numericos.values(), color=colores)
ax.set_ylabel("Potencia (MW)")
ax.set_title("Generación por Tecnología")
plt.xticks(rotation=45)
st.pyplot(fig)

st.info("Las tecnologías verdes son: Eólica, Solar fotovoltaica e Hidráulica.")
