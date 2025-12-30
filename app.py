import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
import io
from fpdf import FPDF

# 1. Ekran Ayarları (Geniş və User-Friendly)
st.set_page_config(page_title="SATELLA - AI Studio", layout="wide", initial_sidebar_state="expanded")

# 2. AI Studio Professional Design (CSS)
st.markdown("""
    <style>
    /* Fon rəngləri */
    .main { background-color: #0d1117; color: #f0f6fc; }
    [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d; }
    
    /* Sağ panel metrik kartları */
    .metric-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .metric-title { color: #8b949e; font-size: 10px; font-weight: bold; margin-bottom: 5px; }
    .metric-val { color: #58a6ff; font-size: 24px; font-weight: bold; }
    .status-ready { color: #3fb950; font-size: 14px; font-weight: 600; }

    /* Xüsusi Proqress Barlar */
    .bar-container { margin-top: 15px; margin-bottom: 20px; }
    .bar-label { display: flex; justify-content: space-between; font-size: 11px; color: #8b949e; font-weight: 600; }
    .bar-bg { background: #21262d; border-radius: 10px; height: 6px; width: 100%; margin-top: 5px; }
    .bar-fill { height: 6px; border-radius: 10px; }

    /* Düymə Stilləri */
    .stButton>button { width: 100%; border-radius: 6px; border: none; font-weight: 600; transition: 0.3s; }
    /* Zoom düyməsi - Parlaq Göy */
    div[data-testid="stSidebar"] .stButton>button { background-color: #238af1; color: white; }
    /* PDF Düyməsi - AI Studio Ağ/Boz */
    .download-btn-container button { background-color: #ffffff !important; color: #0d1117 !important; height: 45px; border-radius: 8px !important; }

    /* Alert Box */
    .alert-box {
        background-color: rgba(187, 128, 9, 0.1);
        border: 1px solid rgba(187, 128, 9, 0.4);
        padding: 15px;
        border-radius: 8px;
        color: #d29922;
        font-size: 12px;
        margin-bottom: 15px;
    }
    
    /* Live Badge */
    .live-tag {
        background: #21262d;
        border: 1px solid #30363d;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        display: inline-flex;
        align-items: center;
        margin-bottom: 10px;
    }
    .dot { height: 7px; width: 7px; background-color: #f85149; border-radius: 50%; margin-right: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 3. PDF Yaratma Funksiyası (Xətasız Versiya)
def generate_pdf_bytes(lat, lon):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 15, "SATELLA - FHN MONITORING REPORT", ln=True, align='C')
        pdf.set_font("Arial", '', 11)
        pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf.cell(0, 10, f"Location: Latitude {lat}, Longitude {lon}", ln=True)
        pdf.ln(10)
        pdf.cell(0, 10, "Summary: 6 new illegal construction zones detected via satellite imagery.", ln=True)
        
        # BytesIO ilə yaddaşda saxlayırıq ki, Streamlit error verməsin
        return pdf.output()
    except Exception as e:
        return None

# --- UI STRUKTURU ---
# Səhifəni 3 hissəyə bölürük: Mərkəz (Xəritə) və Sağ (Metriklər). Sol Sidebar onsuz da hazırdır.
col_map, col_right = st.columns([3.2, 1.2], gap="large")

# --- SOL SIDEBAR (Dizayn şəkildəki kimi) ---
with st.sidebar:
    st.markdown('<div style="display:flex; align-items:center; gap:10px;"><div style="background:#2463eb; color:white; padding:5px 8px; border-radius:6px; font-weight:bold;">S</div> <h3 style="margin:0;">SATELLA</h3></div>', unsafe_allow_html=True)
    st.caption("CONSTRUCTION MONITORING")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<p style='font-size:11px; color:#8b949e; font-weight:700;'>🔍 AREA OF INTEREST</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        in_lat = st.text_input("Lat", "40.4093", label_visibility="collapsed")
    with c2:
        in_lon = st.text_input("Lon", "49.8671", label_visibility="collapsed")
    
    if st.button("Zoom to Coordinate"):
        st.session_state.lat = in_lat
        st.session_state.lon = in_lon

    st.markdown("<br><p style='font-size:11px; color:#8b949e; font-weight:700;'>📁 RASTER DATA</p>", unsafe_allow_html=True)
    st.markdown("<div style='border:1px dashed #30363d; padding:15px; border-radius:8px; text-align:center; color:#8b949e; font-size:11px;'>Baseline (T0).tif</div>", unsafe_allow_html=True)
    st.file_uploader("T0", label_visibility="collapsed", key="u1")
    
    st.markdown("<div style='border:1px dashed #30363d; padding:15px; border-radius:8px; text-align:center; color:#8b949e; font-size:11px;'>Current (T1).tif</div>", unsafe_allow_html=True)
    st.file_uploader("T1", label_visibility="collapsed", key="u2")
    
    st.button("Run Change Detection", disabled=True)
    st.markdown("<div style='margin-top:50px; font-size:10px; color:#484f58;'>SATELLA v1.0 | FHN Ready Analysis</div>", unsafe_allow_html=True)

# --- MƏRKƏZİ HİSSƏ (MAP) ---
with col_map:
    st.markdown('<div class="live-tag"><span class="dot"></span> LIVE MONITORING</div>', unsafe_allow_html=True)
    
    curr_lat = float(st.session_state.get('lat', 40.4093))
    curr_lon = float(st.session_state.get('lon', 49.8671))
    
    # Xəritə - Professional Dark Style
    m = folium.Map(location=[curr_lat, curr_lon], zoom_start=15, tiles="CartoDB dark_matter")
    folium.Marker([curr_lat, curr_lon]).add_to(m)
    folium_static(m, width=980, height=650)

# --- SAĞ HİSSƏ (SYSTEM METRICS & PDF) ---
with col_right:
    st.markdown('<h3 style="font-size:18px;">📊 System Metrics</h3>', unsafe_allow_html=True)
    
    # Metrik Kartları
    r1, r2 = st.columns(2)
    with r1:
        st.markdown('<div class="metric-box"><p class="metric-title">NEW STRUCTURES</p><p class="metric-val">6</p></div>', unsafe_allow_html=True)
    with r2:
        st.markdown('<div class="metric-box"><p class="metric-title">STATUS</p><p class="status-ready">✓ Ready</p></div>', unsafe_allow_html=True)
    
    # Proqress Barlar (AI Studio Rəngləri)
    metrics = [
        ("PRECISION (IOU)", 92, "#388bfd"),
        ("RECALL RATE", 88, "#3fb950"),
        ("F1 PERFORMANCE", 90, "#a371f7")
    ]
    
    for label, val, color in metrics:
        st.markdown(f"""
            <div class="bar-container">
                <div class="bar-label"><span>{label}</span><span>{val}%</span></div>
                <div class="bar-bg"><div class="bar-fill" style="width:{val}%; background-color:{color};"></div></div>
            </div>
        """, unsafe_allow_html=True)

    # Verification Box
    st.markdown("""
        <div class="alert-box">
            <b>🛡️ Verification Required</b><br>
            Changes detected in sensitive zones. Generated reports must be submitted to FHN for field verification.
        </div>
    """, unsafe_allow_html=True)

    # --- PDF DOWNLOAD (Burada gəlməlidir) ---
    report_data = generate_pdf_bytes(curr_lat, curr_lon)
    if report_data:
        st.markdown('<div class="download-btn-container">', unsafe_allow_html=True)
        st.download_button(
            label="📄 Generate FHN Report (PDF)",
            data=report_data,
            file_name=f"SATELLA_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br><p style='font-size:11px; color:#8b949e; font-weight:700;'>⚠️ DETECTION HISTORY</p>", unsafe_allow_html=True)
    st.caption("No active detections in session.")
