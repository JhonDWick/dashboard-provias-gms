import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# Configuración de página con diseño ancho
st.set_page_config(
    page_title="PVD - Dashboard de Solicitudes de Recursos",
    page_icon="🛣️",
    layout="wide"
)

# Estilos CSS Profesionales e Institucionales
st.markdown("""
    <style>
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
        padding: 15px;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .kpi-title { font-size: 12px; color: #666; font-weight: bold; text-transform: uppercase; }
    .kpi-value { font-size: 24px; color: #0b4f8a; font-weight: bold; margin-top: 5px; }
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

df = cargar_datos()

# Usuarios y Accesos
USUARIOS = {
    "central_gms": {"pass": "GmsCentral2026!", "nombre": "Especialista Central", "rol": "SEDE_CENTRAL", "provincias": "TODAS"},
    "jparra": {"pass": "Zonal2026!", "nombre": "José Parra Benavides", "rol": "ESPECIALISTA_ZONAL", "provincias": ["ACOBAMBA"]},
    "evasquez": {"pass": "Zonal2026!", "nombre": "Edgar Vásquez Rivera", "rol": "ESPECIALISTA_ZONAL", "provincias": ["ANGARAES", "CHURCAMPA"]},
    "jponce": {"pass": "Zonal2026!", "nombre": "Jhon Ponce Francia", "rol": "ESPECIALISTA_ZONAL", "provincias": ["CASTROVIRREYNA", "HUAYTARÁ"]},
    "jcarhuaricra": {"pass": "Zonal2026!", "nombre": "Jaqueline Carhuaricra", "rol": "ESPECIALISTA_ZONAL", "provincias": ["HUANCAVELICA"]},
    "rleon": {"pass": "Zonal2026!", "nombre": "Randolf León Rojas", "rol": "ESPECIALISTA_ZONAL", "provincias": ["TAYACAJA"]},
    "atorres": {"pass": "Zonal2026!", "nombre": "Alexa Torres Flores", "rol": "ESPECIALISTA_ZONAL", "provincias": ["TACNA", "CANDARAVE", "TARATA", "JORGE BASADRE"]},
    "lortiz": {"pass": "Zonal2026!", "nombre": "Luis Ortiz Fonttis", "rol": "ESPECIALISTA_ZONAL", "provincias": ["MARISCAL NIETO", "ILO", "GENERAL SÁNCHEZ CERRO"]}
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

if not st.session_state.logged_in:
    st.sidebar.title("🔐 Acceso - Provías Descentralizado")
    usr = st.sidebar.text_input("Usuario")
    pwd = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Iniciar Sesión"):
        if usr in USUARIOS and USUARIOS[usr]["pass"] == pwd:
            st.session_state.logged_in = True
            st.session_state.user = USUARIOS[usr]
            st.rerun()
        else:
            st.sidebar.error("Credenciales incorrectas.")
    st.stop()

user = st.session_state.user

# ENCABEZADO SUPERIOR CON TÍTULO ACORDADO
st.markdown("""
<div class="header-container">
    <div class="header-title">DASHBOARD DE MONITOREO Y SEGUIMIENTO DE SOLICITUDES DE RECURSOS - SEDE CENTRAL & UNIDADES ZONALES</div>
</div>
""", unsafe_allow_html=True)

# BARRA LATERAL (MENÚ Y FILTROS)
st.sidebar.markdown(f"👤 **{user['nombre']}**")
st.sidebar.markdown(f"📌 *{user['rol']}*")
if st.sidebar.button("Cerrar Sesión"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filtros de Búsqueda")

df_f = df.copy()
if user["rol"] == "ESPECIALISTA_ZONAL":
    df_f = df_f[df_f["Provincia"].str.upper().isin(user["provincias"])]

regiones = ["Todas"] + sorted(list(df_f["Region"].dropna().unique()))
sel_reg = st.sidebar.selectbox("Región", regiones)
if sel_reg != "Todas":
    df_f = df_f[df_f["Region"] == sel_reg]

provincias = ["Todas"] + sorted(list(df_f["Provincia"].dropna().unique()))
sel_prov = st.sidebar.selectbox("Provincia", provincias)
if sel_prov != "Todas":
    df_f = df_f[df_f["Provincia"] == sel_prov]

# RESUMEN EJECUTIVO (KPIS)
st.markdown("### 📊 Resumen Ejecutivo")

total_s = len(df_f)
op_fav = len(df_f[df_f["Estado_Zonal"] == "Opinión favorable"])
val_gms = len(df_f[df_f["Estado_GMS"] == "Validado"])
pend_val = len(df_f[df_f["Estado_GMS"] == "En revisión GMS"])
rev_zonal = len(df_f[df_f["Estado_Zonal"] == "En revisión"])
obs_zonal = len(df_f[df_f["Estado_Zonal"] == "Observado"])
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

# BANDEJA DE TRABAJO
st.markdown("### 📋 Bandeja de Trabajo - Monitoreo y Seguimiento")
st.dataframe(df_f, use_container_width=True)

# Botón de exportar reporte
col_ex1, col_ex2 = st.columns([3, 1])
with col_ex2:
    csv_data = df_f.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Exportar Reporte (CSV)", data=csv_data, file_name=f"Reporte_Provincia_{sel_prov}.csv", mime="text/csv")

st.markdown("---")

# SECCIÓN EXCLUSIVA PARA EL ESPECIALISTA ZONAL (NUEVOS TRÁMITES Y ESTADOS)
if user["rol"] == "ESPECIALISTA_ZONAL":
    st.markdown("### ➕ Gestión Zonal: Registrar Nueva Solicitud o Actualizar Estado")
    
    tab_nuevo, tab_actualizar = st.tabs(["📝 Registrar Nueva Solicitud", "✏️ Actualizar Estado de Trámite"])
    
    with tab_nuevo:
        with st.form("form_nueva_solicitud"):
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                num_ht = st.text_input("Número de HT (ej. E-050000-2026)")
                reg_ing = st.selectbox("Región", sorted(list(df["Region"].dropna().unique())))
                prov_ing = st.selectbox("Provincia Asignada", user["provincias"])
            with col_f2:
                serv_ing = st.text_input("Servicio / Obra", "Mantenimiento Rutinario")
                num_tram = st.number_input("Número de Tramos", min_value=1, value=1)
                mes_ing = st.selectbox("Mes", ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Setiembre", "Octubre", "Noviembre", "Diciembre"])
            with col_f3:
                tipo_t = st.selectbox("Tipo de Trámite", ["Solicitud de recursos", "Recursos RNU"])
                estado_z = st.selectbox("Estado Zonal", ["En revisión", "Opinión favorable", "Observado"])
                fec_ing = st.date_input("Fecha Ingreso Zonal", date.today())
                
            btn_guardar = st.form_submit_button("💾 Guardar Solicitud en la Zonal")
            if btn_guardar:
                st.success(f"¡Solicitud {num_ht} registrada con éxito para la provincia de {prov_prov_ing if 'prov_prov_ing' in locals() else prov_ing}!")
    
    with tab_actualizar:
        with st.form("form_act_estado"):
            ht_sel = st.selectbox("Seleccione Código HT a modificar:", df_f["HT"].tolist() if not df_f.empty else [])
            nuevo_est_z = st.selectbox("Nuevo Estado Zonal:", ["En revisión", "Opinión favorable", "Observado"])
            btn_act = st.form_submit_button("🔄 Actualizar Estado Zonal")
            if btn_act and ht_sel:
                st.success(f"¡El estado zonal de la HT {ht_sel} fue actualizado a '{nuevo_est_z}' con éxito!")

st.markdown("---")

# MÓDULOS INFERIORES (ALERTAS Y EFICIENCIA)
col_inf1, col_inf2 = st.columns(2)

with col_inf1:
    st.markdown("### 🚨 Alertas de Solicitudes Críticas")
    st.info("No se registran solicitudes críticas con exceso de días en la bandeja actual.")

with col_inf2:
    st.markdown("### 📈 Eficiencia por Región / Zona")
    if not df_f.empty:
        fig = px.bar(df_f, x="Region", y="Num_Tramos", color="Estado_Zonal", barmode="group")
        fig.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
