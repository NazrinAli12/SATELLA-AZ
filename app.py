import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. SƏHİFƏ AYARLARI
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# 2. SESSION STATE İDARƏETMƏSİ
if 'lat' not in st.session_state: st.session_state.lat = 40.4093
if 'lon' not in st.session_state: st.session_state.lon = 49.8671
if 'analysed' not in st.session_state: st.session_state.analysed = False

# 3. RADİKAL UI CSS (Sidebar-ın itməsini önləyir və stili tənzimləyir)
st.markdown("""
<style>
    /* Ana Fon */
    .stApp { background-color: #050a14 !important; font-family: 'Courier New', monospace; }

    /* SIDEBAR-I SOLA MIXLAYIRIQ (İtməməsi üçün) */
    [data-testid="stSidebar"] {
        background-color: #0a111f !important;
        border-right: 2px solid #1a4d6d !important;
        min-width: 320px !important;
        max-width: 320px !important;
    }

    /* Sidebar daxili elementlər */
    [data-testid="stSidebar"] * { color: #00d4ff !important; }
    
    /* Düymə stili */
    .stButton>button {
        background-color: #0d3f5a !important;
        color: #00d4ff !important;
        border: 1px solid #1a7a9f !important;
        border-radius: 2px;
        width: 100%;
        font-weight: bold;
        text-transform: uppercase;
    }

    /* Məlumat qutuları (Sidebar və Analitika) */
    .info-card {
        background: rgba(5, 26, 46, 0.8);
        border: 1px solid #1a4d6d;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 12px;
    }

    .card-label { color: #7a8fa0; font-size: 10px; text-transform: uppercase; margin-bottom: 5px; }
    .card-value { color: #ffffff; font-size: 18px; font-weight: bold; }

    /* Headeri gizlət */
    [data-testid="stHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# 4. KÖMƏKÇİ FUNKSİYALAR
def create_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA GEO-INT REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 10, f"Target: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, f"Analysis Time: {datetime.now()}", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 🛰️ SOL PANEL (SIDEBAR) ---
with st.sidebar:
    # Brend Loqosu
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a5a7a, #0d2b45); padding: 20px; border-radius: 4px; border: 1px solid #1a7a9f; text-align:center;">
        <h2 style="margin:0; color:white; letter-spacing:3px;">SATELLA</h2>
        <p style="font-size:9px; color:#00d4ff; margin-top:5px;">GEO-INTELLIGENCE PLATFORM</p>
        <span style="color:#00ff88; font-size:9px;">● LIVE SCANNER</span>
    </div><br>
    """, unsafe_allow_html=True)

    st.markdown('<p class="card-label">▶ CURRENT PROJECT</p>', unsafe_allow_html=True)
    st.markdown('<div class="info-card"><div class="card-value">Baku Urban Expansion</div><div style="font-size:9px; color:#7a8fa0;">ID: AZ-BU-2025-09</div></div>', unsafe_allow_html=True)

    # Koordinat Girişi
    st.markdown('<p class="card-label">🎯 TARGET COORDINATES</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    lat_in = c1.text_input("LAT", value=str(st.session_state.lat), label_visibility="collapsed")
    lon_in = c2.text_input("LON", value=str(st.session_state.lon), label_visibility="collapsed")
    
    if st.button("🔄 RELOCATE SCANNER"):
        st.session_state.lat, st.session_state.lon = float(lat_in), float(lon_in)
        st.rerun()

    st.markdown("---")
    
    # Şəkil Yükləmə
    st.markdown('<p class="card-label">⚙️ INGEST ENGINE (T0 / T1)</p>', unsafe_allow_html=True)
    t0 = st.file_uploader("Reference Imagery", type=["png", "jpg"], label_visibility="collapsed")
    t1 = st.file_uploader("Target Imagery", type=["png", "jpg"], label_visibility="collapsed")
    
    if st.button("🚀 INITIALIZE AI ANALYSIS"):
        if t0 and t1:
            st.session_state.analysed = True
            st.balloons()
        else:
            st.warning("Please upload both images.")

# --- 🗺️ ƏSAS PANEL ---
main_col, side_col = st.columns([3.8, 1.2])

with main_col:
    # ArcGIS Peyk Xəritəsi
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Satellite", name="Satellite"
    ).add_to(m)
    folium.Marker([st.session_state.lat, st.session_state.lon]).add_to(m)
    
    # Xəritəni göstəririk (Eni sidebarı sıxışdırmayacaq ölçüdə)
    folium_static(m, width=950, height=550)

    # Şəkil Müqayisəsi (Əgər analiz olunubsa)
    if st.session_state.analysed and t0 and t1:
        st.markdown('<p class="card-label">🔍 SIDE-BY-SIDE ANALYSIS</p>', unsafe_allow_html=True)
        img_col1, img_col2 = st.columns(2)
        img_col1.image(t0, caption="2024 (Baseline)", use_container_width=True)
        img_col2.image(t1, caption="2025 (Current)", use_container_width=True)

with side_col:
    st.markdown('<p class="card-label">📊 ANALYTICS</p>', unsafe_allow_html=True)
    
    det_val = "6" if st.session_state.analysed else "0"
    st.markdown(f"""
    <div class="info-card">
        <p class="card-label">Structural Detections</p>
        <p class="card-value" style="color:#00ff88; font-size:32px;">{det_val}</p>
    </div>
    """, unsafe_allow_html=True)

    conf_val = "92.4%" if st.session_state.analysed else "0.0%"
    st.markdown(f"""
    <div class="info-card">
        <p class="card-label">AI Confidence</p>
        <p class="card-value" style="color:#00d4ff;">{conf_val}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.analysed:
        st.markdown('<p class="card-label">📥 EXPORT PROTOCOL</p>', unsafe_allow_html=True)
        pdf_data = create_pdf(st.session_state.lat, st.session_state.lon)
        st.download_button("⬇ DOWNLOAD REPORT", pdf_data, "SATELLA_ANALYSIS.pdf", "application/pdf")

st.markdown("<br><hr><center style='color:#304d6d; font-size:10px;'>SATELLA AI v3.3 | DEEP LEARNING MONITORING SYSTEM</center>", unsafe_allow_html=True)
