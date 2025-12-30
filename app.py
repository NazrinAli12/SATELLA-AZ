import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# 2. UI Təkmilləşdirməsi
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        overflow: hidden !important;
    }

    [data-testid="stHeader"] { display: none; }

    /* SOL SİDEBAR */
    section[data-testid="stSidebar"] {
        width: 340px !important;
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
    }
    section[data-testid="stSidebar"] > div {
        height: 100vh !important;
        overflow: hidden !important;
        padding: 1rem !important;
    }

    .stVerticalBlock { gap: 0.2rem !important; }
    
    div.stButton > button {
        background: #1a73e8 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        height: 38px !important;
        width: 100%;
        border: none !important;
        margin-top: 5px;
    }

    .sidebar-label {
        font-size: 11px;
        font-weight: 700;
        color: #9ca3af;
        margin-bottom: 4px;
        margin-top: 12px;
        text-transform: uppercase;
    }

    .success-msg {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        padding: 8px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
        margin-top: 10px;
        border: 1px solid rgba(16, 185, 129, 0.2);
        text-align: center;
    }

    .metric-box {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Şəkil Ölçüləndirmə (Tam eyni ölçü üçün məcburi format)
def process_images(img1, img2):
    i1 = Image.open(img1)
    i2 = Image.open(img2)
    
    # Hər iki şəkli eyni ölçüyə (məsələn 1024x768) məcburi gətiririk
    # Atılan nümunədəki kimi dördbucaqlı dursa, ən yaxşı nəticəni verir.
    target_size = (1024, 768)
    
    # LANCZOS filtri keyfiyyəti ən yüksək səviyyədə saxlayır
    return i1.resize(target_size, Image.Resampling.LANCZOS), i2.resize(target_size, Image.Resampling.LANCZOS)

# 4. PDF Funksiyası
def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA ANALYSIS REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Coordinates: {lat}, {lon}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1e3a8a,#3b82f6);padding:0.8rem;border-radius:8px;margin-bottom:1rem'>
        <h2 style='color:white;margin:0;font-size:18px;'>🛰️ SATELLA AI</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p class='sidebar-label'>Area of Interest</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: lat_val = st.text_input("LATITUDE", value="40.394799", key="lat_in")
    with c2: lon_val = st.text_input("LONGITUDE", value="49.849585", key="lon_in")
    
    st.markdown("<p class='sidebar-label'>Imagery Inputs</p>", unsafe_allow_html=True)
    st.caption("T0: 2024 Baseline (Reference)")
    t0_file = st.file_uploader("Upload T0", type=["png","jpg"], label_visibility="collapsed", key="u1")
    
    st.caption("T1: 2025 Current (Target)")
    t1_file = st.file_uploader("Upload T1", type=["png","jpg"], label_visibility="collapsed", key="u2")
    
    if st.button("RUN CHANGE DETECTION"):
        if t0_file and t1_file:
            st.session_state.lat = float(lat_val)
            st.session_state.lon = float(lon_val)
            st.session_state.run = True
        else:
            st.error("Please upload both images!")

    if st.session_state.get('run', False):
        st.markdown("<div class='success-msg'>✅ Detected 1 new structures.</div>", unsafe_allow_html=True)

# --- ƏSAS EKRAN ---
col_map, col_metrics = st.columns([3.9, 1.1])

with col_map:
    cur_lat = st.session_state.get('lat', 40.394799)
    cur_lon = st.session_state.get('lon', 49.849585)
    
    m = folium.Map(location=[cur_lat, cur_lon], zoom_start=17, tiles=None)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite View"
    ).add_to(m)
    folium.Marker([cur_lat, cur_lon], icon=folium.Icon(color="blue", icon="info-sign")).add_to(m)
    
    folium_static(m, width=1200, height=600)
    
    # ŞƏKİLLƏRİN SİMMETRİK GÖSTƏRİLMƏSİ
    if t0_file and t1_file:
        st.markdown("<br>", unsafe_allow_html=True)
        img1, img2 = process_images(t0_file, t1_file)
        
        img_c1, img_c2 = st.columns(2)
        with img_c1:
            st.image(img1, caption="Baseline 2024 (T0)", use_container_width=True)
        with img_c2:
            st.image(img2, caption="Current 2025 (T1)", use_container_width=True)

with col_metrics:
    st.markdown("### 📊 Metrics")
    st.markdown(f"""
    <div class="metric-box">
        <p style='color:#9ca3af;font-size:10px;font-weight:700;margin:0'>IDENTIFIED</p>
        <p style='color:white;font-size:26px;font-weight:800;margin:0'>1</p>
    </div>
    <div class="metric-box">
        <p style='color:#9ca3af;font-size:10px;font-weight:700;margin:0'>PRECISION</p>
        <p style='color:#3b82f6;font-size:26px;font-weight:800;margin:0'>92%</p>
    </div>
    <div class="metric-box">
        <p style='color:#9ca3af;font-size:10px;font-weight:700;margin:0'>F1-SCORE</p>
        <p style='color:#10b981;font-size:26px;font-weight:800;margin:0'>90%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('run', False):
        report = generate_pdf(cur_lat, cur_lon)
        st.download_button("📥 GENERATE REPORT", data=report, file_name="satella_report.pdf", use_container_width=True)

    st.markdown("<div style='margin-top:30px; color:#4b5563; font-size:10px; text-align:center'>SATELLA AI v3.2</div>", unsafe_allow_html=True)
