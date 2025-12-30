import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. Professional Ekran Ayarı
st.set_page_config(page_title="SATELLA - AI Studio", layout="wide", initial_sidebar_state="expanded")

# 2. AI Studio UI - CSS (Şəkildəki tünd sidebar və sağ panel üçün)
st.markdown("""
    <style>
    /* Fon rəngləri */
    .main { background-color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111418 !important; border-right: 1px solid #1e2227; }
    
    /* Sağ Panel - Metrics */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418;
        color: white;
        padding: 25px !important;
        border-left: 1px solid #1e2227;
        min-height: 100vh;
    }

    /* Metrik Kartları */
    .metric-card {
        background-color: #1a1f26;
        border: 1px solid #2d333b;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .m-label { color: #8b949e; font-size: 10px; font-weight: 700; text-transform: uppercase; }
    .m-value { color: #58a6ff; font-size: 26px; font-weight: 700; }
    .status-ok { color: #3fb950; font-size: 14px; font-weight: 600; }

    /* Proqress Bar Dizaynı */
    .p-container { margin-bottom: 20px; }
    .p-text { display: flex; justify-content: space-between; font-size: 11px; color: #8b949e; margin-bottom: 5px; }
    .p-bg { background: #2d333b; border-radius: 10px; height: 6px; width: 100%; }
    .p-fill { height: 100%; border-radius: 10px; }

    /* Report Düyməsi (Ağ rəngli professional düymə) */
    .stDownloadButton button {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 700 !important;
        height: 48px !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100%;
        margin-top: 20px;
    }

    /* Sidebar Elementləri */
    .stTextInput input { background-color: #1a1f26 !important; border: 1px solid #2d333b !important; color: white !important; }
    .upload-box { border: 1px dashed #2d333b; padding: 15px; border-radius: 8px; text-align: center; color: #8b949e; font-size: 11px; margin-bottom: 10px; }
    
    /* Live Badge */
    .live-badge {
        position: absolute; top: 15px; left: 15px; z-index: 999;
        background: #1a1f26; border: 1px solid #2d333b; padding: 5px 12px;
        border-radius: 6px; color: white; font-size: 11px; display: flex; align-items: center;
    }
    .red-dot { height: 8px; width: 8px; background: #f85149; border-radius: 50%; margin-right: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 3. PDF FUNKSİYASI (ERROR FIX: Bytes conversion)
def get_pdf_bytes(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="SATELLA - Construction Monitoring Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(200, 10, txt=f"Location: {lat}, {lon}", ln=True)
    pdf.cell(200, 10, txt="Status: 6 Detected Structures (Illegal)", ln=True)
    
    # Əsas hissə: Obyekti bayt-a çeviririk
    return pdf.output(dest='S').encode('latin-1')

# --- UI LAYOUT ---
col_map, col_right = st.columns([3.5, 1.3], gap="none")

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown('<div style="display:flex; align-items:center; gap:10px;"><div style="background:#2463eb; padding:6px; border-radius:6px; font-weight:900; color:white;">🛰️</div> <h2 style="margin:0; font-size:20px; color:white;">SATELLA</h2></div>', unsafe_allow_html=True)
    st.caption("CONSTRUCTION MONITORING")
    
    st.markdown("<br><p style='font-size:11px; font-weight:700; color:#8b949e;'>🔍 AREA OF INTEREST</p>", unsafe_allow_html=True)
    s_c1, s_c2 = st.columns(2)
    with s_c1: lat_in = st.text_input("Lat", "40.4093", label_visibility="collapsed")
    with s_c2: lon_in = st.text_input("Lon", "49.8671", label_visibility="collapsed")
    
    if st.button("Zoom to Coordinate", type="primary", use_container_width=True):
        st.session_state.lat, st.session_state.lon = lat_in, lon_in

    st.markdown("<br><p style='font-size:11px; font-weight:700; color:#8b949e;'>📁 RASTER DATA</p>", unsafe_allow_html=True)
    st.markdown('<div class="upload-box">📄 Baseline (T0).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T0", label_visibility="collapsed", key="u1")
    st.markdown('<div class="upload-box">📄 Current (T1).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T1", label_visibility="collapsed", key="u2")
    
    st.button("Run Change Detection", disabled=True, use_container_width=True)

# --- MƏRKƏZİ XƏRİTƏ ---
with col_map:
    st.markdown('<div class="live-badge"><span class="red-dot"></span> LIVE MONITORING</div>', unsafe_allow_html=True)
    c_lat = float(st.session_state.get('lat', 40.4093))
    c_lon = float(st.session_state.get('lon', 49.8671))
    
    m = folium.Map(location=[c_lat, c_lon], zoom_start=15, tiles="OpenStreetMap")
    folium.Marker([c_lat, c_lon]).add_to(m)
    folium_static(m, width=1050, height=750)

# --- SAĞ PANEL (AI Studio Stylized) ---
with col_right:
    st.markdown('<h3 style="color:white; font-size:18px;">📊 System Metrics</h3>', unsafe_allow_html=True)
    
    # Metriklər
    m1, m2 = st.columns(2)
    with m1: st.markdown('<div class="metric-card"><p class="m-label">NEW STRUCTURES</p><p class="m-value">6</p></div>', unsafe_allow_html=True)
    with m2: st.markdown('<div class="metric-card"><p class="m-label">STATUS</p><p class="status-ok">✓ Ready</p></div>', unsafe_allow_html=True)
    
    # Proqress Barlar
    p_data = [("PRECISION (IOU)", "92%", "#388bfd"), ("RECALL RATE", "88%", "#3fb950"), ("F1 PERFORMANCE", "90%", "#a371f7")]
    for label, val, color in p_data:
        st.markdown(f'<div class="p-container"><div class="p-text"><span>{label}</span><span>{val}</span></div><div class="p-bg"><div class="p-fill" style="width:{val}; background:{color};"></div></div></div>', unsafe_allow_html=True)

    # Verification Warning
    st.markdown('<div style="background:rgba(187,128,9,0.1); border:1px solid #d29922; padding:15px; border-radius:8px; color:#d29922; font-size:12px;"><b>🛡️ Verification Required</b><br>Changes detected in sensitive zones. Submit to FHN.</div>', unsafe_allow_html=True)

    # PDF DOWNLOAD (FIXED)
    pdf_data = get_pdf_bytes(c_lat, c_lon)
    st.download_button(
        label="📄 Generate FHN Report (PDF)",
        data=pdf_data,
        file_name="SATELLA_Report.pdf",
        mime="application/pdf"
    )

    st.markdown("<p style='font-size:11px; color:#8b949e; margin-top:20px;'>⚠ DETECTION HISTORY</p>", unsafe_allow_html=True)
    st.caption("No active detections in session.")
