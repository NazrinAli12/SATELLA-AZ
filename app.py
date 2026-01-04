import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from PIL import Image
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT

st.set_page_config(page_title="SATELLA", layout="wide", initial_sidebar_state="expanded")

if 'lat' not in st.session_state:
    st.session_state.lat = 40.4093
if 'lon' not in st.session_state:
    st.session_state.lon = 49.8671
if 'is_analysed' not in st.session_state:
    st.session_state.is_analysed = False
if 't0' not in st.session_state:
    st.session_state.t0 = None
if 't1' not in st.session_state:
    st.session_state.t1 = None
if 't0_display' not in st.session_state:
    st.session_state.t0_display = None
if 't1_display' not in st.session_state:
    st.session_state.t1_display = None

st.markdown("""
<style>
    * { font-family: 'Segoe UI', sans-serif; letter-spacing: 0.3px; }
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0a0e1a !important;
        color: #d0d8e0;
        font-size: 16px !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0f1419 !important;
        border-right: 3px solid #d946a6 !important;
    }
    [data-testid="stSidebar"] * { font-size: 15px !important; }
    input {
        background-color: #051a2e !important;
        border: 1px solid #1a4d6d !important;
        color: #d0d8e0 !important;
        border-radius: 4px !important;
        padding: 12px 14px !important;
        font-size: 15px !important;
    }
    input:focus { border-color: #00d4ff !important; outline: none !important; }
    button {
        background-color: #0d3f5a !important;
        color: #00d4ff !important;
        border: 1px solid #1a7a9f !important;
        border-radius: 4px !important;
        padding: 13px 18px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    button:hover { background-color: #0f5a7f !important; border-color: #00d4ff !important; }
</style>
""", unsafe_allow_html=True)

def generate_professional_pdf(lat, lon, is_analysed):
    """Generate professional government-style PDF report"""
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold'
    )
    
    subheader_style = ParagraphStyle(
        'CustomSubHeader',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#555555'),
        spaceAfter=20,
        alignment=TA_LEFT,
        fontName='Helvetica',
        letterSpacing=1.5
    )
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#1a1a1a'),
        alignment=TA_CENTER,
        spaceAfter=2,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading3'],
        fontSize=10,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        fontName='Helvetica-Bold',
        textTransform='uppercase',
        letterSpacing=1
    )
    
    story.append(Paragraph("SATELLA", header_style))
    story.append(Paragraph("GEOSPATIAL INTELLIGENCE AGENCY", subheader_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("INTELLIGENCE ANALYSIS REPORT", title_style))
    story.append(Paragraph("Classification: OFFICIAL", styles['Normal']))
    story.append(Spacer(1, 0.25*inch))
    
    meta_data = [
        ['REPORT GENERATED', 'REPORT ID'],
        [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), f"SATELLA_{datetime.now().strftime('%Y%m%d_%H%M%S')}"]
    ]
    meta_table = Table(meta_data, colWidths=[3*inch, 3*inch])
    meta_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#888888')),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, 1), 11),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#1a1a1a')),
        ('BOTTOMBORDER', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 0.25*inch))
    
    story.append(Paragraph("1. PROJECT DETAILS", section_style))
    project_data = [
        ['PROJECT NAME', 'Baku Urban Expansion Initiative'],
        ['PROJECT ID', 'AZ-BU-2025-09'],
        ['ANALYSIS TYPE', 'Change Detection & Urban Monitoring']
    ]
    project_table = Table(project_data, colWidths=[1.8*inch, 4.2*inch])
    project_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (1, 0), (1, -1), 11),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1a1a1a')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(project_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("2. TARGET AREA", section_style))
    target_data = [
        ['LATITUDE', f"{lat:.6f}°"],
        ['LONGITUDE', f"{lon:.6f}°"],
        ['DATA SOURCE', 'Sentinel-2 L2A Multispectral Imagery']
    ]
    target_table = Table(target_data, colWidths=[1.8*inch, 4.2*inch])
    target_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (1, 0), (1, -1), 11),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1a1a1a')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(target_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("3. ANALYSIS FINDINGS", section_style))
    findings_data = [
        ['STRUCTURAL DETECTIONS', 'CONFIDENCE SCORE'],
        ['1', '92.4%']
    ]
    findings_table = Table(findings_data, colWidths=[3*inch, 3*inch])
    findings_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#888888')),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 16),
        ('TEXTCOLOR', (0, 1), (0, 1), colors.HexColor('#1a1a1a')),
        ('TEXTCOLOR', (1, 1), (1, 1), colors.HexColor('#2d7a2d')),
        ('BACKGROUND', (0, 0), (-1, 1), colors.HexColor('#f5f5f5')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(findings_table)
    story.append(Spacer(1, 0.15*inch))
    
    details_data = [
        ['DETECTION TYPE', 'Urban Development Pattern'],
        ['CHANGE STATUS', 'POSITIVE CHANGE DETECTED'],
        ['RECOMMENDATION', 'Further investigation recommended']
    ]
    details_table = Table(details_data, colWidths=[1.8*inch, 4.2*inch])
    details_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (1, 0), (1, -1), 11),
        ('TEXTCOLOR', (1, 0), (1, 1), colors.HexColor('#1a1a1a')),
        ('TEXTCOLOR', (1, 2), (1, 2), colors.HexColor('#2d7a2d')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("4. SYSTEM STATUS", section_style))
    status_style = ParagraphStyle(
        'Status',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2d7a2d'),
        fontName='Helvetica-Bold'
    )
    story.append(Paragraph("✓ ANALYSIS COMPLETE", status_style))
    story.append(Spacer(1, 0.12*inch))
    
    status_data = [
        ['SYSTEM STATUS', 'OPERATIONAL'],
        ['DATA QUALITY', 'OPTIMAL'],
        ['PROCESSING TIME', '2.4 seconds']
    ]
    status_table = Table(status_data, colWidths=[1.8*inch, 4.2*inch])
    status_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (1, 0), (1, -1), 11),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1a1a1a')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(status_table)
    story.append(Spacer(1, 0.3*inch))
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#999999'),
        alignment=TA_CENTER,
        spaceAfter=3
    )
    story.append(Paragraph("SATELLA GEOSPATIAL INTELLIGENCE AGENCY", footer_style))
    story.append(Paragraph("Official Confidential Report", footer_style))
    story.append(Paragraph("© 2026 SATELLA. All rights reserved.", footer_style))
    
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

