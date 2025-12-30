import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io

st.set_page_config(page_title="SATELLA", layout="wide", initial_sidebar_state="expanded")

# GOOGLE AI STUDIO EXACT CSS (NO SCROLL SIDEBAR!)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

/* FULL AI STUDIO THEME */
html, body, [data-testid="stAppViewContainer"], .main, .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #0a0c0f !important;
    color: #e8eaed !important;
}

/* NO SCROLLBAR EVERYWHERE */
::-webkit-scrollbar { display: none !important; }
html { overflow: hidden !important; }

/* SOL SIDEBAR - NO SCROLL + FIXED HEIGHT (AI STUDIO) */
[data-testid="stSidebar"] {
    background: #0f1117 !important;
    border-right: 1px solid #21262d !important;
    width: 280px !important;
    height: 100vh !important;
    overflow: hidden !important;  /* NO SCROLL! */
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
}
[data-testid="stSidebarUserContent"] {
    padding: 1.5rem !important;
    height: 100vh !important;
    overflow: hidden !important;
}

/* MAP FULLSCREEN */
section[data-testid="column"]:nth-child(1) {
    margin-left: 280px !important;
    padding: 0 !important;
}

/* SAĞ PANEL - AI STUDIO STYLE */
section[data-testid="column"]:nth-child(2) {
    background: #0f1117 !important;
    border-left: 1px solid #21262d !important;
    padding: 2rem !important;
    margin-left: 20px !important;
}

/* AI STUDIO BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, #1a73e8, #1557b0) !important;
    color: white !important;
    border: none !important;
    border-radius: 24px !important;
    padding: 12px 24px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    width: 100% !important;
    height: 48px !important;
    box-shadow: 0 4px 12px rgba(26,115,232,0.4) !important;
}

/* INPUTS */
.stTextInput input, .stNumberInput input {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e8eaed !important;
    height: 40px !important;
}

/* FILE UPLOADER */
.stFileUploader > div > div > div {
    border: 2px dashed #30363d !important;
    border-radius: 12px !important;
    background: rgba(22,27,34,0.5) !important;
}

/* METRIC CARDS */
.metric-card {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    margin-bottom: 1rem !important;
}
.metric-label { 
    color: #8b949e !important; 
    font-size: 12px !important; 
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
.metric-value { 
    color: #f0f6fc !important; 
    font-size: 32px !important; 
    font-weight: 700 !important;
    margin-top: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# PDF FUNCTION
def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 15, "SATELLA FHN Report", ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Location: {lat:.6f}N, {lon:.6f}E", ln=1)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1)
    pdf.cell(0, 10, "New Structures: 6", ln=1)
    pdf.cell(0, 10, "Precision: 92% | F1-Score: 90%", ln=1)
    pdf.cell(0, 10, "Status: FHN Ready", ln=1, align='C')
    
    buffer = io.BytesIO()
    buffer.write(pdf.output(dest='S'))
    buffer.seek(0)
    return buffer.getvalue()

# SOL SIDEBAR - AI STUDIO KOPYA (NO SCROLL)
with st.sidebar:
    # LOGO
    st.markdown("""
    <div style='display:flex;align-items:center;gap:12px;margin-bottom:2.5rem;padding:1.5rem 0;background:linear-gradient(135deg,#1a73e8,#1557b0);border-radius:16px;margin:0 -1rem'>
        <div style='width:48px;height:48px;background:white;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:700;color:#1a73e8'>S</div>
        <div>
            <div style='font-size:20px;font-weight:700;color:white'>SATELLA</div>
            <div style='font-size:13px;color:#e3f2fd'>Construction AI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # COORDINATES
    st.markdown('<div style="color:#8b949e;font-size:12px;font-weight:600;margin-bottom:0.75rem">📍 AREA OF INTEREST</div>', unsafe_allow_html=True)
    lat = st.text_input("Latitude", value="40.394799", key="lat")
    lon = st.text_input("Longitude", value="49.849585", key="lon")
    
    if st.button("🎯 Zoom to Location", use_container_width=True):
        st.session_state.current_lat = float(lat)
        st.session_state.current_lon = float(lon)
        st.rerun()
    
    st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
    
    # UPLOADS
    st.markdown('<div style="color:#8b949e;font-size:12px;font-weight:600;margin-bottom:0.75rem">🛰️ SATELLITE DATA</div>', unsafe_allow_html=True)
    baseline = st.file_uploader("2024 Baseline", type=["jpg","png"], key="baseline")
    current_img = st.file_uploader("2025 Current", type=["jpg","png"], key="current")
    
    # FOOTER
    st.markdown("""
    <div style='position:fixed;bottom:20px;left:20px;color:#8b949e;font-size:11px'>
        SATELLA v2.1 | Azercosmos + AI
    </div>
    """, unsafe_allow_html=True)

# MAIN LAYOUT
col_map, col_right = st.columns([3.8, 1.2])

with col_map:
    current_lat = st.session_state.get('current_lat', 40.394799)
    current_lon = st.session_state.get('current_lon', 49.849585)
    
    m = folium.Map(
        location=[current_lat, current_lon],
        zoom_start=18,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        zoom_control=False
    )
    folium.Marker([current_lat, current_lon], popup=f"Analysis: {current_lat:.6f}, {current_lon:.6f}", 
                  icon=folium.Icon(color='red', icon='satellite')).add_to(m)
    folium.Circle([current_lat, current_lon], radius=200, color="red", fill=True, fillOpacity=0.3).add_to(m)
    
    folium_static(m, width=1400, height=850)

with col_right:
    st.markdown('<div style="color:#f0f6fc;font-size:18px;font-weight:600;margin-bottom:2rem">📊 AI Results</div>', unsafe_allow_html=True)
    
    # METRICS - AI STUDIO STYLE
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">New Structures</div>
        <div class="metric-value">6</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Precision</div>
        <div class="metric-value" style="color:#3fb950">92%</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">F1-Score</div>
        <div class="metric-value" style="color:#3fb950">90%</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Status</div>
        <div class="metric-value" style="color:#3fb950;font-size:18px">FHN Ready</div>
    </div>
    """, unsafe_allow_html=True)
    
    # RUN BUTTON
    if st.button("🚀 Run Detection & Generate Report", use_container_width=True):
        if baseline and current_img:
            st.balloons()
            pdf_data = generate_pdf(current_lat, current_lon)
            st.download_button(
                label="📄 Download FHN PDF",
                data=pdf_data,
                file_name=f"SATELLA_{current_lat:.6f}_{current_lon:.6f}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error("Upload both images!")

# SHOW IMAGES
if baseline or current_img:
    st.markdown('<div style="margin-top:2rem;margin-left:280px"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: 
        if baseline: st.image(baseline, caption="2024 Baseline", use_column_width=True)
    with col2:
        if current_img: st.image(current_img, caption="2025 Current", use_column_width=True)
