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

# Estilos CSS Profesionales e Institucionales (Solución forzada para texto de botones)
st.markdown("""
    <style>
    /* Fondo de infraestructura vial en la barra lateral con capa institucional */
    [data-testid="stSidebar"] {
        background-image: linear-gradient(rgba(11, 79, 138, 0.92), rgba(11, 79, 138, 0.92)), url("https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?q=80&w=1000&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        color: white;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: white !important;
    }
    
    /* FORZAR COLOR OSCURO EN TODO TEXTO O ELEMENTO DENTRO DE LOS BOTONES */
    div.stButton > button {
        background-color: #ffffff !important;
        border: 2px solid #ffffff !important;
        border-radius: 6px !important;
        width: 100% !important;
        height: 42px !important;
    }
    div.stButton > button * {
        color: #0b4f8a !important;
        font-weight: 800 !important;
        font-size: 15px !important;
    }
    div.stButton > button:hover {
        background-color: #e2e8f0 !important;
        border-color: #e2e8f0 !important;
    }
    div.stButton > button:hover * {
        color: #072e52 !important;
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

df = cargar_datos()

# Función para convertir imágenes locales a Base64 probando varias rutas/nombres exactos
def img_to_base64(possible_names):
    for name in possible_names:
        try:
            with open(name, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except Exception:
            continue
    return ""

# Buscar las imágenes con los nombres exactos
img_transp_b64 = img_to_base64(["Consulta Amigable.png", "consulta amigable.png", "transparencia.png"])
img_transf_b64 = img_to_base64(["Consulta Transferencia.png", "consulta transferencia.png", "transferencia.png"])

# Usuarios y Asignación Exacta de Provincias según Cuadro Oficial
USUARIOS = {
    "central_gms": {"pass": "GmsCentral2026!", "nombre": "Especialista Sede Central", "rol": "SEDE_CENTRAL", "provincias": "TODAS"},
    "jparra": {"pass": "Zonal2026!", "nombre": "José Parra Benavides", "rol": "ESPECIALISTA_ZONAL", "provincias": ["ACOBAMBA"]},
    "evasquez": {"pass": "Zonal2026!", "nombre": "Edgar Vásquez Rivera", "rol": "ESPECIALISTA_ZONAL", "provincias": ["ANGARAES", "CHURCAMPA"]},
    "jponce": {"pass": "Zonal2026!", "nombre": "Jhon Ponce Francia", "rol": "ESPECIALISTA_ZONAL", "provincias": ["CASTROVIRREYNA", "HUAYTARÁ"]},
    "jcarhuaricra": {"pass": "Zonal2026!", "nombre": "Jaqueline Judith Carhuaricra Estrella", "rol": "ESPECIALISTA_ZONAL", "provincias": ["HUANCAVELICA"]},
    "rleon": {"pass": "Zonal2026!", "nombre": "Randolf Arturo León Rojas", "rol": "ESPECIALISTA_ZONAL", "provincias": ["TAYACAJA"]},
    "atorres": {"pass": "Zonal2026!", "nombre": "Alexa Torres Flores", "rol": "ESPECIALISTA_ZONAL", "provincias": ["TACNA", "CANDARAVE", "TARATA", "JORGE BASADRE"]},
    "lortiz": {"pass": "Zonal2026!", "nombre": "Luis Eduardo Ortiz Fonttis", "rol": "ESPECIALISTA_ZONAL", "provincias": ["MARISCAL NIETO", "ILO", "GENERAL SANCHEZ CERRO"]}
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

# BARRA LATERAL CON CREDENCIALES DE ACCESO
st.sidebar.title("🔐 Acceso al Sistema")
st.sidebar.markdown("---")

if not st.session_state.logged_in:
    usr = st.sidebar.text_input("Usuario")
    pwd = st.sidebar.text_input("Contraseña", type="password")
    
    # Botón con etiqueta directa
    if st.sidebar.button("INICIAR SESIÓN", key="btn_login"):
        if usr in USUARIOS and USUARIOS[usr]["pass"] == pwd:
            st.session_state.logged_in = True
            st.session_state.user = USUARIOS[usr]
            st.rerun()
        else:
            st.sidebar.error("Usuario o contraseña incorrectos.")
    
    # PANTALLA DE BIENVENIDA INSTITUCIONAL CON LOGOS MEF
    st.markdown("""
        <div style="background-color: #0b4f8a; padding: 25px; border-radius: 8px; color: white; text-align: center; margin-bottom: 25px;">
            <h1 style="color: white; margin: 0; font-size: 26px;">MINISTERIO DE TRANSPORTES Y COMUNICACIONES</h1>
            <h3 style="color: #e0e0e0; margin-top: 8px; font-weight: normal; font-size: 18px;">PROVÍAS DESCENTRALIZADO — GERENCIA DE MONITOREO Y SEGUIMIENTO (GMS)</h3>
        </div>
    """, unsafe_allow_html=True)

    col_title, col_links = st.columns([3, 1])
    with col_title:
        st.markdown("### 🌐 Plataforma de Monitoreo y Gestión de Solicitudes de Recursos Financieros")
    with col_links:
        html_transp = f'<img src="data:image/png;base64,{img_transp_b64}" style="height: 35px; width: auto; border-radius: 4px;" alt="Consulta Amigable"/>' if img_transp_b64 else '<span style="font-size: 13px; font-weight: bold; color: #0b4f8a;">Consulta Amigable</span>'
        html_transf = f'<img src="data:image/png;base64,{img_transf_b64}" style="height: 35px; width: auto; border-radius: 4px;" alt="Consulta Transferencia"/>' if img_transf_b64 else '<span style="font-size: 13px; font-weight: bold; color: #0b4f8a;">Consulta Transferencia</span>'

        st.markdown(
            f"""
            <div style="text-align: right; padding-top: 5px; display: flex; justify-content: flex-end; gap: 15px; align-items: center;">
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

    st.write("Sistema informático orientado al seguimiento, control de estados y tramitación de recursos para el mantenimiento rutinario de caminos vecinales a nivel nacional.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_w1, col_w2, col_w3 = st.columns(3)
    with col_w1:
        st.markdown("""
            <div class="welcome-card">
                <h4>🛣️ Cobertura Zonal</h4>
                <p>Supervisión descentralizada en las jurisdicciones viales de las regiones de <b>Tacna, Moquegua y Huancavelica</b>.</p>
            </div>
        """, unsafe_allow_html=True)
    with col_w2:
        st.markdown("""
            <div class="welcome-card">
                <h4>📊 Trazabilidad en Línea</h4>
                <p>Control automatizado de Hojas de Trámite (HT), opiniones favorables y validaciones centrales en tiempo real.</p>
            </div>
        """, unsafe_allow_html=True)
    with col_w3:
        st.markdown("""
            <div class="welcome-card">
                <h4>👥 Acceso por Roles</h4>
                <p>Perfiles diferenciados y seguros para Especialistas de Unidades Zonales y Especialistas de Sede Central.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👈 **Instrucción:** Por favor, ingrese su usuario y contraseña asignados en el panel lateral izquierdo para acceder al sistema.")
    st.stop()

user = st.session_state.user

# ENCABEZADO SUPERIOR DEL DASHBOARD
st.markdown("""
<div class="header-container">
    <div class="header-title">DASHBOARD DE MONITOREO Y SEGUIMIENTO DE SOLICITUDES DE RECURSOS - SEDE CENTRAL & UNIDADES ZONALES</div>
</div>
""", unsafe_allow_html=True)

# BARRA LATERAL CON DATOS DE USUARIO AUTENTICADO
st.sidebar.markdown(f"👤 **{user['nombre']}**")
st.sidebar.markdown(f"📌 *{user['rol']}*")
if user["rol"] == "ESPECIALISTA_ZONAL":
    st.sidebar.markdown(f"📍 **Provincias a cargo:** {', '.join(user['provincias'])}")

if st.sidebar.button("CERRAR SESIÓN", key="btn_logout"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filtros de Búsqueda")

df_f = df.copy()

# APLICAR FILTRO ESTRICTO DE PROVINCIAS SEGÚN EL ROL
if user["rol"] == "ESPECIALISTA_ZONAL":
    provincias_usuario = [p.strip().upper() for p in user["provincias"]]
    df_f = df_f[df_f["Provincia"].astype(str).str.strip().str.upper().isin(provincias_usuario)]

# Filtro por Región
regiones = ["Todas"] + sorted(list(df_f["Region"].dropna().unique()))
sel_reg = st.sidebar.selectbox("Región", regiones)
if sel_reg != "Todas":
    df_f = df_f[df_f["Region"] == sel_reg]

# Filtro por Provincia
provincias_disponibles = ["Todas"] + sorted(list(df_f["Provincia"].dropna().unique()))
sel_prov = st.sidebar.selectbox("Provincia", provincias_disponibles)
if sel_prov != "Todas":
    df_f = df_f[df_f["Provincia"] == sel_prov]

# RESUMEN EJECUTIVO (KPIS CON TAMAÑOS UNIFORMES)
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

# 1. BANDEJA EXCLUSIVA PARA SEDE CENTRAL (ÚLTIMAS 6 ACTUALIZACIONES ORDENADAS DE MÁS RECIENTE A MÁS ANTIGUA)
if user["rol"] == "SEDE_CENTRAL":
    st.markdown("### 🔔 Bandeja de Actualizaciones Recientes de Unidades Zonales")
    st.info("Monitoreo en tiempo real de los trámites que registran avances, opiniones favorables u observaciones en regiones (Últimas 6 actualizaciones).")
    
    df_actualizaciones = df.copy()
    if "Fecha_Opinion_Zonal" in df_actualizaciones.columns:
        df_actualizaciones["Fecha_Temp"] = pd.to_datetime(df_actualizaciones["Fecha_Opinion_Zonal"], errors="coerce")
        df_actualizaciones = df_actualizaciones.sort_values(by="Fecha_Temp", ascending=False).head(6)
        df_actualizaciones = df_actualizaciones.drop(columns=["Fecha_Temp"])
    
    st.dataframe(
        df_actualizaciones[["HT", "Region", "Provincia", "Servicio", "Estado_Zonal", "Fecha_Opinion_Zonal", "Estado_GMS"]],
        use_container_width=True
    )
    st.markdown("---")

# 2. BANDEJA DE TRABAJO PRINCIPAL
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
                st.success(f"¡Solicitud {num_ht} registrada con éxito para la provincia de {prov_ing}!")
    
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
