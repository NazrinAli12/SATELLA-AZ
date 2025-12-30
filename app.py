import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. Səhifə Ayarları
st.set_page_config(page_title="Google AI Studio - Satella", layout="wide", initial_sidebar_state="expanded")

# 2. Google AI Studio Sol Panel Vizualı (CSS)
st.markdown("""
    <style>
    /* Ümumi tünd fon */
    .main { background-color: #0b0d0f !important; }
    
    /* Sol Sidebar - Tam AI Studio tərzi */
    [data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid #1e2227 !important;
        width: 300px !important;
    }

    /* Sidebar Logo və Başlıq */
    .sb-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0px 20px 0px;
    }
    .sb-logo {
        background: #2463eb;
        color: white;
        padding: 6px 10px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 16px;
    }
    .sb-title {
        color: #e8eaed;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* Bölmə Başlıqları (Göy-boz kiçik hərflər) */
    .sb-label {
        color: #8b949e;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 12px;
        margin-top: 25px;
        letter-spacing: 0.8px;
    }

    /* Input Sahələri */
    .stTextInput input {
        background-color: #1a1f26 !important;
        border: 1px solid #2d333b !important;
        color: #c9d1d9 !important;
        border-radius: 8px !important;
        height: 40px !important;
    }

    /* Göy Düymə (Zoom to Coordinate) */
    div.stButton > button:first-child {
        background-color: #2463eb !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important; /* Oval düymə */
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 8px 20px !important;
        width: 100% !important;
        transition: background 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #1d4ed8 !important;
    }

    /* Raster Data Qutuları (Dotted Border) */
    .upload-box-custom {
        border: 1px dashed #30363d;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        background: transparent;
        margin-bottom: 8px;
    }
    .upload-icon {
        color: #8b949e;
        font-size: 18px;
        margin-bottom: 5px;
    }
    .upload-text {
        color: #8b949e;
        font-size: 12px;
    }

    /* Alt qeyd (Footer in Sidebar) */
    .sb-footer {
        position: fixed;
        bottom: 20px;
        font-size: 10px;
        color: #484f58;
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)

# PDF funksiyası (dəyişilmədi)
def generate_pdf_report(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Analysis: {lat}, {lon}", ln=True)
    return bytes(pdf.output())

# --- SOL SIDEBAR (AI STUDIO CLONE) ---
with st.sidebar:
    # Logo hissəsi
    st.markdown('''
        <div class="sb-brand">
            <div class="sb-logo">🛰️</div>
            <div>
                <div class="sb-title">SATELLA</div>
                <div style="font-size: 9px; color: #8b949e;">CONSTRUCTION MONITORING</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Area of Interest
    st.markdown('<p class="sb-label">🔍 Area of Interest</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: lat_input = st.text_input("Lat", "40.4093", label_visibility="collapsed")
    with c2: lon_input = st.text_input("Lon", "49.8671", label_visibility="collapsed")
    
    if st.button("Zoom to Coordinate"):
        st.session_state.lat, st.session_state.lon = lat_input, lon_input

    # Raster Data Section
    st.markdown('<p class="sb-label">📁 Raster Data</p>', unsafe_allow_html=True)
    
    # Baseline T0
    st.markdown('<div class="upload-box-custom"><div class="upload-icon">📄</div><div class="upload-text">Baseline (T0).tif</div></div>', unsafe_allow_html=True)
    st.file_uploader("T0", label_visibility="collapsed", key="f1")
    
    # Current T1
    st.markdown('<div class="upload-box-custom"><div class="upload-icon">📄</div><div class="upload-text">Current (T1).tif</div></div>', unsafe_allow_html=True)
    st.file_uploader("Current (T1)", label_visibility="collapsed", key="f2")
    
    # Run düyməsi (Aktiv olmayan halda)
    st.button("Run Change Detection", disabled=True)

    # Sidebar Footer
    st.markdown('''
        <div class="sb-footer">
            SATELLA v1.0 | Sentinel-2 & Azercosmos<br>
            Integration. Developed for FHN Construction<br>
            Safety Standards.
        </div>
    ''', unsafe_allow_html=True)

# --- SAĞ VƏ MƏRKƏZ HİSSƏ (Eyni qaldı) ---
col_map, col_metrics = st.columns([3.6, 1.2], gap="small")

with col_map:
    st.markdown('<div style="background:#1a1f26; border:1px solid #2d333b; color:white; padding:6px 12px; border-radius:6px; font-size:11px; font-weight:700; display:inline-flex; align-items:center; margin-bottom:15px;"><span style="height:8px; width:8px; background:#f85149; border-radius:50%; margin-right:8px;"></span> LIVE MONITORING</div>', unsafe_allow_html=True)
    c_lat = float(st.session_state.get('lat', 40.4093))
    c_lon = float(st.session_state.get('lon', 49.8671))
    m = folium.Map(location=[c_lat, c_lon], zoom_start=15, tiles="OpenStreetMap")
    folium_static(m, width=1000, height=750)

with col_metrics:
    st.markdown('<h3 style="color:white; font-size:18px;">📊 System Metrics</h3>', unsafe_allow_html=True)
    # Metriklər və PDF düyməsi bura gəlir (əvvəlki kimi)
    pdf_data = generate_pdf_report(c_lat, c_lon)
    st.download_button("📄 Generate FHN Report (PDF)", data=pdf_data, file_name="report.pdf", mime="application/pdf", use_container_width=True)
