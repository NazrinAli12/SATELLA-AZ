import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. Səhifə konfiqurasiyası (Google AI Studio tərzi)
st.set_page_config(
    page_title="Google AI Studio", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. Google AI Studio Professional CSS
st.markdown("""
    <style>
    /* Ana Fon */
    .main { background-color: #0b0d0f !important; }
    
    /* Sol Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid #1e2227 !important;
        width: 280px !important;
    }

    /* Sağ Panel (System Metrics) */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #1e2227 !important;
        padding: 25px !important;
        min-height: 100vh;
    }

    /* Metrik Kartları */
    .m-card {
        background-color: #1a1f26;
        border: 1px solid #2d333b;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
    }
    .m-label { color: #8b949e; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; }
    .m-value { color: #c9d1d9; font-size: 24px; font-weight: 600; }
    .m-status { color: #3fb950; font-size: 13px; font-weight: 600; }

    /* Proqress Barlar */
    .p-container { margin-top: 15px; }
    .p-label-row { display: flex; justify-content: space-between; font-size: 11px; color: #8b949e; font-weight: 600; margin-bottom: 6px; }
    .p-bar-bg { background: #2d333b; border-radius: 10px; height: 6px; width: 100%; }
    .p-bar-fill { height: 100%; border-radius: 10px; }

    /* PDF Düyməsi (Ağ Google Düyməsi) */
    div.stDownloadButton > button {
        background-color: #ffffff !important;
        color: #0d1117 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100% !important;
        height: 42px !important;
        margin-top: 20px !important;
    }

    /* Sidebar Girişləri */
    .stTextInput input { background-color: #1a1f26 !important; border: 1px solid #2d333b !important; color: white !important; }
    .upload-box { border: 1px dashed #2d333b; padding: 15px; border-radius: 8px; text-align: center; color: #8b949e; font-size: 11px; margin-bottom: 10px; }

    /* Xəritə Live Badge */
    .live-tag {
        background: #1a1f26; border: 1px solid #2d333b; padding: 5px 12px;
        border-radius: 6px; color: white; font-size: 11px; font-weight: 700;
        display: inline-flex; align-items: center; margin-bottom: 15px;
    }
    .dot { height: 8px; width: 8px; background: #f85149; border-radius: 50%; margin-right: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 3. PDF Generator (Stabil Bayt Metodu)
def get_pdf_report(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "SATELLA MONITORING REPORT", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(0, 10, f"Location: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, "Result: 6 New structures detected via satellite imagery.", ln=True)
    return bytes(pdf.output())

# --- LAYOUT (Gap xətası "small" ilə düzəldildi) ---
col_map, col_right = st.columns([3.8, 1.2], gap="small")

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown('<div style="display:flex; align-items:center; gap:10px;"><div style="background:#2463eb; padding:6px; border-radius:6px; font-weight:bold; color:white;">🛰️</div> <h2 style="margin:0; font-size:20px; color:white;">SATELLA</h2></div>', unsafe_allow_html=True)
    st.caption("GOOGLE AI STUDIO CLONE")
    
    st.markdown("<br><p style='font-size:11px; font-weight:700; color:#8b949e;'>🔍 AREA OF INTEREST</p>", unsafe_allow_html=True)
    s_c1, s_c2 = st.columns(2)
    with s_c1: lat_val = st.text_input("Lat", "40.4093", label_visibility="collapsed")
    with s_c2: lon_val = st.text_input("Lon", "49.8671", label_visibility="collapsed")
    
    if st.button("Zoom to Coordinate", type="primary", use_container_width=True):
        st.session_state.lat, st.session_state.lon = lat_val, lon_val

    st.markdown("<br><p style='font-size:11px; font-weight:700; color:#8b949e;'>📁 RASTER DATA</p>", unsafe_allow_html=True)
    st.markdown('<div class="upload-box">📄 Baseline (T0).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T0", label_visibility="collapsed", key="u1")
    st.markdown('<div class="upload-box">📄 Current (T1).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T1", label_visibility="collapsed", key="u2")
    
    st.button("Run Change Detection", disabled=True, use_container_width=True)

# --- MƏRKƏZİ HİSSƏ (MAP) ---
with col_map:
    st.markdown('<div class="live-tag"><span class="dot"></span> LIVE MONITORING</div>', unsafe_allow_html=True)
    c_lat = float(st.session_state.get('lat', 40.4093))
    c_lon = float(st.session_state.get('lon', 49.8671))
    
    # Google AI Studio tərzində ağ təmiz xəritə
    m = folium.Map(location=[c_lat, c_lon], zoom_start=15, tiles="OpenStreetMap")
    folium.Marker([c_lat, c_lon]).add_to(m)
    folium_static(m, width=1180, height=850)

# --- SAĞ PANEL (SYSTEM METRICS) ---
with col_right:
    st.markdown('<h3 style="color:white; font-size:18px; margin-bottom:20px;">📊 System Metrics</h3>', unsafe_allow_html=True)
    
    # Metriklər
    r1, r2 = st.columns(2)
    with r1: st.markdown('<div class="m-card"><p class="m-label">NEW STRUCTURES</p><p class="m-value">6</p></div>', unsafe_allow_html=True)
    with r2: st.markdown('<div class="m-card"><p class="m-label">STATUS</p><p class="m-status">✓ Ready</p></div>', unsafe_allow_html=True)
    
    # Proqress Barlar
    p_data = [("PRECISION (IOU)", "92%", "#388bfd"), ("RECALL RATE", "88%", "#3fb950"), ("F1 PERFORMANCE", "90%", "#a371f7")]
    for label, val, color in p_data:
        st.markdown(f'''
            <div class="p-container">
                <div class="p-label-row"><span>{label}</span><span>{val}</span></div>
                <div class="p-bar-bg"><div class="p-bar-fill" style="width:{val}; background:{color};"></div></div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown('<div style="background:rgba(187,128,9,0.1); border:1px solid #d29922; padding:15px; border-radius:8px; color:#d29922; font-size:11px; margin-top:20px;"><b>🛡️ Verification Required</b><br>Submit generated reports to FHN.</div>', unsafe_allow_html=True)

    # PDF DOWNLOAD DÜYMƏSİ (ARTIQ SAĞDADIR VƏ XƏTASIZDIR)
    pdf_bytes = get_pdf_report(c_lat, c_lon)
    st.download_button(
        label="📄 Generate FHN Report (PDF)",
        data=pdf_bytes,
        file_name="SATELLA_FHN_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
    st.markdown("<p style='font-size:11px; color:#484f58; margin-top:30px;'>No active detections in session.</p>", unsafe_allow_html=True)
