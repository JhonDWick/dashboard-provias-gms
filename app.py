# CONEXIÓN CON GSPREAD VÍA STREAMLIT SECRETS (CON DEPORACIÓN VISIBLE)
@st.cache_resource
def conectar_google_sheets():
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials_dict = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(credentials_dict, scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).worksheet("BD")
        return sheet
    except Exception as e:
        st.error(f"❌ ERROR EXACTO DE CONEXIÓN: {e}")
        return None

sheet_bd = conectar_google_sheets()
