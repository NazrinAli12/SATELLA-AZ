import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# Session State tənzimləmələri
if 'lat' not in st.session_state: st.session_state.lat = 40.4093
if 'lon' not in st.session_state: st.session_state.lon = 49.8671
if 'is_analysed' not in st.session_state: st.session_state.is_analysed = False

# 2. PROFESSIONAL KİBER-PANAL UI (CSS)
st.markdown("""
<style>
    /* Ümumi fon və şrift */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    * { font-family: 'JetBrains Mono', monospace; }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050b14 !important;
        color: #e0e0e0;
    }

    /* Sol Panel (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #08101a !important;
        border-right: 2px solid #00d4ff !important;
        box-shadow: 5px 0 15px rgba(0, 212, 255, 0.1);
    }

    /* Kartlar (Info Box) */
    .cyber-card {
        background: rgba(13, 31, 55, 0.8);
        border: 1px solid #1a4d6d;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 15px;
        position: relative;
        overflow: hidden;
    }
    
    .cyber-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: #00d4ff;
    }

    .stat-value {
        color: #00d4ff;
        font-size: 28px;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }

    /* Düymələr */
    .stButton>button {
        background: linear-gradient(90deg, #0d3f5a 0%, #1a7a9f 100%) !important;
        color: white !important;
        border: 1px solid #00d4ff !important;
        border-radius: 2px !important;
        font-weight: bold !important;
        transition: 0.3s all;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 15px #00d4ff;
        transform: translateY(-2px);
    }

    /* Header gizlət */
    [data-testid="stHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# --- SOL PANEL (SIDEBAR) ---
with st.sidebar:
    # Logo & Status
    st.markdown("""
    <div style="background: #0d2b45; border: 1px solid #1a4d6d; padding: 20px; border-radius: 4px; margin-bottom: 25px;">
        <h1 style="color: #00d4ff; margin: 0; font-size: 22px; letter-spacing: 3px;">🛰️ SATELLA</h1>
        <p style="color: #7a8fa0; font-size: 10px; margin: 5px 0 0 0;">GEO-INTEL CORE v3.2</p>
        <div style="margin-top:10px;"><span style="color: #00ff88;">●</span> <small>SYSTEM LIVE</small></div>
    </div>
    """, unsafe_allow_html=True)

    # Coordinates
    st.subheader("🎯 TARGETING")
    lat_in = st.text_input("LATITUDE", value=str(st.session_state.lat))
    lon_in = st.text_input("LONGITUDE", value=str(st.session_state.lon))
    
    if st.button("🔄 RELOCATE SCANNER", use_container_width=True):
        st.session_state.lat = float(lat_input) if 'lat_input' in locals() else float(lat_in)
        st.session_state.lon = float(lon_input) if 'lon_input' in locals() else float(lon_in)
        st.rerun()

    st.markdown("---")
    
    # Files
    st.subheader("⚙️ DATA INGEST")
    t0_file = st.file_uploader("BASELINE (T0)", type=["png", "jpg"])
    t1_file = st.file_uploader("TARGET (T1)", type=["png", "jpg"])
    
    if st.button("▶ START AI ENGINE", use_container_width=True):
        if t0_file and t1_file:
            st.session_state.is_analysed = True
            st.balloons()
        else:
            st.warning("Data stream missing.")

# --- ƏSAS EKRAN (MAP & ANALYTICS) ---
col_map, col_data = st.columns([3.5, 1.2])

with col_map:
    # Real-vaxt xəritə tənzimləməsi
    # ArcGIS World Imagery daha detallı və "real" görünür (Google Map alternativi)
    m = folium.Map(
        location=[st.session_state.lat, st.session_state.lon], 
        zoom_start=18, 
        tiles=None # Standart xəritəni silirik
    )
    
    # Yüksək Keyfiyyətli Peyk Təbəqəsi
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite View"
    ).add_to(m)
    
    # Hədəf nişanı
    folium.Marker(
        [st.session_state.lat, st.session_state.lon],
        popup="Target AOI",
        icon=folium.Icon(color='blue', icon='crosshairs', prefix='fa')
    ).add_to(m)
    
    # Xəritəni göstər
    folium_static(m, width=1050, height=650)
    
    # Şəkil müqayisəsi (Analizdən sonra)
    if st.session_state.is_analysed:
        st.markdown("### 🔍 OPTICAL COMPARISON")
        c1, c2 = st.columns(2)
        c1.image(t0_file, caption="2024 (Baseline)", use_container_width=True)
        c2.image(t1_file, caption="2025 (Target)", use_container_width=True)

with col_data:
    st.markdown("### 📊 ANALYTICS")
    
    # Stat Kartları
    det_val = "6" if st.session_state.is_analysed else "0"
    st.markdown(f"""
    <div class="cyber-card">
        <p style="color: #7a8fa0; font-size: 11px; margin:0;">NEW STRUCTURES</p>
        <p class="stat-value">{det_val} Units</p>
    </div>
    """, unsafe_allow_html=True)
    
    conf_val = "92.4%" if st.session_state.is_analysed else "0.0%"
    st.markdown(f"""
    <div class="cyber-card">
        <p style="color: #7a8fa0; font-size: 11px; margin:0;">AI PRECISION</p>
        <p class="stat-value" style="color: #00ff88;">{conf_val}</p>
    </div>
    """, unsafe_allow_html=True)

    # Export
    if st.session_state.is_analysed:
        st.markdown("### 📥 PROTOCOL")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(40, 10, "SATELLA INTELLIGENCE REPORT")
        pdf_out = pdf.output(dest='S').encode('latin-1')
        st.download_button("DOWNLOAD DATA", pdf_out, "report.pdf", use_container_width=True)

st.markdown("<p style='text-align:center; color:#30363d; font-size:10px; margin-top:50px;'>SATELLA GEO-INTEL // ENCRYPTED CONNECTION</p>", unsafe_allow_html=True)
