import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. Səhifə Ayarları
st.set_page_config(page_title="Google AI Studio - Satella", layout="wide", initial_sidebar_state="expanded")

# 2. AI Studio UI CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0f !important;
    }

    /* Sidebar - AI Studio Tünd */
    [data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid #1e2227;
    }

    /* Sağ Panel - Metrics */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #1e2227;
        padding: 24px !important;
        min-height: 100vh;
    }

    /* Metrik Kartları */
    .metric-box {
        background-color: #1a1f26;
        border: 1px solid #2d333b;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .m-title { color: #8b949e; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; }
    .m-val { color: #58a6ff; font-size: 28px; font-weight: 700; }
    .m-status { color: #3fb950; font-size: 14px; font-weight: 600; }

    /* Proqress Barlar */
    .p-header { display: flex; justify-content: space-between; font-size: 11px; color: #8b949e; font-weight: 700; margin-bottom: 8px; margin-top: 15px; }
    .p-bar-outer { background: #2d333b; border-radius: 10px; height: 6px; width: 100%; margin-bottom: 20px; }
    .p-bar-inner { height: 100%; border-radius: 10px; }

    /* PDF Düyməsi (Google AI Studio Ağ Düymə Stili) */
    div.stDownloadButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        height: 44px !important;
        border-radius: 6px !important;
        border: none !important;
        width: 100% !important;
        margin-top: 25px !important;
    }

    .warning-card {
        background-color: rgba(187, 128, 9, 0.08);
        border: 1px solid rgba(187, 128, 9, 0.3);
        border-radius: 8px;
        padding: 16px;
        color: #d29922;
        font-size: 12px;
        line-height: 1.5;
        margin-top: 20px;
    }

    .live-indicator {
        background: #1a1f26; border: 1px solid #2d333b;
        color: white; padding: 6px 14px; border-radius: 8px;
        font-size: 11px; font-weight: 700; display: inline-flex; align-items: center; margin-bottom: 10px;
    }
    .pulse-dot { height: 8px; width: 8px; background: #f85149; border-radius: 50%; margin-right: 8px; }

    /* Inputlar */
    .stTextInput input { background-color: #1a1f26 !important; border: 1px solid #2d333b !important; color: white !important; }
    .upload-container { border: 1px dashed #2d333b; padding: 15px; border-radius: 8px; text-align: center; color: #8b949e; font-size: 12px; margin-bottom: 12px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Stabil PDF Generator
def generate_pdf_report(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA CONSTRUCTION ANALYSIS", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(0, 10, f"Location: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, "Result: 6 New structures identified.", ln=True)
    # Streamlit üçün bayt formatına çeviririk
    return bytes(pdf.output())

# --- LAYOUT (Gap xətası burada düzəldildi) ---
col_map, col_metrics = st.columns([3.6, 1.2], gap="small")

# --- LEFT SIDEBAR ---
with st.sidebar:
    st.markdown('<div style="display:flex; align-items:center; gap:12px; margin-bottom:20px;"><div style="background:#2463eb; padding:8px; border-radius:8px; font-weight:900; color:white;">🛰️</div> <h2 style="margin:0; font-size:18px; color:white;">SATELLA</h2></div>', unsafe_allow_html=True)
    
    st.markdown("<p style='font-size:11px; font-weight:700; color:#8b949e;'>🔍 AREA OF INTEREST</p>", unsafe_allow_html=True)
    sub_c1, sub_c2 = st.columns(2)
    with sub_c1: lat_input = st.text_input("Lat", "40.4093", key="lat_in", label_visibility="collapsed")
    with sub_c2: lon_input = st.text_input("Lon", "49.8671", key="lon_in", label_visibility="collapsed")
    
    if st.button("Zoom to Coordinate", use_container_width=True):
        st.session_state.lat, st.session_state.lon = lat_input, lon_input

    st.markdown("<br><p style='font-size:11px; font-weight:700; color:#8b949e;'>📁 RASTER DATA</p>", unsafe_allow_html=True)
    st.markdown('<div class="upload-container">📄 Baseline (T0).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T0", label_visibility="collapsed", key="file1")
    st.markdown('<div class="upload-container">📄 Current (T1).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T1", label_visibility="collapsed", key="file2")
    
    st.button("Run Change Detection", disabled=True, use_container_width=True)

# --- CENTRAL MAP ---
with col_map:
    st.markdown('<div class="live-indicator"><span class="pulse-dot"></span> LIVE MONITORING</div>', unsafe_allow_html=True)
    c_lat = float(st.session_state.get('lat', 40.4093))
    c_lon = float(st.session_state.get('lon', 49.8671))
    
    m = folium.Map(location=[c_lat, c_lon], zoom_start=15, tiles="OpenStreetMap")
    folium.Marker([c_lat, c_lon]).add_to(m)
    folium_static(m, width=1100, height=800)

# --- RIGHT PANEL ---
with col_metrics:
    st.markdown('<h3 style="color:white; font-size:18px; margin-bottom:24px;">📊 System Metrics</h3>', unsafe_allow_html=True)
    
    m_c1, m_c2 = st.columns(2)
    with m_c1: st.markdown('<div class="metric-box"><p class="m-title">NEW STRUCTURES</p><p class="m-val">6</p></div>', unsafe_allow_html=True)
    with m_c2: st.markdown('<div class="metric-box"><p class="m-title">STATUS</p><p class="m-status">✓ Ready</p></div>', unsafe_allow_html=True)
    
    metrics = [("PRECISION (IOU)", "92%", "#388bfd"), ("RECALL RATE", "88%", "#3fb950"), ("F1 PERFORMANCE", "90%", "#a371f7")]
    for label, val, color in metrics:
        st.markdown(f"""
            <div class="p-header"><span>{label}</span><span>{val}</span></div>
            <div class="p-bar-outer"><div class="p-bar-inner" style="width:{val}; background:{color};"></div></div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="warning-card">🛡️ <b>Verification Required</b><br>Submit generated reports to FHN.</div>', unsafe_allow_html=True)

    # PDF DÜYMƏSİ
    report_data = generate_pdf_report(c_lat, c_lon)
    st.download_button(
        label="📄 Generate FHN Report (PDF)",
        data=report_data,
        file_name="SATELLA_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
