
# SATELLA - Azerbaijan Construction Monitoring Platform

SATELLA is a specialized satellite monitoring system designed for the detection of illegal or undocumented building activities in Azerbaijan.

## Key Features
- **Sentinel-2 & Azercosmos Integration:** Powered by high-resolution satellite imagery.
- **Gemini Vision AI:** Advanced computer vision model for identifying structural changes over time.
- **FHN Ready:** Compliant with Azerbaijan's Ministry of Emergency Situations (FHN) construction reporting standards.
- **Interactive Map:** Real-time geospatial visualization using Leaflet.
- **Metrics Dashboard:** Precision, Recall, and F1-score tracking for AI model performance.

## Usage
1. Enter the Latitude and Longitude of the target area in Azerbaijan (e.g., Baku: 40.4093, 49.8671).
2. Upload a **Baseline** GeoTIFF/Image (older reference).
3. Upload a **Current** GeoTIFF/Image (recent status).
4. Click **Run Change Detection** to let Gemini analyze the differences.
5. Review detections on the map and generate an official PDF report.

## Technology Stack
- **Frontend:** React, TypeScript, Tailwind CSS
- **Maps:** Leaflet, React-Leaflet
- **AI Engine:** Google Gemini (Generative AI)
- **PDF Generation:** jsPDF
- **Icons:** Lucide React
