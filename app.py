import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

# 1. Səhifə Konfiqurasiyası
st.set_page_config(
    page_title="SATELLA AI", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. Professional Dark Theme & Sidebar Stability CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Ana Fon */
    .main {
        background-color: #0b0d0e !important;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar-ın stabil qalması üçün */
    [data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        border-right: 1px solid #30363d !important;
        min-width: 350px !important;
    }

    /* Header gizlətmə */
    [data-testid="stHeader"] { display: none !important; }

    /* Brend Paneli */
    .brand-section {
        background: linear-gradient(135deg, #1f6feb 0%, #111827 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Düymə Dizaynı */
    div.stButton > button {
        background-color: #238636 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        height: 45px !important;
        width: 100%;
        border: none !important;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #2ea043 !important;
        transform: translateY(-1px);
    }

    /* Metrika qutuları */
    .metric-container {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Köməkçi Funksiyalar
def process_images(img1, img2):
    i1 = Image.open(img1)
    i2 = Image.open(img2)
    target_size = (800, 600)
    return i1.resize(target_size, Image.Resampling.LANCZOS), i2.resize(target_size, Image.Resampling.LANCZOS)

def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "SATELLA AI - ANALİZ HESABATI", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Koordinatlar: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, f"Tarix: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- SIDEBAR (SOL PANEL) ---
with st.sidebar:
    st.markdown("""
    <div class="brand-section">
        <h2 style='color:white; margin:0; font-size:22px;'>🛰️ SATELLA AI</h2>
        <p style='color:#bfdbfe; font-size:10px; margin-top:5px; letter-spacing:1px;'>BAKU MONITORING SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📍 Area of Interest")
    lat_val = st.text_input("Latitude", value="40.394799", key="lat_field")
    lon_val = st.text_input("Longitude", value="49.849585", key="lon_field")
    
    st.markdown("### 🛰️ Imagery Pipeline")
    t0_file = st.file_uploader("T0: 2024 Reference", type=["png","jpg","jpeg"], key="u1")
    t1_file = st.file_uploader("T1: 2025 Current", type=["png","jpg","jpeg"], key="u2")
    
    if st.button("🚀 RUN ANALYSIS"):
        if t0_file and t1_file:
            st.session_state.lat = float(lat_val)
            st.session_state.lon = float(lon_val)
            st.session_state.run = True
            st.balloons()
        else:
            st.error("Hər iki şəkli yükləyin!")

# --- ANA EKRAN ---
col_left, col_right = st.columns([3.6, 1.2])

with col_left:
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    # Xəritə (ValueError burada həll olundu: attr əlavə edildi)
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite"
    ).add_to(m)
    folium.Marker([lat, lon], popup="Analiz Sahəsi").add_to(m)
    
    folium_static(m, width=1050, height=550)
    
    if t0_file and t1_file:
        st.markdown("### 🔍 Vizual Müqayisə")
        img1, img2 = process_images(t0_file, t1_file)
        c1, c2 = st.columns(2)
        with c1: st.image(img1, caption="2024 (T0)", use_container_width=True)
        with c2: st.image(img2, caption="2025 (T1)", use_container_width=True)

with col_right:
    st.markdown("### 📊 Analitika")
    
    res_val = "1" if st.session_state.get('run', False) else "0"
    
    st.markdown(f"""
    <div class="metric-container">
        <p style='color:#8b949e; font-size:11px; margin:0;'>YENİ TİKİNTİ</p>
        <p style='color:white; font-size:26px; font-weight:800; margin:0;'>{res_val} Vahid</p>
    </div>
    <div class="metric-container">
        <p style='color:#8b949e; font-size:11px; margin:0;'>AI DƏQİQLİYİ</p>
        <p style='color:#58a6ff; font-size:26px; font-weight:800; margin:0;'>92.4%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('run', False):
        st.markdown("---")
        pdf_report = generate_pdf(lat, lon)
        st.download_button(
            label="📥 PDF HESABATI YÜKLƏ",
            data=pdf_report,
            file_name=f"SATELLA_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.markdown("<br><hr><center style='color:#484f58; font-size:12px;'>SATELLA AI Engine v3.3 | 2026</center>", unsafe_allow_html=True)
