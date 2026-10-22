import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import base64

# Configuración de página con diseño ancho
st.set_page_config(
    page_title="PVD - Dashboard de Solicitudes de Recursos",
    page_icon="🛣️",
    layout="wide"
)

# Estilos CSS Profesionales e Institucionales
st.markdown("""
    <style>
    /* Fondo de infraestructura vial en la barra lateral con capa institucional */
    [data-testid="stSidebar"] {
        background-image: linear-gradient(rgba(11, 79, 138, 0.90), rgba(11, 79, 138, 0.90)), url("https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?q=80&w=1000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        color: white;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: white !important;
    }
    .header-container {
        background-color: #0b4f8a;
        padding: 12px 20px;
        border-radius: 6px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 20px;
        font-weight: bold;
        color: white;
        margin: 0;
        text-align: center;
        width: 100%;
    }
    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-left: 5px solid #0b4f8a;
        padding: 12px 8px;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
        height: 95px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    .kpi-title { 
        font-size: 10px; 
        color: #555; 
        font-weight: bold; 
        text-transform: uppercase; 
        line-height: 1.2;
        margin-bottom: 4px;
    }
    .kpi-value { 
        font-size: 22px; 
        color: #0b4f8a; 
        font-weight: bold; 
        margin: 0;
    }
    /* Tarjetas de bienvenida con dimensiones estrictamente idénticas */
    .welcome-card {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-top: 4px solid #0b4f8a;
        padding: 22px 18px;
        border-radius: 8px;
        text-align: center;
        height: 185px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
    .welcome-card h4 {
        font-size: 16px;
        color: #0b4f8a;
        margin-bottom: 10px;
        margin-top: 0;
    }
    .welcome-card p {
        font-size: 13px;
        color: #555;
        line-height: 1.4;
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# URL del Google Sheets
SHEET_ID = "1v2Nc7v7JNB2IVFqhXM81WVJvaJgiuh31HNA68WwbOlI"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=BD"

@st.cache_data(ttl=10)
def cargar_datos():
    try:
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        return pd.DataFrame()

df = cargar_
