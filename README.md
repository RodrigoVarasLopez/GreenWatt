# 🌱 GreenWatt

**GreenWatt** es una aplicación web desarrollada con Streamlit que permite visualizar la generación eléctrica en España en tiempo real y comparar su evolución horaria entre diferentes días. Utiliza la API oficial de Red Eléctrica de España (e-sios).

## 🚀 Características

* Visualización en tiempo real de generación por tecnología (eólica, solar, nuclear, etc.).
* Comparativa horaria de la generación entre Hoy, Ayer y Anteayer.
* Gráficos interactivos y tabla de datos.
* Identificación visual de fuentes sostenibles vs contaminantes.

## 💡 Tecnologías Soportadas

| Tecnología         | ID API |
| ------------------ | ------ |
| Hidraulica         | 12     |
| Nuclear            | 6      |
| Eólica             | 5      |
| Solar fotovoltaica | 4      |
| Carbón             | 16     |
| Ciclo combinado    | 20     |
| Cogeneración       | 22     |

## 🪨 Instalación local

```bash
# Clonar el repositorio
https://github.com/tu-usuario/greenwatt.git
cd greenwatt

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo de secretos
mkdir .streamlit
nano .streamlit/secrets.toml
```

Contenido del archivo `.streamlit/secrets.toml`:

```toml
ESIOS_API_TOKEN = "tu_token_privado_aqui"
```

Ejecutar la app:

```bash
streamlit run app.py
```

## 🌐 Despliegue en Streamlit Cloud

1. Sube el repositorio a GitHub.
2. Accede a [streamlit.io/cloud](https://streamlit.io/cloud) e inicia sesión.
3. Selecciona tu repo y configura `app.py` como archivo principal.
4. En la sección *Secrets*, agrega:

```toml
ESIOS_API_TOKEN = "tu_token_privado"
```

5. Haz deploy y listo 🚀

## 🌿 Licencia

MIT

## 👋 Autor

**Rodrigo Varas** — Proyecto educativo Green Software (Curso Carbono)
