import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. Page Configuration
st.set_page_config(page_title="SATELLA - AI Studio", layout="wide")

# 2. AI Studio Mirror CSS
st.markdown("""
    <style>
    /* Ana Fon */
    .main { background-color: #0d1117 !important; }
    
    /* Sidebar Ümumi Stil */
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d !important;
        width: 320px !important;
    }

    /* Logo və Başlıq Sahəsi */
    .sb-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 5px 0px 25px 0px;
    }
    .sb-icon {
        background-color: #2f81f7;
        color: white;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 8px;
        font-weight: bold;
    }
    .sb-brand-name {
        color: #f0f6fc;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.5px;
        line-height: 1.2;
    }
    .sb-brand-sub {
        color: #8b949e;
        font-size: 10px;
        text-transform: uppercase;
    }

    /* Bölmə Başlıqları */
    .sb-section-title {
        color: #8b949e;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        margin: 20px 0 10px 0;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Input və Düymələr */
    .stTextInput input {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        color: #c9d1d9 !important;
        border-radius: 6px !important;
    }
    
    /* GÖY OVAL DÜYMƏ (AI STUDIO TƏRZİ) */
    div.stButton > button:first-child {
        background-color: #2f81f7 !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important; /* Oval */
        font-size: 13px !important;
        font-weight: 600 !important;
        width: 100% !important;
        padding: 6px 0px !important;
        margin-top: 10px;
    }

    /* Raster Data Qutuları (Dotted/Dashed) */
    .raster-box {
        border: 1px dashed #30363d;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
        background: transparent;
    }
    .raster-label {
        color: #8b949e;
        font-size: 12px;
        margin-top: 5px;
    }

    /* RUN Düyməsi (Daha tünd/sönük) */
    div.stButton > button[disabled] {
        background-color: #21262d !important;
        color: #484f58 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }

    /* Footer Text */
    .sb-footer-text {
        font-size: 10px;
        color: #484f58;
        border-top: 1px solid #21262d;
        padding-top: 15px;
        margin-top: 50px;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sol Panel Struktur (Sidebar)
with st.sidebar:
    # Üst Logo Hissəsi
    st.markdown('''
        <div class="sb-header">
            <div class="sb-icon">🛰️</div>
            <div>
                <div class="sb-brand-name">SATELLA</div>
                <div class="sb-brand-sub">CONSTRUCTION MONITORING</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Area of Interest
    st.markdown('<div class="sb-section-title">🔍 AREA OF INTEREST</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: lat_val = st.text_input("Lat", "40.4093", label_visibility="collapsed")
    with c2: lon_val = st.text_input("Lon", "49.8671", label_visibility="collapsed")
    
    if st.button("Zoom to Coordinate"):
        st.session_state.lat, st.session_state.lon = lat_val, lon_val

    # Raster Data
    st.markdown('<div class="sb-section-title">📤 RASTER DATA</div>', unsafe_allow_html=True)
    
    # Baseline T0 Box
    st.markdown('<div class="raster-box"><div style="color:#8b949e;">📄</div><div class="raster-label">Baseline (T0).tif</div></div>', unsafe_allow_html=True)
    st.file_uploader("T0", label_visibility="collapsed", key="file1")
    
    # Current T1 Box
    st.markdown('<div class="raster-box"><div style="color:#8b949e;">📄</div><div class="raster-label">Current (T1).tif</div></div>', unsafe_allow_html=True)
    st.file_uploader("T1", label_visibility="collapsed", key="file2")
    
    st.button("Run Change Detection", disabled=True)

    # Sidebar Footer
    st.markdown('''
        <div class="sb-footer-text">
            SATELLA v1.0 | Sentinel-2 & Azercosmos Integration.<br>
            Developed for FHN Construction Safety Standards.
        </div>
    ''', unsafe_allow_html=True)

# 4. Mərkəz və Sağ Panel (Funsionallıq qorundu)
col_map, col_right = st.columns([3.8, 1.2], gap="small")

with col_map:
    st.markdown('<div style="background:#161b22; border:1px solid #30363d; color:white; padding:6px 12px; border-radius:20px; font-size:11px; font-weight:700; display:inline-flex; align-items:center; margin-bottom:15px;"><span style="height:8px; width:8px; background:#f85149; border-radius:50%; margin-right:8px;"></span> LIVE MONITORING</div>', unsafe_allow_html=True)
    
    current_lat = float(st.session_state.get('lat', 40.4093))
    current_lon = float(st.session_state.get('lon', 49.8671))
    
    m = folium.Map(location=[current_lat, current_lon], zoom_start=15, tiles="OpenStreetMap")
    folium_static(m, width=1100, height=800)

with col_right:
    st.markdown('<h3 style="color:#f0f6fc; font-size:18px;">📊 System Metrics</h3>', unsafe_allow_html=True)
    # Metriklər və digər elementlər bura (əvvəlki kimi stabil qalır)
    st.info("Metrics ready for display.")
    
    # PDF Düyməsi funksionallığı
    def get_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="SATELLA Report", ln=True)
        return bytes(pdf.output())

    st.download_button("📄 Generate FHN Report (PDF)", data=get_pdf(), file_name="fhn_report.pdf", use_container_width=True)
