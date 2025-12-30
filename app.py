import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# 2. UI Təkmilləşdirməsi (Sidebar problemini həll edən versiya)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
    }

    /* Üst başlığı gizlət, amma sidebar düyməsini saxla */
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }

    /* SOL SİDEBAR - Stabilizasiya */
    section[data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        border-right: 1px solid #30363d !important;
        min-width: 320px !important;
    }
    
    /* Loqo Paneli */
    .brand-card {
        background: linear-gradient(135deg, #1f6feb 0%, #111827 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 2rem;
    }
    
    .brand-title {
        color: #ffffff;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin: 0;
    }
    
    .brand-subtitle {
        color: rgba(255,255,255,0.7);
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 5px;
    }

    /* Professional Düymələr */
    div.stButton > button {
        background-color: #238636 !important;
        color: white !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        height: 45px !important;
        width: 100%;
        border: none !important;
    }
    
    /* Metrika Qutuları */
    .metric-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
    }

    /* Sidebar daxili mətnlər */
    .sidebar-label {
        font-size: 11px;
        font-weight: 700;
        color: #8b949e;
        margin-top: 15px;
        text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# 3. Köməkçi Funksiyalar
def process_images(img1, img2):
    i1 = Image.open(img1)
    i2 = Image.open(img2)
    target_size = (1024, 768)
    return i1.resize(target_size, Image.Resampling.LANCZOS), i2.resize(target_size, Image.Resampling.LANCZOS)

def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA ANALYSIS REPORT", ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div class="brand-card">
        <p class="brand-title">🛰️ SATELLA AI</p>
        <p class="brand-subtitle">Geospatial Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p class='sidebar-label'>Koordinatlar</p>", unsafe_allow_html=True)
    lat_val = st.text_input("Enlik (LAT)", value="40.394799")
    lon_val = st.text_input("Uzunluq (LON)", value="49.849585")
    
    st.markdown("<p class='sidebar-label'>Şəkil Yükləmə (T0 vs T1)</p>", unsafe_allow_html=True)
    t0_file = st.file_uploader("Referans Şəkil (T0)", type=["png","jpg"])
    t1_file = st.file_uploader("Cari Şəkil (T1)", type=["png","jpg"])
    
    if st.button("ANALİZİ BAŞLAT"):
        if t0_file and t1_file:
            st.session_state.lat = float(lat_val)
            st.session_state.lon = float(lon_val)
            st.session_state.run = True
        else:
            st.warning("Zəhmət olmasa hər iki şəkli yükləyin.")

# --- ƏSAS EKRAN ---
col_map, col_metrics = st.columns([3.5, 1.5])

with col_map:
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    # Xəritə hissəsi
    m = folium.Map(location=[lat, lon], zoom_start=16)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Satellite"
    ).add_to(m)
    folium.Marker([lat, lon]).add_to(m)
    folium_static(m, width=900, height=500)
    
    # Şəkillərin yan-yana müqayisəsi
    if t0_file and t1_file:
        img1, img2 = process_images(t0_file, t1_file)
        st.markdown("### Vizual Müqayisə")
        ic1, ic2 = st.columns(2)
        ic1.image(img1, caption="2024 (T0)", use_container_width=True)
        ic2.image(img2, caption="2025 (T1)", use_container_width=True)

with col_metrics:
    st.markdown("### ANALİTİKA")
    
    stats = [
        ("AŞKARLANAN DƏYİŞİKLİK", "1 Tikinti", "#f0f6fc"),
        ("AI DƏQİQLİYİ", "92.4%", "#58a6ff"),
        ("SİSTEM STATUSU", "Aktiv", "#3fb950")
    ]
    
    for label, val, color in stats:
        st.markdown(f"""
        <div class="metric-box">
            <p style='color:#8b949e; font-size:11px; font-weight:700; margin:0'>{label}</p>
            <p style='color:{color}; font-size:24px; font-weight:800; margin:0'>{val}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.get('run', False):
        report = generate_pdf(lat, lon)
        st.download_button("📥 PDF HESABATI YÜKLƏ", data=report, file_name="satella_report.pdf", use_container_width=True)
