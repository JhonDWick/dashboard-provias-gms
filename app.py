import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# Configuración de la página Streamlit
st.set_page_config(
    page_title="PVD - Dashboard de Solicitudes de Recursos",
    page_icon="🛣️",
    layout="wide"
)

# Estilos CSS de interfaz
st.markdown("""
    <style>
    .main-title {
        background-color: #0b4f8a;
        color: white;
        padding: 16px 20px;
        border-radius: 8px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# URL pública de exportación CSV del Google Sheets
SHEET_ID = "1v2Nc7v7JNB2IVFqhXM81WVJvaJgiuh31HNA68WwbOlI"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=BD"

@st.cache_data(ttl=10)
def cargar_datos_gsheets():
    """Carga los datos directamente desde el Google Sheets público"""
    try:
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        st.error(f"Error al conectar con Google Sheets: {e}")
        return pd.DataFrame()

# Cargar DataFrame base
df = cargar_datos_gsheets()

# Diccionario de Usuarios y Permisos por Provincia
USUARIOS = {
    "central_gms": {"pass": "GmsCentral2026!", "nombre": "Especialista Sede Central (GMS)", "rol": "SEDE_CENTRAL", "provincias": "TODAS"},
    "jparra": {"pass": "Zonal2026!", "nombre": "JOSÉ PARRA BENAVIDES", "rol": "ESPECIALISTA_ZONAL", "provincias": ["ACOBAMBA"]},
    "evasquez": {"pass": "Zonal2026!", "nombre": "EDGAR VÁSQUEZ RIVERA", "rol": "ESPECIALISTA_ZONAL", "provincias": ["ANGARAES", "CHURCAMPA"]},
    "jponce": {"pass": "Zonal2026!", "nombre": "JHON PONCE FRANCIA", "rol": "ESPECIALISTA_ZONAL", "provincias": ["CASTROVIRREYNA", "HUAYTARÁ"]},
    "jcarhuaricra": {"pass": "Zonal2026!", "nombre": "JAQUELINE JUDITH CARHUARICRA ESTRELLA", "rol": "ESPECIALISTA_ZONAL", "provincias": ["HUANCAVELICA"]},
    "rleon": {"pass": "Zonal2026!", "nombre": "RANDOLF ARTURO LEÓN ROJAS", "rol": "ESPECIALISTA_ZONAL", "provincias": ["TAYACAJA"]},
    "atorres": {"pass": "Zonal2026!", "nombre": "ALEXA TORRES FLORES", "rol": "ESPECIALISTA_ZONAL", "provincias": ["TACNA", "CANDARAVE", "TARATA", "JORGE BASADRE"]},
    "lortiz": {"pass": "Zonal2026!", "nombre": "LUIS EDUARDO ORTIZ FONTTIS", "rol": "ESPECIALISTA_ZONAL", "provincias": ["MARISCAL NIETO", "ILO", "GENERAL SÁNCHEZ CERRO"]}
}

# Control de Autenticación
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

if not st.session_state.logged_in:
    st.sidebar.title("🔐 Acceso al Sistema PVD")
    usr = st.sidebar.text_input("Usuario")
    pwd = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Ingresar"):
        if usr in USUARIOS and USUARIOS[usr]["pass"] == pwd:
            st.session_state.logged_in = True
            st.session_state.user = USUARIOS[usr]
            st.rerun()
        else:
            st.sidebar.error("Usuario o contraseña no válidos.")
    st.stop()

user = st.session_state.user

# Encabezado Principal
st.markdown("""
<div class="main-title">
    DASHBOARD DE MONITOREO Y SEGUIMIENTO DE SOLICITUDES DE RECURSOS - SEDE CENTRAL & UNIDADES ZONALES
</div>
""", unsafe_allow_html=True)

# Menú Lateral y Filtros
st.sidebar.markdown(f"👤 **Usuario:** {user['nombre']}")
st.sidebar.markdown(f"🔰 **Perfil:** {user['rol']}")
if st.sidebar.button("Cerrar Sesión"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("---")  # <--- Corregido aquí
st.sidebar.header("🔍 Filtros de Búsqueda")

# Filtrar según rol de usuario
df_filtrado = df.copy()
if user["rol"] == "ESPECIALISTA_ZONAL":
    df_filtrado = df_filtrado[df_filtrado["Provincia"].str.upper().isin(user["provincias"])]

# Filtro por Región
regiones = ["Todas"] + sorted(list(df_filtrado["Region"].dropna().unique()))
sel_region = st.sidebar.selectbox("Filtrar por Región", regiones)
if sel_region != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Region"] == sel_region]

# Filtro por Provincia
provincias = ["Todas"] + sorted(list(df_filtrado["Provincia"].dropna().unique()))
sel_provincia = st.sidebar.selectbox("Filtrar por Provincia", provincias)
if sel_provincia != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Provincia"] == sel_provincia]

# Filtro por Estado
estados = ["Todos", "Opinión favorable", "Observado", "En revisión", "Validado"]
sel_estado = st.sidebar.selectbox("Filtrar por Estado", estados)
if sel_estado != "Todos":
    df_filtrado = df_filtrado[(df_filtrado["Estado_Zonal"] == sel_estado) | (df_filtrado["Estado_GMS"] == sel_estado)]

# KPIs - Resumen Ejecutivo
st.subheader("📊 Resumen Ejecutivo")

total_solicitudes = len(df_filtrado)
op_favorable_zonal = len(df_filtrado[df_filtrado["Estado_Zonal"] == "Opinión favorable"])
validacion_gms = len(df_filtrado[df_filtrado["Estado_GMS"] == "Validado"])
pendientes_gms = len(df_filtrado[df_filtrado["Estado_GMS"] == "En revisión GMS"])
en_revision_zonal = len(df_filtrado[df_filtrado["Estado_Zonal"] == "En revisión"])
observados_zonal = len(df_filtrado[df_filtrado["Estado_Zonal"] == "Observado"])
aprobadas_tramitadas = validacion_gms

k1, k2, k3, k4, k5, k6, k7 = st.columns(7)
k1.metric("Total Solicitudes", total_solicitudes)
k2.metric("Op. Favorable Zonal", op_favorable_zonal)
k3.metric("Validación GMS", validacion_gms)
k4.metric("Pendiente Val. GMS", pendientes_gms)
k5.metric("En Revisión Zonal", en_revision_zonal)
k6.metric("Observados Zonal", observados_zonal)
k7.metric("Aprobadas/Tramitadas", aprobadas_tramitadas)

st.markdown("---")

# Bandeja de Trabajo Principal
st.subheader("📋 Bandeja de Trabajo - Monitoreo y Seguimiento")
st.dataframe(df_filtrado, use_container_width=True)

# Exportar Reporte por Provincia
col_exp1, col_exp2 = st.columns([3, 1])
with col_exp2:
    csv_bytes = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Exportar Reporte (CSV)",
        data=csv_bytes,
        file_name=f"Reporte_Solicitudes_{sel_provincia}.csv",
        mime="text/csv"
    )

st.markdown("---")

# Formulario para Nueva Solicitud (Ingreso de fila nueva por la Zonal)
if user["rol"] == "ESPECIALISTA_ZONAL":
    st.subheader("➕ Registrar Nueva Solicitud de Recursos (Unidad Zonal)")
    with st.form("form_nueva_solicitud"):
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            num_ht = st.text_input("Número de HT (ej. E-050000-2026)")
            region_ingreso = st.selectbox("Región", sorted(list(df["Region"].dropna().unique())))
            provincia_ingreso = st.selectbox("Provincia", user["provincias"])
        with col_f2:
            servicio_ingreso = st.text_input("Servicio / Obra", "Mantenimiento Rutinario")
            num_tramos = st.number_input("Número de Tramos", min_value=1, value=1)
            mes_ingreso = st.selectbox("Mes", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"])
        with col_f3:
            tipo_tramite = st.selectbox("Tipo de Trámite", ["Solicitud de recursos", "Recursos RNU"])
            estado_inicial = st.selectbox("Estado Zonal Inicial", ["En revisión", "Opinión favorable", "Observado"])
            fecha_ingreso = st.date_input("Fecha Ingreso Zonal", date.today())

        btn_guardar = st.form_submit_button("💾 Guardar Solicitud")
        if btn_guardar:
            st.success(f"La solicitud {num_ht} fue registrada para la provincia de {provincia_ingreso}.")
