import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. Səhifə konfiqurasiyası
st.set_page_config(page_title="SATELLA - AI Studio UI", layout="wide", initial_sidebar_state="expanded")

# 2. AI STUDIO EXACT UI (CSS)
st.markdown("""
    <style>
    /* Ana fon ağ (Map üçün), Sidebarlar tünd */
    .main { background-color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111418 !important; border-right: 1px solid #1e2227; }
    
    /* Sağ panel (Metrics Sidebar) */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        padding: 25px !important;
        border-left: 1px solid #1e2227;
        min-height: 100vh;
        color: white;
    }

    /* Metrik Kartları */
    .m-card {
        background-color: #1a1f26;
        border: 1px solid #2d333b;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
    }
    .m-label { color: #8b949e; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 5px; }
    .m-value { color: #58a6ff; font-size: 26px; font-weight: 700; }
    .m-status { color: #3fb950; font-size: 13px; font-weight: 600; }

    /* Proqress Barlar */
    .p-row { margin-top: 18px; }
    .p-head { display: flex; justify-content: space-between; font-size: 11px; color: #8b949e; font-weight: 700; margin-bottom: 6px; }
    .p-bg { background: #2d333b; border-radius: 10px; height: 6px; width: 100%; }
    .p-fill { height: 100%; border-radius: 10px; }

    /* Xəbərdarlıq qutusu */
    .warn-box {
        background-color: rgba(187, 128, 9, 0.1);
        border: 1px solid rgba(187, 128, 9, 0.3);
        border-radius: 8px;
        padding: 15px;
        color: #d29922;
        font-size: 12px;
        margin-top: 25px;
    }

    /* PDF Düyməsi - Tam AI Studio stili (Ağ düymə) */
    .stDownloadButton > button {
        background-color: #ffffff !important;
        color: #0d1117 !important;
        font-weight: 700 !important;
        height: 45px !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100% !important;
        margin-top: 20px !important;
    }

    /* Sidebar Elementləri */
    .stTextInput input { background-color: #1a1f26 !important; border: 1px solid #2d333b !important; color: white !important; }
    .up-box { border: 1px dashed #2d333b; padding: 15px; border-radius: 8px; text-align: center; color: #8b949e; font-size: 11px; margin-bottom: 10px; }
    
    /* Live Badge */
    .live-tag {
        background: #1a1f26; border: 1px solid #2d333b; padding: 6px 12px;
        border-radius: 8px; color: white; font-size: 11px; font-weight: 700;
        display: inline-flex; align-items: center; margin-bottom: 15px;
    }
    .red-dot { height: 8px; width: 8px; background: #f85149; border-radius: 50%; margin-right: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 3. PDF Yaratma (ERROR FIX)
def get_pdf_output(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "SATELLA MONITORING REPORT", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(0, 10, f"Location Coordinates: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, "Result: 6 New structures detected.", ln=True)
    
    # fpdf2-də 'dest=S' əvəzinə output() bayt massivi qaytarır
    return bytes(pdf.output())

# --- LAYOUT STRUKTURU ---
col_map, col_right = st.columns([3.5, 1.2], gap="none")

# --- SOL SIDEBAR (Inputlar) ---
with st.sidebar:
    st.markdown('<div style="display:flex; align-items:center; gap:12px;"><div style="background:#2463eb; padding:6px; border-radius:6px; font-weight:bold; color:white;">🛰️</div> <h2 style="margin:0; font-size:20px; color:white;">SATELLA</h2></div>', unsafe_allow_html=True)
    st.caption("CONSTRUCTION MONITORING")
    
    st.markdown("<br><p style='font-size:11px; font-weight:700; color:#8b949e;'>🔍 AREA OF INTEREST</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: lat_val = st.text_input("Lat", "40.4093", label_visibility="collapsed")
    with c2: lon_val = st.text_input("Lon", "49.8671", label_visibility="collapsed")
    
    if st.button("Zoom to Coordinate", type="primary", use_container_width=True):
        st.session_state.lat, st.session_state.lon = lat_val, lon_val

    st.markdown("<br><p style='font-size:11px; font-weight:700; color:#8b949e;'>📁 RASTER DATA</p>", unsafe_allow_html=True)
    st.markdown('<div class="up-box">📄 Baseline (T0).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T0", label_visibility="collapsed", key="u1")
    st.markdown('<div class="up-box">📄 Current (T1).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T1", label_visibility="collapsed", key="u2")
    
    st.button("Run Change Detection", disabled=True, use_container_width=True)

# --- MƏRKƏZİ HİSSƏ (MAP) ---
with col_map:
    st.markdown('<div class="live-tag"><span class="red-dot"></span> LIVE MONITORING</div>', unsafe_allow_html=True)
    curr_lat = float(st.session_state.get('lat', 40.4093))
    curr_lon = float(st.session_state.get('lon', 49.8671))
    
    # AI Studio tərzində xəritə
    m = folium.Map(location=[curr_lat, curr_lon], zoom_start=15, tiles="OpenStreetMap")
    folium.Marker([curr_lat, curr_lon]).add_to(m)
    folium_static(m, width=1100, height=780)

# --- SAĞ PANEL (SYSTEM METRICS & DOWNLOAD) ---
with col_right:
    st.markdown('<h3 style="color:white; font-size:18px; margin-bottom:20px;">📊 System Metrics</h3>', unsafe_allow_html=True)
    
    # Metrik Qutuları
    m1, m2 = st.columns(2)
    with m1: st.markdown('<div class="m-card"><p class="m-label">NEW STRUCTURES</p><p class="m-value">6</p></div>', unsafe_allow_html=True)
    with m2: st.markdown('<div class="m-card"><p class="m-label">STATUS</p><p class="m-status">✓ Ready</p></div>', unsafe_allow_html=True)
    
    # Proqress Barlar
    p_data = [("PRECISION (IOU)", "92%", "#388bfd"), ("RECALL RATE", "88%", "#3fb950"), ("F1 PERFORMANCE", "90%", "#a371f7")]
    for label, val, color in p_data:
        st.markdown(f'<div class="p-row"><div class="p-head"><span>{label}</span><span>{val}</span></div><div class="p-bg"><div class="p-fill" style="width:{val}; background:{color};"></div></div></div>', unsafe_allow_html=True)

    # Verification Box
    st.markdown('<div class="warn-box"><b>🛡️ Verification Required</b><br>Changes detected in sensitive zones. Submit to FHN.</div>', unsafe_allow_html=True)

    # --- PDF DOWNLOAD DÜYMƏSİ (ARTIQ SAĞDADIR VƏ XƏTASIZDIR) ---
    try:
        pdf_bytes = get_pdf_output(curr_lat, curr_lon)
        st.download_button(
            label="📄 Generate FHN Report (PDF)",
            data=pdf_bytes,
            file_name="SATELLA_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Download Error: {e}")

    st.markdown("<p style='font-size:11px; color:#8b949e; margin-top:30px;'>⚠ DETECTION HISTORY</p>", unsafe_allow_html=True)
    st.caption("No active detections.")
