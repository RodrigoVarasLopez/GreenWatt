import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ============================
# CONFIGURACION
# ============================
st.set_page_config(page_title="GreenWatt", layout="centered")
st.title("🔌 GreenWatt: Generación Eléctrica por Tecnología (REE - e-sios)")

# ============================
# API TOKEN (desde secrets)
# ============================
API_TOKEN = st.secrets["ESIOS_API_TOKEN"]

headers = {
    "Accept": "application/json; application/vnd.esios-api-v1+json",
    "Content-Type": "application/json",
    "Host": "api.esios.ree.es",
    "x-api-key": API_TOKEN
}

# ============================
# TECNOLOGIAS DISPONIBLES
# ============================
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

# ============================
# FUNCIONES
# ============================
@st.cache_data
def obtener_valor_actual(indicador_id):
    url = f'https://api.esios.ree.es/indicators/{indicador_id}'
    try:
        r = requests.get(url, headers=headers)
        print(f"[{indicador_id}] → Status {r.status_code}")  # Debug
        if r.status_code == 200:
            valores = r.json()['indicator']['values']
            return valores[-1]['value'] if valores else 0
    except Exception as e:
        print(f"Error en obtener_valor_actual({indicador_id}): {e}")
    return 0

@st.cache_data
def obtener_historico(indicador_id, start_date, end_date):
    url = f"https://api.esios.ree.es/indicators/{indicador_id}?start_date={start_date}&end_date={end_date}"
    try:
        r = requests.get(url, headers=headers)
        print(f"[Hist {indicador_id}] → Status {r.status_code}")  # Debug
        if r.status_code == 200:
            valores = r.json()['indicator']['values']
            df = pd.DataFrame(valores)
            df['datetime_utc'] = pd.to_datetime(df['datetime_utc'])
            df['fecha'] = df['datetime_utc'].dt.date
            df['hora'] = df['datetime_utc'].dt.hour
            return df[['datetime_utc', 'value', 'fecha', 'hora']]
    except Exception as e:
        print(f"Error en obtener_historico({indicador_id}): {e}")
    return pd.DataFrame()

# ============================
# TABS
# ============================
tabs = st.tabs(["📊 Producción Actual", "📈 Comparativa Histórica"])

# ----------------------------
# TAB 1 - Producción Actual
# ----------------------------
with tabs[0]:
    datos_actuales = {tec: obtener_valor_actual(id_) for tec, id_ in tecnologias.items()}
    df_actual = pd.DataFrame.from_dict(datos_actuales, orient='index', columns=['value'])

    st.subheader("⚡ Producción actual (MW)")
    st.caption("Datos en tiempo real desde la API de Red Eléctrica de España (e-sios).")
    st.dataframe(df_actual)

    colores = ['green' if t in sostenibles else 'gray' for t in df_actual.index]
    fig, ax = plt.subplots()
    ax.bar(df_actual.index, df_actual['value'], color=colores)
    ax.set_ylabel("Potencia (MW)")
    ax.set_title("Generación por Tecnología")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ----------------------------
# TAB 2 - Comparativa Histórica
# ----------------------------
with tabs[1]:
    st.subheader("📅 Comparación horaria: Hoy, Ayer y Anteayer")

    tecnologia_seleccionada = st.selectbox("Selecciona una tecnología:", list(tecnologias.keys()))
    id_tecnologia = tecnologias[tecnologia_seleccionada]

    hoy = datetime.utcnow()
    ayer = hoy - timedelta(days=1)
    anteayer = hoy - timedelta(days=2)

    fecha_inicio = anteayer.replace(hour=0, minute=0)
    fecha_fin = hoy.replace(hour=23, minute=59)

    df_hist = obtener_historico(id_tecnologia, fecha_inicio.isoformat(), fecha_fin.isoformat())

    if not df_hist.empty:
        st.info("Datos en hora UTC. Cada curva representa un día.")
        import seaborn as sns

        fig, ax = plt.subplots(figsize=(12, 5))
        sns.lineplot(data=df_hist, x="hora", y="value", hue="fecha", marker="o", ax=ax)
        ax.set_title(f"Evolución horaria de la generación - {tecnologia_seleccionada}")
        ax.set_ylabel("MW")
        ax.set_xlabel("Hora del día")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.warning("No se pudieron recuperar datos históricos para esa tecnología.")
