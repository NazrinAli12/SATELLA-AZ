import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
import io
from fpdf import FPDF

# Səhifə konfiqurasiyası - AI Studio kimi geniş ekran
st.set_page_config(page_title="SATELLA - Construction Monitoring", layout="wide", initial_sidebar_state="expanded")

# --- AI STUDIO EXACT DESIGN (CSS) ---
st.markdown("""
    <style>
    /* Ana fon rəngi */
    .main { background-color: #0d1117; color: #c9d1d9; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    
    /* Başlıqlar */
    h1, h2, h3 { color: #f0f6fc !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
    
    /* Yan panel başlıqları */
    .sidebar-header { color: #8b949e; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 10px; }

    /* Metrik Kartları (Sağ panel) */
    .metric-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .metric-label { color: #8b949e; font-size: 11px; font-weight: 600; }
    .metric-value { color: #58a6ff; font-size: 24px; font-weight: 700; }
    .status-badge { color: #3fb950; font-size: 14px; font-weight: 600; }

    /* Xəbərdarlıq qutusu (AI Studio stili) */
    .warning-box {
        background-color: rgba(187, 128, 9, 0.15);
        border: 1px solid rgba(187, 128, 9, 0.4);
        color: #d29922;
        padding: 12px;
        border-radius: 6px;
        font-size: 13px;
        margin-bottom: 15px;
    }

    /* Düymə stilləri */
    .stButton>button { border-radius: 6px; width: 100%; height: 40px; }
    /* Zoom düyməsi - Mavi */
    div[data-testid="stSidebar"] .stButton>button { background-color: #238636; color: white; border: none; }
    /* Generate Report düyməsi - Ağ/Açıq */
    .report-btn button { background-color: #f0f6fc !important; color: #0d1117 !important; font-weight: bold !important; }

    /* "LIVE MONITORING" etiketi */
    .live-badge {
        background-color: #21262d;
        color: #f0f6fc;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        display: inline-flex;
        align-items: center;
        border: 1px solid #30363d;
    }
    .live-dot { height: 8px; width: 8px; background-color: #f85149; border-radius: 50%; margin-right: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- PDF YARATMA FUNKSIYASI (Fixed AttributeError) ---
def create_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA - Construction Monitoring Report", ln=1)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1)
    pdf.cell(0, 10, f"Location: {lat}, {lon}", ln=1)
    pdf.ln(10)
    pdf.cell(0, 10, "Detection Results: 6 new structures detected.", ln=1)
    
    # fpdf2-də output() birbaşa bayt qaytarır
    return pdf.output()

# --- SIDEBAR (Sol Panel) ---
with st.sidebar:
    st.markdown('<div style="display:flex; align-items:center; gap:10px;"><img src="https://cdn-icons-png.flaticon.com/512/2092/2092030.png" width="30"><h3>SATELLA</h3></div>', unsafe_allow_html=True)
    st.caption("CONSTRUCTION MONITORING")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-header">🔍 AREA OF INTEREST</p>', unsafe_allow_html=True)
    col_in1, col_in2 = st.columns(2)
    with col_in1:
        lat_in = st.text_input("Latitude", value="40.4093", label_visibility="collapsed")
    with col_in2:
        lon_in = st.text_input("Longitude", value="49.8671", label_visibility="collapsed")
    
    if st.button("Zoom to Coordinate"):
        st.session_state.lat = lat_in
        st.session_state.lon = lon_in

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="sidebar-header">📁 RASTER DATA</p>', unsafe_allow_html=True)
    st.file_uploader("Baseline (T0).tif", type=["jpg", "png", "tif"])
    st.file_uploader("Current (T1).tif", type=["jpg", "png", "tif"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Run Change Detection", type="secondary", disabled=True)
    
    st.markdown("<br><br><br><br>")
    st.markdown('<div style="font-size:10px; color:#8b949e;">SATELLA v1.0 | Sentinel-2 & Azercosmos Integration.</div>', unsafe_allow_html=True)

# --- MAIN INTERFACE (Mərkəz və Sağ) ---
col_map, col_sys = st.columns([3, 1])

with col_map:
    st.markdown('<div class="live-badge"><span class="live-dot"></span> LIVE MONITORING</div>', unsafe_allow_html=True)
    
    c_lat = float(st.session_state.get('lat', 40.4093))
    c_lon = float(st.session_state.get('lon', 49.8671))
    
    # Xəritə (Dark Mode)
    m = folium.Map(location=[c_lat, c_lon], zoom_start=15, tiles="CartoDB dark_matter", control_scale=True)
    folium.Marker([c_lat, c_lon]).add_to(m)
    
    # Xəritənin ölçüsünü şəkildəki kimi böyüdürük
    folium_static(m, width=950, height=600)

with col_sys:
    st.markdown('### 📊 System Metrics')
    
    # New Structures & Status Cards
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown(f'<div class="metric-box"><p class="metric-label">NEW STRUCTURES</p><p class="metric-value">6</p></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown(f'<div class="metric-box"><p class="metric-label">STATUS</p><p class="status-badge">✓ Ready</p></div>', unsafe_allow_html=True)
    
    # Progress Bars (AI Studio stili rənglərlə)
    st.markdown('<p class="metric-label">PRECISION (IOU)</p>', unsafe_allow_html=True)
    st.progress(0.92)
    st.caption("92%")
    
    st.markdown('<p class="metric-label">RECALL RATE</p>', unsafe_allow_html=True)
    st.progress(0.88)
    st.caption("88%")
    
    st.markdown('<p class="metric-label">F1 PERFORMANCE</p>', unsafe_allow_html=True)
    st.progress(0.90)
    st.caption("90%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Xəbərdarlıq qutusu
    st.markdown("""
        <div class="warning-box">
            <b>⚠️ Verification Required</b><br>
            Changes detected in sensitive zones. Generated reports must be submitted to FHN for field verification.
        </div>
    """, unsafe_allow_html=True)
    
    # PDF Düyməsi (Ağ rəngli)
    pdf_bytes = create_pdf(c_lat, c_lon)
    st.markdown('<div class="report-btn">', unsafe_allow_html=True)
    st.download_button(
        label="📄 Generate FHN Report (PDF)",
        data=pdf_bytes,
        file_name="SATELLA_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
