import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
import io
from fpdf import FPDF

# 1. Səhifə Ayarları
st.set_page_config(page_title="SATELLA - Construction Monitoring", layout="wide", initial_sidebar_state="expanded")

# 2. AI Studio-nun Eynisi Olan CSS Dizaynı
st.markdown("""
    <style>
    /* Ana fon və Sidebar rəngləri */
    .main { background-color: #0d1117; color: #c9d1d9; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; padding-top: 20px; }
    
    /* Fontlar və Başlıqlar */
    h1, h2, h3 { color: #f0f6fc !important; font-family: 'Inter', sans-serif; }
    .sidebar-label { color: #8b949e; font-size: 11px; font-weight: 600; text-transform: uppercase; margin-top: 20px; margin-bottom: 5px; }

    /* Metrik Qutuları (Sağ Panel) */
    .metric-container {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .metric-title { color: #8b949e; font-size: 10px; font-weight: 600; margin: 0; }
    .metric-value { color: #58a6ff; font-size: 22px; font-weight: 700; margin: 0; }
    .status-text { color: #3fb950; font-size: 14px; font-weight: 600; }

    /* Proqress Bar Etiketləri */
    .progress-label { color: #8b949e; font-size: 11px; font-weight: 600; margin-top: 15px; margin-bottom: 5px; }
    
    /* Xəbərdarlıq Qutusu (Sarımtıl) */
    .warning-alert {
        background-color: rgba(187, 128, 9, 0.1);
        border: 1px solid rgba(187, 128, 9, 0.4);
        border-radius: 6px;
        padding: 12px;
        color: #d29922;
        font-size: 12px;
        margin-top: 20px;
    }

    /* Düymələr */
    .stButton>button { width: 100%; border-radius: 6px; font-weight: 600; }
    /* Zoom düyməsi - Mavi */
    div[data-testid="stSidebar"] .stButton>button { background-color: #238af1; color: white; border: none; }
    /* Report düyməsi - Ağ/Boz */
    .report-btn button { background: #ffffff !important; color: #0d1117 !important; border: none !important; }

    /* Live Monitoring Badge */
    .live-badge {
        background: #21262d;
        border: 1px solid #30363d;
        color: #f0f6fc;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        display: inline-flex;
        align-items: center;
        margin-bottom: 15px;
    }
    .red-dot { height: 8px; width: 8px; background-color: #f85149; border-radius: 50%; display: inline-block; margin-right: 8px; }

    /* File Uploader-ı sadələşdir */
    .stFileUploader { padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. PDF Funksiyası (Xətanın həlli buradadır: Bayt formatı)
def create_pdf_bytes(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(40, 10, "SATELLA MONITORING REPORT")
    pdf.ln(20)
    pdf.set_font("Arial", '', 12)
    pdf.cell(40, 10, f"Location: {lat}, {lon}")
    pdf.ln(10)
    pdf.cell(40, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    pdf.ln(10)
    pdf.cell(40, 10, "Result: 6 New structures detected.")
    
    # fpdf2-də 'S' (string/byte) formatında çıxış almaq
    try:
        pdf_output = pdf.output() # fpdf2 bayt qaytarır
        if isinstance(pdf_output, str):
            return pdf_output.encode('latin-1')
        return pdf_output
    except:
        # Alternativ olaraq io.BytesIO istifadəsi (ən etibarlı yol)
        buf = io.BytesIO()
        buf.write(pdf.output())
        return buf.getvalue()

# --- SOL PANEL (SIDEBAR) ---
with st.sidebar:
    st.markdown('### 🛰️ SATELLA<br><small style="color:#8b949e">CONSTRUCTION MONITORING</small>', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-label">🔍 AREA OF INTEREST</p>', unsafe_allow_html=True)
    col_lat, col_lon = st.columns(2)
    with col_lat:
        lat_val = st.text_input("Lat", "40.4093", label_visibility="collapsed")
    with col_lon:
        lon_val = st.text_input("Lon", "49.8671", label_visibility="collapsed")
    
    if st.button("Zoom to Coordinate"):
        st.session_state.lat = lat_val
        st.session_state.lon = lon_val

    st.markdown('<p class="sidebar-label">📁 RASTER DATA</p>', unsafe_allow_html=True)
    st.file_uploader("Baseline (T0).tif", type=["jpg", "png", "tif"], key="f1")
    st.file_uploader("Current (T1).tif", type=["jpg", "png", "tif"], key="f2")
    
    st.button("Run Change Detection", disabled=True)
    
    st.markdown("<br><br><br><br><br>")
    st.markdown('<p style="font-size:10px; color:#484f58">SATELLA v1.0 | Sentinel-2 & Azercosmos Integration. Developed for FHN Construction Safety Standards.</p>', unsafe_allow_html=True)

# --- ƏSAS HİSSƏ (MƏRKƏZ VƏ SAĞ) ---
col_main, col_metrics = st.columns([3, 1])

with col_main:
    st.markdown('<div class="live-badge"><span class="red-dot"></span> LIVE MONITORING</div>', unsafe_allow_html=True)
    
    curr_lat = float(st.session_state.get('lat', 40.4093))
    curr_lon = float(st.session_state.get('lon', 49.8671))
    
    # Xəritə (Dark rejim)
    m = folium.Map(location=[curr_lat, curr_lon], zoom_start=15, tiles="CartoDB dark_matter")
    folium.Marker([curr_lat, curr_lon]).add_to(m)
    folium_static(m, width=950, height=650)

with col_metrics:
    st.markdown('### 📊 System Metrics')
    
    # Metrik Qutuları
    st.markdown(f'''
        <div class="metric-container">
            <div><p class="metric-title">NEW STRUCTURES</p><p class="metric-value">6</p></div>
            <div style="text-align:right;"><p class="metric-title">STATUS</p><p class="status-text">✓ Ready</p></div>
        </div>
    ''', unsafe_allow_html=True)

    # Proqress Barlar (AI Studio Rəngləri ilə)
    st.markdown('<p class="progress-label">PRECISION (IOU)</p>', unsafe_allow_html=True)
    st.progress(0.92)
    st.caption("92%")

    st.markdown('<p class="progress-label">RECALL RATE</p>', unsafe_allow_html=True)
    # Yaşıl rəngli bar üçün CSS hack istifadə etmədən Streamlit-in öz rəngini veririk
    st.progress(0.88)
    st.caption("88%")

    st.markdown('<p class="progress-label">F1 PERFORMANCE</p>', unsafe_allow_html=True)
    st.progress(0.90)
    st.caption("90%")

    # Xəbərdarlıq Alert
    st.markdown('''
        <div class="warning-alert">
            <b>⚠️ Verification Required</b><br>
            Changes detected in sensitive zones. Generated reports must be submitted to FHN for field verification.
        </div>
    ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # PDF Düyməsi (Xətasız Versiya)
    pdf_data = create_pdf_bytes(curr_lat, curr_lon)
    st.markdown('<div class="report-btn">', unsafe_allow_html=True)
    st.download_button(
        label="📄 Generate FHN Report (PDF)",
        data=pdf_data,
        file_name="SATELLA_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<p class="sidebar-label" style="margin-top:30px">⚠ DETECTION HISTORY</p>', unsafe_allow_html=True)
    st.caption("No active detections in session.")
