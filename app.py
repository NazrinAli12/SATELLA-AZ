import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. Səhifə konfiqurasiyası
st.set_page_config(page_title="SATELLA - AI Studio UI", layout="wide", initial_sidebar_state="expanded")

# 2. AI STUDIO EXACT CSS (Skrinşotlardakı rəng və ölçülər)
st.markdown("""
    <style>
    /* Ana Fon və Sidebar */
    .main { background-color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #111418 !important; border-right: 1px solid #1e2227; min-width: 300px !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    
    /* Sağ Panel (System Metrics) */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418;
        padding: 20px !important;
        min-height: 100vh;
        border-left: 1px solid #1e2227;
    }

    /* Kartlar (Sağ Panel) */
    .metric-card {
        background-color: #1a1f26;
        border: 1px solid #2d333b;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
    }
    .metric-label { color: #8b949e; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; }
    .metric-value { color: #58a6ff; font-size: 28px; font-weight: 700; }
    .status-text { color: #3fb950; font-size: 14px; font-weight: 600; }

    /* Proqress Barlar */
    .p-container { margin-top: 20px; }
    .p-header { display: flex; justify-content: space-between; font-size: 11px; color: #8b949e; font-weight: 700; margin-bottom: 6px; }
    .p-bar-bg { background: #2d333b; border-radius: 10px; height: 6px; width: 100%; overflow: hidden; margin-bottom: 15px; }
    .p-fill { height: 100%; border-radius: 10px; }

    /* Düymələr */
    .stButton>button { width: 100%; border-radius: 8px; font-weight: 600; border: none; transition: 0.2s; }
    /* Zoom - Göy */
    .zoom-btn button { background-color: #2463eb !important; color: white !important; height: 42px; }
    /* Report - Ağ */
    .report-btn button { background-color: #ffffff !important; color: #000000 !important; height: 48px; margin-top: 20px; }
    
    /* Warning Box */
    .warn-box {
        background-color: rgba(187, 128, 9, 0.1);
        border: 1px solid rgba(187, 128, 9, 0.3);
        border-radius: 10px;
        padding: 15px;
        color: #d29922;
        font-size: 12px;
        margin-top: 20px;
        line-height: 1.5;
    }

    /* Live Monitoring Badge */
    .live-badge {
        position: absolute; top: 20px; left: 20px; z-index: 1000;
        background: #1a1f26; border: 1px solid #2d333b;
        color: white; padding: 6px 12px; border-radius: 8px;
        font-size: 11px; font-weight: 700; display: flex; align-items: center;
    }
    .dot { height: 8px; width: 8px; background: #f85149; border-radius: 50%; margin-right: 8px; }
    
    /* Sidebar Inputlar */
    .stTextInput input { background-color: #1a1f26 !important; border: 1px solid #2d333b !important; }
    .upload-area { border: 1px dashed #2d333b; border-radius: 10px; padding: 20px; text-align: center; margin-bottom: 10px; font-size: 12px; color: #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# 3. PDF GENERATOR (Xətasız Versiya)
def create_pdf_report(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA CONSTRUCTION REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Coordinates: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(0, 10, "Status: 6 New structures detected in the area.", ln=True)
    # Output byte qaytarmalıdır ki, StreamlitAPIException verməsin
    return pdf.output(dest='S').encode('latin-1')

# --- LAYOUT ---
col_left, col_right = st.columns([3.5, 1.2], gap="none")

# --- SOL SIDEBAR (Dizayn: image_d12a71.png) ---
with st.sidebar:
    st.markdown('<div style="display:flex; align-items:center; gap:12px; margin-bottom:5px;"><div style="background:#2463eb; padding:6px; border-radius:6px; font-weight:900;">🛰️</div> <h2 style="margin:0; font-size:20px;">SATELLA</h2></div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:10px; color:#8b949e; margin-top:-10px; letter-spacing:1px;">CONSTRUCTION MONITORING</p>', unsafe_allow_html=True)
    
    st.markdown("<br><p style='font-size:11px; font-weight:700; color:#8b949e;'>🔍 AREA OF INTEREST</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: lat_val = st.text_input("Lat", "40.4093", label_visibility="collapsed")
    with c2: lon_val = st.text_input("Lon", "49.8671", label_visibility="collapsed")
    
    st.markdown('<div class="zoom-btn">', unsafe_allow_html=True)
    if st.button("Zoom to Coordinate"):
        st.session_state.lat, st.session_state.lon = lat_val, lon_val
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><p style='font-size:11px; font-weight:700; color:#8b949e;'>📁 RASTER DATA</p>", unsafe_allow_html=True)
    st.markdown('<div class="upload-area">📄 Baseline (T0).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T0", label_visibility="collapsed", key="u1")
    
    st.markdown('<div class="upload-area">📄 Current (T1).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T1", label_visibility="collapsed", key="u2")
    
    st.button("Run Change Detection", disabled=True)
    
    st.markdown("<div style='margin-top:60px; font-size:10px; color:#484f58;'>SATELLA v1.0 | Sentinel-2 & Azercosmos<br>Developed for FHN Standards.</div>", unsafe_allow_html=True)

# --- MƏRKƏZİ XƏRİTƏ (Dizayn: image_d12aee.png - Light Mode Map) ---
with col_left:
    st.markdown('<div class="live-badge"><span class="dot"></span> LIVE MONITORING</div>', unsafe_allow_html=True)
    
    curr_lat = float(st.session_state.get('lat', 40.4093))
    curr_lon = float(st.session_state.get('lon', 49.8671))
    
    # AI Studio skrinşotundakı kimi ağ (Light) xəritə
    m = folium.Map(location=[curr_lat, curr_lon], zoom_start=15, tiles="OpenStreetMap")
    folium.Marker([curr_lat, curr_lon]).add_to(m)
    folium_static(m, width=1050, height=750)

# --- SAĞ PANEL (Dizayn: image_d12acb.png) ---
with col_right:
    st.markdown('<h3 style="font-size:18px; margin-bottom:25px;">📊 System Metrics</h3>', unsafe_allow_html=True)
    
    # Metriklər yan-yana
    m1, m2 = st.columns(2)
    with m1:
        st.markdown('<div class="metric-card"><p class="metric-label">NEW STRUCTURES</p><p class="metric-value">0</p></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-card"><p class="metric-label">STATUS</p><p class="status-text">✓ Ready</p></div>', unsafe_allow_html=True)
    
    # Proqress Barlar
    metrics_data = [
        ("PRECISION (IOU)", "92%", "#388bfd"),
        ("RECALL RATE", "88%", "#3fb950"),
        ("F1 PERFORMANCE", "90%", "#a371f7")
    ]
    
    for label, val, color in metrics_data:
        st.markdown(f"""
            <div class="p-container">
                <div class="p-header"><span>{label}</span><span>{val}</span></div>
                <div class="p-bar-bg"><div class="p-fill" style="width:{val}; background:{color};"></div></div>
            </div>
        """, unsafe_allow_html=True)

    # Verification Box
    st.markdown("""
        <div class="warn-box">
            <span style="font-size:16px;">🛡️</span> <b>Verification Required</b><br>
            Changes detected in sensitive zones. Generated reports must be submitted to FHN for field verification.
        </div>
    """, unsafe_allow_html=True)

    # PDF DÜYMƏSİ (Download xətasız)
    pdf_content = create_pdf_report(curr_lat, curr_lon)
    st.markdown('<div class="report-btn">', unsafe_allow_html=True)
    st.download_button(
        label="📄 Generate FHN Report (PDF)",
        data=pdf_content,
        file_name=f"FHN_Report_{datetime.now().strftime('%d%m%Y')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<p style='font-size:11px; color:#8b949e; margin-top:30px; font-weight:700;'>⚠ DETECTION HISTORY</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:11px; color:#484f58; font-style:italic;'>No active detections in session.</p>", unsafe_allow_html=True)
