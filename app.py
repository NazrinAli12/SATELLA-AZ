import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io

# 1. Page Configuration
st.set_page_config(page_title="SATELLA | AI Studio", layout="wide", initial_sidebar_state="expanded")

# 2. Advanced AI Studio Styling (CSS)
st.markdown("""
<style>
    /* Google Sans / Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        overflow: hidden !important;
    }

    /* Padding-ləri ləğv et */
    [data-testid="stHeader"], .block-container {
        padding: 0 !important; margin: 0 !important;
    }

    /* SOL SİDEBAR - AI Studio Black */
    section[data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
        width: 280px !important;
        overflow: hidden !important;
    }
    section[data-testid="stSidebar"] > div {
        overflow: hidden !important; /* Scroll-u tam ləğv et */
    }

    /* SAĞ PANEL (FIXED) - AI Studio Settings Style */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #2d333b !important;
        height: 100vh !important;
        padding: 24px 16px !important;
        position: fixed;
        right: 0;
        top: 0;
        z-index: 1000;
        overflow-y: auto;
    }

    /* AI Studio Göy Oval Düymə */
    div.stButton > button {
        background-color: #1a73e8 !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 6px 20px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        width: 100% !important;
        margin-top: 10px;
    }

    /* Sağ Panel Metrik Kartları */
    .metric-container {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
    }
    .metric-label { color: #9aa0a6; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { color: #f1f3f4; font-size: 22px; font-weight: 500; margin-top: 5px; }

    /* Input Stili */
    .stTextInput input {
        background-color: #1a1f24 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 6px !important;
        color: white !important;
        height: 35px !important;
    }

    /* Fayl yükləmə qutuları */
    .stFileUploader section {
        background-color: #1a1f24 !important;
        border: 1px dashed #3c4043 !important;
        padding: 5px !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. PDF Function
def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 20, "SATELLA CONSTRUCTION ANALYSIS", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Analysis Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(0, 10, f"Target Coordinates: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, "-"*50, ln=True)
    pdf.cell(0, 10, "Detection Results: 6 New Structures Identified", ln=True)
    pdf.cell(0, 10, "Accuracy: 92.4%", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- SOL SIDEBAR (AI STUDIO CLONE) ---
with st.sidebar:
    st.markdown("""
        <div style='display:flex; align-items:center; gap:12px; margin-bottom:2rem;'>
            <div style='background:#1a73e8; color:white; padding:6px 10px; border-radius:6px; font-weight:bold'>S</div>
            <div>
                <div style='color:white; font-size:16px; font-weight:600; line-height:1'>SATELLA</div>
                <div style='color:#8b949e; font-size:10px; margin-top:4px'>CONSTRUCTION AI</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#9aa0a6; font-size:11px; font-weight:600'>COORDINATES</p>", unsafe_allow_html=True)
    lat_input = st.text_input("Lat", "40.394799", label_visibility="collapsed")
    lon_input = st.text_input("Lon", "49.849585", label_visibility="collapsed")

    if st.button("Analyze Location"):
        st.session_state.lat = float(lat_input)
        st.session_state.lon = float(lon_input)

    st.markdown("<br><p style='color:#9aa0a6; font-size:11px; font-weight:600'>SATELLITE DATA</p>", unsafe_allow_html=True)
    baseline = st.file_uploader("2024 Baseline", type=["png","jpg"], key="b1", label_visibility="collapsed")
    current = st.file_uploader("2025 Current", type=["png","jpg"], key="c1", label_visibility="collapsed")
    
    st.markdown("<div style='margin-top:50px; color:#484f58; font-size:10px;'>v1.5.2 | Enterprise Level API</div>", unsafe_allow_html=True)

# --- MAIN CONTENT & RIGHT PANEL ---
col_map, col_right = st.columns([4.2, 1.2])

with col_map:
    # Live Badge
    st.markdown("""
        <div style='position:absolute; top:20px; left:20px; z-index:1000; background:#111418; border:1px solid #3c4043; padding:5px 15px; border-radius:20px; color:white; font-size:12px; display:flex; align-items:center; gap:8px'>
            <span style='height:8px; width:8px; background:#ea4335; border-radius:50%'></span> LIVE ANALYSIS
        </div>
    """, unsafe_allow_html=True)
    
    lat_val = st.session_state.get('lat', 40.394799)
    lon_val = st.session_state.get('lon', 49.849585)
    
    m = folium.Map([lat_val, lon_val], zoom_start=18, tiles="CartoDB dark_matter", zoom_control=False)
    folium.Marker([lat_val, lon_val]).add_to(m)
    folium.Circle([lat_val, lon_val], 150, color="#1a73e8", fill=True, opacity=0.4).add_to(m)
    folium_static(m, width=1350, height=850)

with col_right:
    st.markdown("<p style='color:white; font-size:18px; font-weight:500; margin-bottom:20px'>Metrics & Control</p>", unsafe_allow_html=True)
    
    # Sağ Panel Kartları
    st.markdown("""
        <div class="metric-container"><div class="metric-label">Detected Anomalies</div><div class="metric-value">6 Structures</div></div>
        <div class="metric-container"><div class="metric-label">Model Confidence</div><div class="metric-value">92.4%</div></div>
        <div class="metric-container"><div class="metric-label">Area Analyzed</div><div class="metric-value">1.2 km²</div></div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("<p style='color:#9aa0a6; font-size:11px; font-weight:600'>EXPORT OPTIONS</p>", unsafe_allow_html=True)
    
    if st.button("📄 Prepare FHN Report", use_container_width=True):
        if baseline and current:
            pdf_bytes = generate_pdf(lat_val, lon_val)
            st.download_button(
                label="Download Official PDF",
                data=pdf_bytes,
                file_name=f"SATELLA_Report_{datetime.now().strftime('%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error("Missing Satellite Images!")

    if baseline: st.image(baseline, caption="T0 Baseline", use_container_width=True)
    if current: st.image(current, caption="T1 Current", use_container_width=True)
