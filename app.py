import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import base64
import requests
import io

# Configuración de página con diseño ancho
st.set_page_config(
    page_title="PVD - Dashboard de Solicitudes de Recursos",
    page_icon="🛣️",
    layout="wide"
)

# Estilos CSS Profesionales con Fondo Ejecutivo e Institucional
st.markdown("""
    <style>
    .stApp {
        background-color: #f8fafc !important;
    }
    [data-testid="stSidebar"] {
        background-image: linear-gradient(rgba(220, 38, 38, 0.94), rgba(185, 28, 28, 0.94)), url("https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?q=80&w=1000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        color: white;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: white !important;
    }
    div.stButton > button {
        background-color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 6px !important;
        width: 100% !important;
        height: 42px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    div.stButton > button * {
        color: #dc2626 !important;
        font-weight: 800 !important;
        font-size: 15px !important;
    }
    div.stButton > button:hover {
        background-color: #ffeeef !important;
        border-color: #ffeeef !important;
    }
    div.stButton > button:hover * {
        color: #991b1b !important;
    }

    .header-container {
        background-color: #dc2626;
        padding: 14px 22px;
        border-radius: 8px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(220, 38, 38, 0.2);
    }
    .header-title {
        font-size: 20px;
        font-weight: bold;
        color: white;
        margin: 0;
        text-align: center;
        width: 100%;
        letter-spacing: 0.5px;
    }
    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 5px solid #dc2626;
        padding: 14px 10px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
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
        color: #64748b; 
        font-weight: bold; 
        text-transform: uppercase; 
        line-height: 1.2;
        margin-bottom: 4px;
    }
    .kpi-value { 
        font-size: 22px; 
        color: #dc2626; 
        font-weight: bold; 
        margin: 0;
    }
    .welcome-card-header {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #dc2626;
        padding: 12px;
        border-radius: 8px 8px 0 0;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .welcome-card-header h4 {
        font-size: 15px;
        color: #dc2626;
        margin: 0;
        font-weight: bold;
    }
    .formal-subtitle {
        font-family: 'Arial', sans-serif;
        font-size: 22px;
        font-weight: 800;
        color: #1e293b;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# URL e Identificador del Google Sheets
SHEET_ID = "1v2Nc7v7JNB2IVFqhXM81WVJvaJgiuh31HNA68WwbOlI"

@st.cache_data(ttl=5)
def cargar_datos():
    try:
        CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=BD"
        df_loaded = pd.read_csv(CSV_URL)
        return df_loaded
    except Exception as e:
        st.error(f"❌ Error al cargar los datos de Google Sheets: {e}")
        return pd.DataFrame()

df = cargar_datos()

if not df.empty and "Provincia" in df.columns:
    df["Provincia_Formateada"] = df["Provincia"].astype(str).str.strip().str.title()
    if "Fecha_Ingreso_Zonal" in df.columns:
        df["_Fecha_Temp"] = pd.to_datetime(df["Fecha_Ingreso_Zonal"], errors="coerce")
        df = df.sort_values(by="_Fecha_Temp", ascending=False).drop(columns=["_Fecha_Temp"])
else:
    df["Provincia_Formateada"] = "Sin información"

def img_to_base64(possible_names):
    for name in possible_names:
        try:
            with open(name, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except Exception:
            continue
    return ""

img_transp_b64 = img_to_base64(["Consulta Amigable.png", "consulta amigable.png", "transparencia.png"])
img_transf_b64 = img_to_base64(["Consulta Transferencia.png", "consulta transferencia.png", "transferencia.png"])

USUARIOS = {
    "central_gms": {"pass": "GmsCentral2026!", "nombre": "Especialista Sede Central", "rol": "SEDE_CENTRAL", "provincias": "TODAS", "regiones": ["Huancavelica", "Moquegua", "Tacna"]},
    "jparra": {"pass": "Zonal2026!", "nombre": "José Parra Benavides", "rol": "ESPECIALISTA_ZONAL", "provincias": ["ACOBAMBA"], "regiones": ["Huancavelica"]},
    "evasquez": {"pass": "Zonal2026!", "nombre": "Edgar Vásquez Rivera", "rol": "ESPECIALISTA_ZONAL", "provincias": ["ANGARAES", "CHURCAMPA"], "regiones": ["Huancavelica"]},
    "jponce": {"pass": "Zonal2026!", "nombre": "Jhon Ponce Francia", "rol": "ESPECIALISTA_ZONAL", "provincias": ["CASTROVIRREYNA", "HUAYTARÁ"], "regiones": ["Huancavelica"]},
    "jcarhuaricra": {"pass": "Zonal2026!", "nombre": "Jaqueline Judith Carhuaricra Estrella", "rol": "ESPECIALISTA_ZONAL", "provincias": ["HUANCAVELICA"], "regiones": ["Huancavelica"]},
    "rleon": {"pass": "Zonal2026!", "nombre": "Randolf Arturo León Rojas", "rol": "ESPECIALISTA_ZONAL", "provincias": ["TAYACAJA"], "regiones": ["Huancavelica"]},
    "atorres": {"pass": "Zonal2026!", "nombre": "Alexa Torres Flores", "rol": "ESPECIALISTA_ZONAL", "provincias": ["TACNA", "CANDARAVE", "TARATA", "JORGE BASADRE"], "regiones": ["Tacna"]},
    "lortiz": {"pass": "Zonal2026!", "nombre": "Luis Eduardo Ortiz Fonttis", "rol": "ESPECIALISTA_ZONAL", "provincias": ["MARISCAL NIETO", "ILO", "GENERAL SANCHEZ CERRO"], "regiones": ["Moquegua"]}
}

query_params = st.query_params
usr_param = query_params.get("u", None)

if usr_param and usr_param in USUARIOS:
    st.session_state.logged_in = True
    st.session_state.user = USUARIOS[usr_param]
    st.session_state.usr_key = usr_param
elif "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

st.sidebar.title("🔐 Acceso al Sistema")
st.sidebar.markdown("---")

if not st.session_state.logged_in:
    usr = st.sidebar.text_input("Usuario")
    pwd = st.sidebar.text_input("Contraseña", type="password")
    
    if st.sidebar.button("INICIAR SESIÓN", key="btn_login"):
        if usr in USUARIOS and USUARIOS[usr]["pass"] == pwd:
            st.session_state.logged_in = True
            st.session_state.user = USUARIOS[usr]
            st.session_state.usr_key = usr
            st.query_params["u"] = usr
            st.rerun()
        else:
            st.sidebar.error("Usuario o contraseña incorrectos.")
    
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; font-size: 13px; font-weight: bold; margin-bottom: 8px; color: white;'>ENLACES DE INTERÉS MEF</p>", unsafe_allow_html=True)
    
    html_transp = f'<img src="data:image/png;base64,{img_transp_b64}" style="max-height: 45px; width: auto; border-radius: 4px; background-color: white; padding: 4px;" alt="Consulta Amigable"/>' if img_transp_b64 else '<span style="font-size: 13px; font-weight: bold; color: white;">Consulta Amigable</span>'
    html_transf = f'<img src="data:image/png;base64,{img_transf_b64}" style="max-height: 45px; width: auto; border-radius: 4px; background-color: white; padding: 4px;" alt="Consulta Transferencia"/>' if img_transf_b64 else '<span style="font-size: 13px; font-weight: bold; color: white;">Consulta Transferencia</span>'

    st.sidebar.markdown(
        f"""
        <div style="text-align: center; display: flex; flex-direction: column; gap: 12px; align-items: center; padding-bottom: 20px;">
            <a href="https://apps5.mineco.gob.pe/transparencia/Navegador/default.aspx?y=2026&ap=Actividad" target="_blank" title="Consulta Amigable MEF">
                {html_transp}
            </a>
            <a href="https://apps5.mineco.gob.pe/transferencias/gl/default.aspx" target="_blank" title="Consulta de Transferencias MEF">
                {html_transf}
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("""
        <div style="background-color: #dc2626; padding: 25px; border-radius: 8px; color: white; text-align: center; margin-bottom: 25px; box-shadow: 0 4px 6px -1px rgba(220, 38, 38, 0.2);">
            <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 800;">PROVÍAS DESCENTRALIZADO</h1>
            <h3 style="color: #fef2f2; margin-top: 8px; font-weight: normal; font-size: 17px;">COORDINACIÓN DE MANTENIMIENTO VIAL — GERENCIA DE MONITOREO Y SEGUIMIENTO (GMS)</h3>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="formal-subtitle">🌐 PLATAFORMA DE MONITOREO Y GESTIÓN</div>', unsafe_allow_html=True)
    st.write("Sistema informático orientado al seguimiento, control de estados y tramitación de recursos para el mantenimiento rutinario de caminos vecinales a nivel nacional.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_w1, col_w2, col_w3 = st.columns(3)
    
    with col_w1:
        st.markdown('<div class="welcome-card-header"><h4>🛣️ Cobertura Zonal</h4></div>', unsafe_allow_html=True)
        if not df.empty and "Region" in df.columns:
            df_reg = df.groupby("Region", as_index=False).size()
            df_reg.columns = ["Región", "Solicitudes"]
            fig_w1 = px.bar(
                df_reg, x="Solicitudes", y="Región", orientation="h",
                color_discrete_sequence=["#dc2626"], text="Solicitudes"
            )
            fig_w1.update_layout(
                height=180, margin=dict(l=5, r=5, t=10, b=10),
                xaxis_title="", yaxis_title="", showlegend=False,
                paper_bgcolor="white", plot_bgcolor="white"
            )
            st.plotly_chart(fig_w1, use_container_width=True)
        else:
            st.info("Cargando cobertura zonal...")

    with col_w2:
        st.markdown('<div class="welcome-card-header"><h4>📊 Trazabilidad en Línea</h4></div>', unsafe_allow_html=True)
        if not df.empty and "Estado_Zonal" in df.columns:
            df_est_z = df.groupby("Estado_Zonal", as_index=False).size()
            df_est_z.columns = ["Estado", "Cantidad"]
            fig_w2 = px.pie(
                df_est_z, values="Cantidad", names="Estado", hole=0.5,
                color_discrete_sequence=["#2563eb", "#60a5fa", "#1d4ed8"]
            )
            fig_w2.update_layout(
                height=180, margin=dict(l=5, r=5, t=10, b=10),
                showlegend=True, legend=dict(orientation="h", y=-0.2),
                paper_bgcolor="white", plot_bgcolor="white"
            )
            st.plotly_chart(fig_w2, use_container_width=True)
        else:
            st.info("Cargando estados zonales...")

    with col_w3:
        st.markdown('<div class="welcome-card-header"><h4>👥 Validaciones GMS</h4></div>', unsafe_allow_html=True)
        if not df.empty and "Estado_GMS" in df.columns:
            df_est_gms = df.groupby("Estado_GMS", as_index=False).size()
            df_est_gms.columns = ["Estado GMS", "Cantidad"]
            fig_w3 = px.pie(
                df_est_gms, values="Cantidad", names="Estado GMS", hole=0.5,
                color_discrete_sequence=["#16a34a", "#22c55e", "#15803d"]
            )
            fig_w3.update_layout(
                height=180, margin=dict(l=5, r=5, t=10, b=10),
                showlegend=True, legend=dict(orientation="h", y=-0.2),
                paper_bgcolor="white", plot_bgcolor="white"
            )
            st.plotly_chart(fig_w3, use_container_width=True)
        else:
            st.info("Cargando validaciones GMS...")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👈 **Instrucción:** Por favor, ingrese su usuario y contraseña asignados en el panel lateral izquierdo para acceder al sistema.")
    st.stop()

user = st.session_state.user

st.markdown("""
<div class="header-container">
    <div class="header-title">DASHBOARD DE MONITOREO Y SEGUIMIENTO DE SOLICITUDES DE RECURSOS - SEDE CENTRAL & UNIDADES ZONALES</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"👤 **{user['nombre']}**")
st.sidebar.markdown(f"📌 *{user['rol']}*")
if user["rol"] == "ESPECIALISTA_ZONAL":
    st.sidebar.markdown(f"📍 **Provincias a cargo:** {', '.join(user['provincias'])}")

if st.sidebar.button("CERRAR SESIÓN", key="btn_logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.query_params.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filtros de Búsqueda")

df_f = df.copy()

if user["rol"] == "ESPECIALISTA_ZONAL":
    provincias_usuario = [p.strip().upper() for p in user["provincias"]]
    df_f = df_f[df_f["Provincia"].astype(str).str.strip().str.upper().isin(provincias_usuario)]

regiones = ["Todas"] + sorted(list(df_f["Region"].dropna().unique()))
sel_reg = st.sidebar.selectbox("Región", regiones)
if sel_reg != "Todas":
    df_f = df_f[df_f["Region"] == sel_reg]

provincias_disponibles = ["Todas"] + sorted(list(df_f["Provincia"].dropna().unique()))
sel_prov = st.sidebar.selectbox("Provincia", provincias_disponibles)
if sel_prov != "Todas":
    df_f = df_f[df_f["Provincia"] == sel_prov]

if user["rol"] == "ESPECIALISTA_ZONAL":
    st.markdown("### ➕ Gestión Zonal: Visualización y Monitoreo")
    st.info("Nota: Las consultas se encuentran sincronizadas en tiempo real con la base de datos de Google Sheets.")

st.markdown("### 📊 Resumen Ejecutivo")

total_s = len(df_f)
op_fav = len(df_f[df_f["Estado_Zonal"] == "Opinión favorable"]) if "Estado_Zonal" in df_f.columns else 0
val_gms = len(df_f[df_f["Estado_GMS"] == "Validado"]) if "Estado_GMS" in df_f.columns else 0
pend_val = len(df_f[df_f["Estado_GMS"] == "En revisión GMS"]) if "Estado_GMS" in df_f.columns else 0
rev_zonal = len(df_f[df_f["Estado_Zonal"] == "En revisión"]) if "Estado_Zonal" in df_f.columns else 0
obs_zonal = len(df_f[df_f["Estado_Zonal"] == "Observado"]) if "Estado_Zonal" in df_f.columns else 0
aprobadas = val_gms

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
with c1: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Solicitudes</div><div class="kpi-value">{total_s}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Op. Favorable Zonal</div><div class="kpi-value">{op_fav}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Validación GMS</div><div class="kpi-value">{val_gms}</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Pendiente GMS</div><div class="kpi-value">{pend_val}</div></div>', unsafe_allow_html=True)
with c5: st.markdown(f'<div class="kpi-card"><div class="kpi-title">En Revisión Zonal</div><div class="kpi-value">{rev_zonal}</div></div>', unsafe_allow_html=True)
with c6: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Observados</div><div class="kpi-value">{obs_zonal}</div></div>', unsafe_allow_html=True)
with c7: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Aprobadas/Tramitadas</div><div class="kpi-value">{aprobadas}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("### 📋 Bandeja de Trabajo - Monitoreo y Seguimiento")
st.dataframe(df_f, use_container_width=True)

col_ex1, col_ex2 = st.columns([3, 1])
with col_ex2:
    csv_data = df_f.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Exportar Reporte (CSV)", data=csv_data, file_name=f"Reporte_Provincia_{sel_prov}.csv", mime="text/csv")

st.markdown("---")

col_inf1, col_inf2 = st.columns(2)

with col_inf1:
    st.markdown("### 🚨 Alertas de Solicitudes Críticas")
    st.info("No se registran solicitudes críticas con exceso de días en la bandeja actual.")

with col_inf2:
    st.markdown("### 📈 Eficiencia: Trámites por Provincia y Mes")
    if not df_f.empty and "Mes" in df_f.columns and "Num_Tramos" in df_f.columns:
        ORDEN_MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        
        df_eficiencia = df_f.groupby(["Provincia_Formateada", "Mes"], as_index=False)["Num_Tramos"].sum()
        df_eficiencia["Mes"] = pd.Categorical(df_eficiencia["Mes"], categories=ORDEN_MESES, ordered=True)
        df_eficiencia = df_eficiencia.sort_values("Mes")
        
        fig = px.bar(
            df_eficiencia, 
            x="Provincia_Formateada", 
            y="Num_Tramos", 
            color="Mes", 
            barmode="group",
            category_orders={"Mes": ORDEN_MESES},
            labels={
                "Provincia_Formateada": "Provincia", 
                "Num_Tramos": "Cantidad de Tramos / Trámites",
                "Mes": "Mes"
            }
        )
        fig.update_layout(
            height=340, 
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(tickangle=0),
            paper_bgcolor="white", plot_bgcolor="white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No se cuenta con la información necesaria en la base de datos para graficar la eficiencia.")
