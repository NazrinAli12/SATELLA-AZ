import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io

st.set_page_config(page_title="SATELLA", layout="wide", initial_sidebar_state="expanded")

# SCROLL YOK CSS
st.markdown("""
<style>
[data-testid="stSidebar"] {
    overflow: hidden !important;
    height: 100vh !important;
    max-height: 100vh !important;
}
[data-testid="stSidebarUserContent"] {
    overflow: hidden !important;
    height: 100vh !important;
    max-height: 100vh !important;
    padding-bottom: 100px !important;
}
::-webkit-scrollbar { display: none !important; }
</style>
""", unsafe_allow_html=True)

def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA Report", ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Lat: {lat:.6f} Lon: {lon:.6f}", ln=1)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=1)
    pdf.cell(0, 10, "Structures: 6 | Precision: 92%", ln=1)
    buffer = io.BytesIO()
    buffer.write(pdf.output(dest='S'))
    buffer.seek(0)
    return buffer.getvalue()

with st.sidebar:
    st.markdown("### 🛰️ SATELLA")
    lat = st.text_input("Lat", "40.394799")
    lon = st.text_input("Lon", "49.849585")
    
    if st.button("Zoom"):
        st.session_state.lat = float(lat)
        st.session_state.lon = float(lon)
        st.rerun()
    
    baseline = st.file_uploader("2024", key="base")
    current = st.file_uploader("2025", key="curr")

col1, col2 = st.columns([4,1])

with col1:
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    m = folium.Map([lat, lon], zoom_start=18)
    folium.Marker([lat, lon]).add_to(m)
    folium_static(m, width=1200, height=700)

with col2:
    st.metric("Structures", 6)
    st.metric("Precision", "92%")
    
    if st.button("Generate PDF"):
        if baseline and current:
            pdf = generate_pdf(lat, lon)
            st.download_button("PDF", pdf, "report.pdf")
        else:
            st.error("Upload both!")

if baseline: st.image(baseline)
if current: st.image(current)
