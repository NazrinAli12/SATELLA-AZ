import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# 2. UI Təkmilləşdirməsi (Enterprise Dark Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Ümumi fon və font */
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
    }

    [data-testid="stHeader"] { display: none; }

    /* SOL SİDEBAR - Ölçüləri bərpa etdik */
    section[data-testid="stSidebar"] {
        width: 320px !important;
        background-color: #0d1117 !important;
        border-right: 1px solid #30363d !important;
    }
    
    /* Loqo Paneli - "Toy" rəngindən "Enterprise" rənginə */
    .brand-card {
        background: linear-gradient(135deg, #1f6feb 0%, #111827 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .brand-title {
        color: #ffffff;
        font-size: 20px;
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
        border: 1px solid rgba(255,255,255,0.1) !important;
        font-weight: 600 !important;
        height: 42px !important;
        width: 100%;
        transition: all 0.2s;
    }
    
    div.stButton > button:hover {
        background-color: #2ea043 !important;
        transform: translateY(-1px);
    }

    /* Sidebar Etiketləri */
    .sidebar-label {
        font-size: 11px;
        font-weight: 700;
        color: #8b949e;
        margin-top: 20px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Metrika Qutuları */
    .metric-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
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

# --- SOL SIDEBAR (Bura qayıtdı) ---
with st.sidebar:
    st.markdown("""
    <div class="brand-card">
        <p class="brand-title">🛰️ SATELLA AI</p>
        <p class="brand-subtitle">Geospatial Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p class='sidebar-label'>Target Parameters</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        lat_val = st.text_input("LAT", value="40.394799", label_visibility="collapsed")
    with c2:
        lon_val = st.text_input("LON", value="49.849585", label_visibility="collapsed")
    
    st.markdown("<p class='sidebar-label'>Imagery Pipeline</p>", unsafe_allow_html=True)
    t0_file = st.file_uploader("Baseline (T0)", type=["png","jpg"], key="u1")
    t1_file = st.file_uploader("Current (T1)", type=["png","jpg"], key="u2")
    
    if st.button("RUN ANALYSIS"):
        if t0_file and t1_file:
            st.session_state.lat = float(lat_val)
            st.session_state.lon = float(lon_val)
            st.session_state.run = True
        else:
            st.warning("Please upload both images.")

# --- ƏSAS EKRAN ---
col_map, col_metrics = st.columns([3.8, 1.2])

with col_map:
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    # Xəritə
    m = folium.Map(location=[lat, lon], zoom_start=17, tiles=None)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri"
    ).add_to(m)
    folium.Marker([lat, lon]).add_to(m)
    folium_static(m, width=1100, height=550)
    
    # Şəkillərin müqayisəsi
    if t0_file and t1_file:
        st.markdown("---")
        img1, img2 = process_images(t0_file, t1_file)
        ic1, ic2 = st.columns(2)
        ic1.image(img1, caption="Baseline Reference", use_container_width=True)
        ic2.image(img2, caption="Current Analysis", use_container_width=True)

with col_metrics:
    st.markdown("<p style='font-weight:700; color:#f0f6fc; margin-bottom:15px'>ANALYTICS ENGINE</p>", unsafe_allow_html=True)
    
    stats = [
        ("DETECTION", "1 Units", "#f0f6fc"),
        ("AI CONFIDENCE", "92.4%", "#58a6ff"),
        ("SYSTEM STATUS", "Active", "#3fb950")
    ]
    
    for label, val, color in stats:
        st.markdown(f"""
        <div class="metric-box">
            <p style='color:#8b949e; font-size:10px; font-weight:700; margin:0'>{label}</p>
            <p style='color:{color}; font-size:22px; font-weight:800; margin:0'>{val}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.get('run', False):
        report = generate_pdf(lat, lon)
        st.download_button("📥 DOWNLOAD REPORT", data=report, file_name="analysis.pdf", use_container_width=True)

    st.markdown("<div style='margin-top:50px; color:#484f58; font-size:10px; text-align:center'>CORE ENGINE v3.2.1</div>", unsafe_allow_html=True)
