import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
import io
from fpdf import FPDF

# Sehife konfiqurasiyası
st.set_page_config(page_title="SATELLA - AI Monitoring", layout="wide", initial_sidebar_state="expanded")

# --- AI STUDIO GÖRÜNÜSÜ ÜCÜN CSS ---
st.markdown("""
    <style>
    /* Arxa fon və ana rənglər */
    .main { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    
    /* Metrik Kartları */
    .metric-card {
        background-color: #1c2128;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #30363d;
        margin-bottom: 10px;
    }
    
    /* Status rəngləri */
    .status-ready { color: #2ea043; font-weight: bold; }
    
    /* Düymə stilləri */
    .stButton>button {
        border-radius: 6px;
        font-weight: 500;
    }
    
    /* Başlıqları AI Studio tərzinə salmaq */
    h1, h2, h3 { color: #f0f6fc !important; font-family: 'Inter', sans-serif; }
    p, span { font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- PDF YARATMA FUNKSİYASI (Sənin orijinal kodun) ---
def create_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 22)
    pdf.cell(0, 15, "SATELLA FHN Report", ln=1, align="C")
    pdf.ln(8)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Location Coordinates", ln=1)
    pdf.set_font("Arial", '', 14)
    pdf.cell(0, 10, f"{lat} N, {lon} E", ln=1)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Detection Results", ln=1)
    pdf.set_font("Arial", '', 14)
    pdf.cell(0, 10, "New Structures Detected: 6", ln=1)
    pdf.cell(0, 10, "Precision: 92%", ln=1)
    pdf.cell(0, 10, "Area Analyzed: 0.9 km2", ln=1)
    
    buffer = io.BytesIO()
    buffer.write(pdf.output(dest='S').encode('latin-1'))
    buffer.seek(0)
    return buffer.getvalue()

# --- SOL PANEL (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 🛰️ SATELLA")
    st.caption("CONSTRUCTION MONITORING")
    st.markdown("---")
    
    st.subheader("🔍 AREA OF INTEREST")
    lat_input = st.text_input("Latitude", value="40.394799")
    lon_input = st.text_input("Longitude", value="49.849585")
    
    if st.button("Zoom to Coordinate", use_container_width=True):
        st.session_state.lat = lat_input
        st.session_state.lon = lon_input
    
    st.markdown("---")
    st.subheader("📁 RASTER DATA")
    baseline = st.file_uploader("Baseline (2024).tif", type=["jpg", "png", "tif"])
    current = st.file_uploader("Current (2025).tif", type=["jpg", "png", "tif"])
    
    st.markdown("##")
    run_detection = st.button("🚀 Run Detection", type="primary", use_container_width=True)

# --- ESAS EKRAN (MAP VE SYSTEM METRICS) ---
col_left, col_right = st.columns([3, 1])

with col_left:
    st.markdown("🔴 **LIVE MONITORING**")
    
    # Koordinatları session_state-dən oxu
    curr_lat = float(st.session_state.get('lat', lat_input))
    curr_lon = float(st.session_state.get('lon', lon_input))
    
    # Xerite (Dark Mode stilinde)
    m = folium.Map(location=[curr_lat, curr_lon], zoom_start=16, tiles="CartoDB dark_matter")
    folium.Marker([curr_lat, curr_lon], popup="Target area").add_to(m)
    folium.Circle([curr_lat, curr_lon], radius=200, color="red", fill=True, fillOpacity=0.2).add_to(m)
    
    folium_static(m, width=900, height=550)
    
    # Sekil önizlemeleri (Xeritenin altında seliqeli sekilde)
    if baseline or current:
        prev_col1, prev_col2 = st.columns(2)
        with prev_col1:
            if baseline: st.image(baseline, caption="2024 Baseline", use_container_width=True)
        with prev_col2:
            if current: st.image(current, caption="2025 Current", use_container_width=True)

with col_right:
    st.markdown("### 📊 System Metrics")
    
    # Metrikler (AI Studio-dakı kimi kartlar)
    st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between;">
                <div><small style="color:gray;">NEW STRUCTURES</small><h2 style="margin:0;">6</h2></div>
                <div style="text-align:right;"><small style="color:gray;">STATUS</small><br><span class="status-ready">● Ready</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Progress Bar-lar
    st.write("PRECISION (IOU)")
    st.progress(0.92)
    st.write("RECALL RATE")
    st.progress(0.88)
    st.write("F1 PERFORMANCE")
    st.progress(0.90)
    
    st.markdown("---")
    st.warning("⚠️ **Verification Required**: Changes detected in sensitive zones. Generated reports must be submitted to FHN.")
    
    # PDF Duymesi
    report_pdf = create_pdf(curr_lat, curr_lon)
    st.download_button(
        label="📄 Generate FHN Report (PDF)",
        data=report_pdf,
        file_name=f"SATELLA_FHN_{datetime.now().strftime('%Y%md')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# Detection animasiyası
if run_detection:
    if baseline and current:
        st.balloons()
        st.sidebar.success("✅ Analysis Complete!")
    else:
        st.sidebar.error("⚠️ Please upload both images!")
