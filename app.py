import streamlit as st
import folium
from streamlit_folium import folium_static
import io

# 1. Page Config
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# 2. UI Styling (Exact AI Studio)
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #0b0d0e !important;
        overflow: hidden !important;
    }
    [data-testid="stHeader"] { display: none; }
    .block-container { padding: 0 !important; }

    /* Sağ Panel */
    .right-panel {
        position: fixed; right: 0; top: 0; width: 320px;
        height: 100vh; background-color: #111418;
        border-left: 1px solid #2d333b; padding: 25px;
        z-index: 1000; color: white;
    }

    /* Sol Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
        overflow: hidden !important;
    }

    /* Xəritə Sahəsi */
    .map-frame { margin-right: 320px; height: 100vh; }
    
    /* Düymə stili */
    div.stButton > button {
        background-color: #1a73e8 !important; color: white !important;
        border-radius: 20px !important; border: none !important;
        width: 100% !important; font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Koordinat İdarəetməsi (Session State)
# Sənin verdiyin koordinatları default edirik
if 'lat' not in st.session_state:
    st.session_state.lat = 40.46102314072054
if 'lon' not in st.session_state:
    st.session_state.lon = 49.88989799049365

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:white; font-size:22px;'>🛰️ SATELLA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9aa0a6; font-size:11px;'>INPUT COORDINATES</p>", unsafe_allow_html=True)
    
    # Text inputlar birbaşa session_state-ə bağlı deyil, düymə ilə yenilənir
    in_lat = st.text_input("Lat", value=str(st.session_state.lat))
    in_lon = st.text_input("Lon", value=str(st.session_state.lon))
    
    if st.button("RUN ANALYSIS"):
        st.session_state.lat = float(in_lat)
        st.session_state.lon = float(in_lon)
        # st.rerun() lazım deyil, düymə onsuz da səhifəni tətikləyir

    st.divider()
    st.file_uploader("Upload Image", label_visibility="collapsed")

# --- SAĞ PANEL ---
st.markdown(f"""
    <div class="right-panel">
        <p style='font-size:18px; font-weight:500; margin-bottom:20px;'>Detection Data</p>
        <div style='background:#1a1f24; border:1px solid #3c4043; padding:15px; border-radius:8px; margin-bottom:15px'>
            <p style='color:#9aa0a6; font-size:10px; margin:0'>TARGET AREA</p>
            <p style='color:#ffffff; font-size:14px; margin:5px 0 0 0'>{st.session_state.lat:.6f}, {st.session_state.lon:.6f}</p>
        </div>
        <div style='background:#1a1f24; border:1px solid #3c4043; padding:15px; border-radius:8px;'>
            <p style='color:#9aa0a6; font-size:10px; margin:0'>NEW STRUCTURES</p>
            <p style='color:#ffffff; font-size:24px; margin:5px 0 0 0; font-weight:bold'>6</p>
        </div>
        <br>
        <p style='color:#3fb950; font-size:12px'>● System Online</p>
    </div>
""", unsafe_allow_html=True)

# --- ANA EKRAN (XƏRİTƏ) ---
# Xəritəni hər dəfə session_state-dəki yeni koordinatla yaradırıq
m = folium.Map(
    location=[st.session_state.lat, st.session_state.lon],
    zoom_start=18,
    tiles="CartoDB dark_matter",
    zoom_control=False
)

# BURA ÇOX VACİBDİR: Markeri birbaşa həmin yerə qoyur
folium.Marker(
    [st.session_state.lat, st.session_state.lon],
    tooltip="Analysis Center",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Dairəvi işarə
folium.Circle(
    [st.session_state.lat, st.session_state.lon],
    radius=50,
    color="#1a73e8",
    fill=True,
    fill_opacity=0.2
).add_to(m)

# Xəritəni göstər
with st.container():
    st.markdown('<div class="map-frame">', unsafe_allow_html=True)
    folium_static(m, width=1250, height=950)
    st.markdown('</div>', unsafe_allow_html=True)
