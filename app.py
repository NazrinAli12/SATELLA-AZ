import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
import io
from fpdf import FPDF

# 1. Səhifə Ayarları
st.set_page_config(page_title="SATELLA - Construction Monitoring", layout="wide", initial_sidebar_state="expanded")

# 2. AI STUDIO EXACT UI (CSS İlə)
st.markdown("""
    <style>
    /* Ümumi Fon */
    .main { background-color: #0d1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #151921; border-right: 1px solid #30363d; }
    
    /* Sidebar Giriş Qutuları */
    .stTextInput input { background-color: #1c2128 !important; border: 1px solid #30363d !important; color: white !important; }
    
    /* AI Studio Göy Düymə (Zoom to Coordinate) */
    .zoom-btn button {
        background-color: #2463eb !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        width: 100%;
        border: none !important;
        height: 40px;
    }

    /* Dashed Upload Qutuları (Sidebar) */
    .upload-box {
        border: 1px dashed #484f58;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        margin-bottom: 10px;
        background-color: #161b22;
    }

    /* Live Monitoring Etiketi (Xəritə üzərində) */
    .live-badge {
        background: #21262d;
        border: 1px solid #30363d;
        color: white;
        padding: 6px 14px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        margin-bottom: 10px;
    }
    .red-dot { height: 8px; width: 8px; background-color: #f85149; border-radius: 50%; margin-right: 8px; }

    /* Sağ Panel - Metrik Kartları */
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .metric-label { color: #8b949e; font-size: 10px; font-weight: 700; text-transform: uppercase; }
    .metric-value { font-size: 28px; font-weight: 700; margin-top: 5px; }
    .status-ready { color: #3fb950; font-size: 14px; font-weight: 600; }

    /* Progress Barlar (Xüsusi Rənglərlə) */
    .progress-text { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 5px; font-weight: 600; }
    .p-bar-bg { background: #21262d; border-radius: 10px; height: 8px; width: 100%; margin-bottom: 20px; }
    .p-bar-fill-blue { background: #388bfd; height: 8px; border-radius: 10px; }
    .p-bar-fill-green { background: #3fb950; height: 8px; border-radius: 10px; }
    .p-bar-fill-purple { background: #a371f7; height: 8px; border-radius: 10px; }

    /* Verification Box (Sarımtıl) */
    .verify-box {
        background-color: rgba(187, 128, 9, 0.1);
        border: 1px solid rgba(187, 128, 9, 0.4);
        padding: 15px;
        border-radius: 8px;
        color: #d29922;
        font-size: 12px;
        margin-top: 10px;
    }

    /* Generate Report Düyməsi (Ağ fonda qara yazı) */
    .report-btn button {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: none !important;
        width: 100%;
        height: 45px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. PDF Funksiyası (StreamlitAPIException Həlli)
def get_pdf_data(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA - Construction Monitoring Report", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Coordinates: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    # output(dest='S') yerinə byte istifadə edirik
    return pdf.output()

# --- SOL PANEL (SIDEBAR) ---
with st.sidebar:
    st.markdown('<div style="display:flex; align-items:center; gap:10px;"><div style="background:#2463eb; padding:5px; border-radius:5px;">🛰️</div> <h2 style="margin:0; font-size:18px;">SATELLA</h2></div>', unsafe_allow_html=True)
    st.caption("CONSTRUCTION MONITORING")
    
    st.markdown("<br><p style='font-size:11px; font-weight:700; color:#8b949e;'>🔍 AREA OF INTEREST</p>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    with col_l:
        lat_input = st.text_input("Lat", value="40.4093", label_visibility="collapsed")
    with col_r:
        lon_input = st.text_input("Lon", value="49.8671", label_visibility="collapsed")
    
    st.markdown('<div class="zoom-btn">', unsafe_allow_html=True)
    if st.button("Zoom to Coordinate"):
        st.session_state.lat = lat_input
        st.session_state.lon = lon_input
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><p style='font-size:11px; font-weight:700; color:#8b949e;'>📁 RASTER DATA</p>", unsafe_allow_html=True)
    st.markdown('<div class="upload-box"><small style="color:#8b949e;">📄 Baseline (T0).tif</small></div>', unsafe_allow_html=True)
    st.file_uploader("Upload T0", label_visibility="collapsed", key="u1")
    
    st.markdown('<div class="upload-box"><small style="color:#8b949e;">📄 Current (T1).tif</small></div>', unsafe_allow_html=True)
    st.file_uploader("Upload T1", label_visibility="collapsed", key="u2")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Run Change Detection", disabled=True, use_container_width=True)

# --- ƏSAS ORTA HİSSƏ (MAP) ---
col_map, col_metrics = st.columns([3.2, 1.2])

with col_map:
    st.markdown('<div class="live-badge"><span class="red-dot"></span> LIVE MONITORING</div>', unsafe_allow_html=True)
    
    c_lat = float(st.session_state.get('lat', 40.4093))
    c_lon = float(st.session_state.get('lon', 49.8671))
    
    # AI Studio tərzində tünd xəritə
    m = folium.Map(location=[c_lat, c_lon], zoom_start=15, tiles="CartoDB dark_matter")
    folium.Marker([c_lat, c_lon]).add_to(m)
    folium_static(m, width=980, height=680)

# --- SAĞ PANEL (SYSTEM METRICS) ---
with col_metrics:
    st.markdown('<h3 style="font-size:18px; display:flex; align-items:center; gap:8px;">📊 System Metrics</h3>', unsafe_allow_html=True)
    
    # New Structures & Status
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown('<div class="metric-card"><p class="metric-label">NEW STRUCTURES</p><p class="metric-value">0</p></div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown('<div class="metric-card"><p class="metric-label">STATUS</p><p class="status-ready">✓ Ready</p></div>', unsafe_allow_html=True)
    
    # Precision Bar
    st.markdown('<div class="progress-text"><span>PRECISION (IOU)</span><span>92%</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="p-bar-bg"><div class="p-bar-fill-blue" style="width: 92%;"></div></div>', unsafe_allow_html=True)

    # Recall Bar
    st.markdown('<div class="progress-text"><span>RECALL RATE</span><span>88%</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="p-bar-bg"><div class="p-bar-fill-green" style="width: 88%;"></div></div>', unsafe_allow_html=True)

    # F1 Bar
    st.markdown('<div class="progress-text"><span>F1 PERFORMANCE</span><span>90%</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="p-bar-bg"><div class="p-bar-fill-purple" style="width: 90%;"></div></div>', unsafe_allow_html=True)

    # Verification Warning
    st.markdown("""
        <div class="verify-box">
            <b>🛡️ Verification Required</b><br>
            Changes detected in sensitive zones. Generated reports must be submitted to FHN for field verification.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # PDF Düyməsi (Xətasız Versiya)
    pdf_bytes = get_pdf_data(c_lat, c_lon)
    st.markdown('<div class="report-btn">', unsafe_allow_html=True)
    st.download_button(
        label="📄 Generate FHN Report (PDF)",
        data=pdf_bytes,
        file_name="SATELLA_FHN_Report.pdf",
        mime="application/pdf"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><p style='font-size:11px; color:#484f58; font-weight:700;'>⚠️ DETECTION HISTORY</p>", unsafe_allow_html=True)
    st.caption("No active detections in session.")