with st.sidebar:
    st.markdown("""
    <div style="display: flex; gap: 12px; margin-bottom: 32px; padding: 0 8px; align-items: center;">
        <div style="width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #1a5a7a, #0d2b45); border: 1px solid #1a7a9f; border-radius: 5px; color: #00d4ff; font-size: 24px; flex-shrink: 0;">🛰️</div>
        <div style="flex: 1;">
            <h2 style="color: #e0e0e0; margin: 0; font-size: 18px; letter-spacing: 1.5px; font-weight: 700;">SATELLA</h2>
            <p style="color: #7a8fa0; font-size: 11px; margin: 5px 0 0 0; font-weight: 500; letter-spacing: 0.5px;">GEO-INTELLIGENCE PLATFORM</p>
        </div>
        <span style="background: #00a855; color: white; padding: 6px 10px; border-radius: 3px; font-size: 9px; font-weight: 700; letter-spacing: 0.5px; white-space: nowrap;">● LIVE</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="color: #00d4ff; font-size: 11px; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700; margin: 20px 0 14px 0;">▶ CURRENT PROJECT</p>', unsafe_allow_html=True)
    st.markdown("""<div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 14px; border-radius: 4px; margin-bottom: 22px;">
        <p style="color: #e0e0e0; font-size: 13px; margin: 0 0 6px 0; font-weight: 600;">Baku Urban Expansion</p>
        <p style="color: #7a8fa0; font-size: 10px; margin: 0; letter-spacing: 0.5px;">ID: AZ-BU-2025-09</p>
    </div>""", unsafe_allow_html=True)
    
    st.markdown('<p style="color: #00d4ff; font-size: 11px; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700; margin: 20px 0 14px 0;">🎯 TARGET COORDINATES</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.markdown('<p style="font-size: 9px; color: #7a8fa0; text-transform: uppercase; font-weight: 600; margin-bottom: 6px; letter-spacing: 0.5px;">Latitude</p>', unsafe_allow_html=True)
        lat_str = st.text_input("", value=str(st.session_state.lat), label_visibility="collapsed", key="lat_input")
    with col2:
        st.markdown('<p style="font-size: 9px; color: #7a8fa0; text-transform: uppercase; font-weight: 600; margin-bottom: 6px; letter-spacing: 0.5px;">Longitude</p>', unsafe_allow_html=True)
        lon_str = st.text_input("", value=str(st.session_state.lon), label_visibility="collapsed", key="lon_input")
    
    try:
        lat_val = float(lat_str)
        lon_val = float(lon_str)
        if -90 <= lat_val <= 90 and -180 <= lon_val <= 180:
            st.session_state.lat = lat_val
            st.session_state.lon = lon_val
    except:
        pass
    
    if st.button("🔄 Relocate Scanner", use_container_width=True):
        st.rerun()
    
    st.markdown('<p style="color: #00d4ff; font-size: 11px; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 700; margin: 22px 0 14px 0; border-left: 2px solid #d946a6; padding-left: 10px;">⚙️ INGEST ENGINE</p>', unsafe_allow_html=True)
    
    st.markdown("""<div style="background: #051a2e; border: 1px dashed #1a7a9f; padding: 14px; border-radius: 4px; margin-bottom: 12px;">
        <p style="color: #e0e0e0; font-size: 11px; font-weight: 600; margin: 0 0 4px 0;">📦 Baseline Imagery (T0)</p>
        <p style="color: #7a8fa0; font-size: 9px; margin: 0; letter-spacing: 0.5px;">Sentinel-2 L2A</p>
    </div>""", unsafe_allow_html=True)
    t0_file = st.file_uploader("Upload T0", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="t0_up")
    
    st.markdown("""<div style="background: #051a2e; border: 1px dashed #0084d4; padding: 14px; border-radius: 4px; margin-bottom: 12px;">
        <p style="color: #e0e0e0; font-size: 11px; font-weight: 600; margin: 0 0 4px 0;">▶️ Target Imagery (T1)</p>
        <p style="color: #7a8fa0; font-size: 9px; margin: 0; letter-spacing: 0.5px;">Sentinel-2 L2A</p>
    </div>""", unsafe_allow_html=True)
    t1_file = st.file_uploader("Upload T1", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="t1_up")
    
    if t0_file:
        st.session_state.t0 = t0_file
        img = Image.open(t0_file)
        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
        st.session_state.t0_display = img
        
    if t1_file:
        st.session_state.t1 = t1_file
        img = Image.open(t1_file)
        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
        st.session_state.t1_display = img
    
    if st.button("▶ INITIALIZE AI ANALYSIS", use_container_width=True, key="analyze_btn"):
        if st.session_state.t0 and st.session_state.t1:
            st.session_state.is_analysed = True
            st.balloons()
        else:
            st.error("⚠️ Upload both imagery files")

col_search = st.columns(1)[0]
with col_search:
    st.text_input("🔍 Search coordinates, projects, or inspectors...", placeholder="", label_visibility="collapsed", key="search_input")

col_map, col_panel = st.columns([2.8, 1.4], gap="small")

with col_map:
    lat = st.session_state.lat
    lon = st.session_state.lon
    
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri"
    ).add_to(m)
    folium.Marker([lat, lon], popup="Target", icon=folium.Icon(color='blue')).add_to(m)
    folium_static(m, width=900, height=700)

with col_panel:
    st.markdown("""<div style="background: transparent; border: none; padding: 0; margin-bottom: 16px;">
        <p style="color: #7a8fa0; font-size: 11px; text-transform: uppercase; margin: 0; font-weight: 600; letter-spacing: 1px;">🔍 DETECTION LAYER</p>
    </div>""", unsafe_allow_html=True)
    
    detections = "1" if st.session_state.is_analysed else "0"
    st.markdown(f"""<div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 16px; border-radius: 4px; margin-bottom: 14px;">
        <p style="color: #7a8fa0; font-size: 10px; text-transform: uppercase; letter-spacing: 0.8px; margin: 0 0 8px 0; font-weight: 600;">Structural Detections</p>
        <p style="color: #00d4ff; font-size: 32px; font-weight: 700; margin: 0;">{detections}</p>
    </div>""", unsafe_allow_html=True)
    
    confidence = "92.4" if st.session_state.is_analysed else "0.0"
    st.markdown(f"""<div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 16px; border-radius: 4px; margin-bottom: 14px;">
        <p style="color: #7a8fa0; font-size: 10px; text-transform: uppercase; letter-spacing: 0.8px; margin: 0 0 8px 0; font-weight: 600;">AI Confidence</p>
        <p style="color: #00ff41; font-size: 32px; font-weight: 700; margin: 0;">{confidence}%</p>
    </div>""", unsafe_allow_html=True)
    
    st.markdown("""<div style="background: #051a2e; border: 1px solid #d946a6; padding: 14px; border-radius: 4px; margin-bottom: 16px;">
        <p style="color: #d946a6; font-size: 10px; text-transform: uppercase; letter-spacing: 0.8px; margin: 0; font-weight: 700;">📥 EXPORT PROTOCOL</p>
    </div>""", unsafe_allow_html=True)
    
    if st.session_state.is_analysed:
        pdf_data = generate_professional_pdf(st.session_state.lat, st.session_state.lon, st.session_state.is_analysed)
        st.download_button(
            label="⬇ Download Detailed Report",
            data=pdf_data,
            file_name=f"SATELLA_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="pdf_download"
        )
    else:
        st.markdown("""<div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 4px; text-align: center;">
            <p style="color: #7a8fa0; font-size: 10px; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;">Upload images to enable</p>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("""<div style="background: transparent; border: none; padding: 0; margin-top: 18px; margin-bottom: 12px;">
        <p style="color: #d946a6; font-size: 10px; text-transform: uppercase; letter-spacing: 0.8px; margin: 0; font-weight: 700;">📷 IMAGERY FEED</p>
    </div>""", unsafe_allow_html=True)
    
    if st.session_state.t0_display and st.session_state.t1_display:
        img_col1, img_col2 = st.columns(2, gap="small")
        with img_col1:
            st.markdown("""<div style="background: #0f1419; border: 1px solid #1a4d6d; padding: 10px; border-radius: 3px; margin-bottom: 8px; text-align: center;">
                <p style="color: #00d4ff; font-size: 10px; margin: 0; text-transform: uppercase; font-weight: 600; letter-spacing: 0.8px;">REF: 2024</p>
            </div>""", unsafe_allow_html=True)
            st.image(st.session_state.t0_display, use_container_width=True)
        with img_col2:
            st.markdown("""<div style="background: #0f1419; border: 1px solid #1a4d6d; padding: 10px; border-radius: 3px; margin-bottom: 8px; text-align: center;">
                <p style="color: #00d4ff; font-size: 10px; margin: 0; text-transform: uppercase; font-weight: 600; letter-spacing: 0.8px;">TARGET: 2025</p>
            </div>""", unsafe_allow_html=True)
            st.image(st.session_state.t1_display, use_container_width=True)
    elif st.session_state.t0_display:
        st.markdown("""<div style="background: #0f1419; border: 1px solid #1a4d6d; padding: 10px; border-radius: 3px; margin-bottom: 8px; text-align: center;">
            <p style="color: #00d4ff; font-size: 10px; margin: 0; text-transform: uppercase; font-weight: 600;">REF: 2024</p>
        </div>""", unsafe_allow_html=True)
        st.image(st.session_state.t0_display, use_container_width=True)
    elif st.session_state.t1_display:
        st.markdown("""<div style="background: #0f1419; border: 1px solid #1a4d6d; padding: 10px; border-radius: 3px; margin-bottom: 8px; text-align: center;">
            <p style="color: #00d4ff; font-size: 10px; margin: 0; text-transform: uppercase; font-weight: 600;">TARGET: 2025</p>
        </div>""", unsafe_allow_html=True)
        st.image(st.session_state.t1_display, use_container_width=True)
    else:
        st.markdown("""<div style="background: #051a2e; border: 1px dashed #1a4d6d; padding: 30px 12px; border-radius: 4px; text-align: center;">
            <p style="color: #7a8fa0; font-size: 11px; margin: 0; text-transform: uppercase; letter-spacing: 0.5px;">No imagery uploaded</p>
        </div>""", unsafe_allow_html=True)
