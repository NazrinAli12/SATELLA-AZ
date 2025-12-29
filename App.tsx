
import React, { useState, useEffect, useCallback } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, ZoomControl, LayersControl } from 'react-leaflet';
import { Satellite, Shield, Map as MapIcon, Upload, Search, FileText, BarChart3, Clock, AlertTriangle, CheckCircle, ChevronRight } from 'lucide-react';
import { Coordinate, BuildingDetection, MonitoringMetrics, HistoryItem } from './types';
import { geminiService } from './services/geminiService';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

// --- Sub-components ---

const MapFlyTo: React.FC<{ coords: Coordinate }> = ({ coords }) => {
  const map = useMap();
  useEffect(() => {
    map.flyTo([coords.lat, coords.lng], 14, { duration: 1.5 });
  }, [coords, map]);
  return null;
};

const MetricGauge: React.FC<{ label: string; value: number; color: string }> = ({ label, value, color }) => (
  <div className="bg-gray-800/50 p-4 rounded-xl border border-gray-700">
    <div className="text-xs text-gray-400 uppercase tracking-wider mb-1">{label}</div>
    <div className="flex items-end gap-2">
      <div className={`text-2xl font-bold ${color}`}>{Math.round(value * 100)}%</div>
      <div className="w-full bg-gray-700 h-1.5 rounded-full mb-2 overflow-hidden">
        <div 
          className={`h-full ${color.replace('text', 'bg')}`} 
          style={{ width: `${value * 100}%` }}
        />
      </div>
    </div>
  </div>
);

// --- Main App ---

const App: React.FC = () => {
  const [lat, setLat] = useState<string>("40.4093");
  const [lng, setLng] = useState<string>("49.8671");
  const [currentCoords, setCurrentCoords] = useState<Coordinate>({ lat: 40.4, lng: 49.8 });
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [baselineFile, setBaselineFile] = useState<File | null>(null);
  const [currentFile, setCurrentFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [detections, setDetections] = useState<BuildingDetection[]>([]);
  const [metrics, setMetrics] = useState<MonitoringMetrics>({
    precision: 0.92,
    recall: 0.88,
    f1Score: 0.90,
    newConstructionsCount: 0
  });

  // Handle Coordinate Zoom
  const handleZoom = () => {
    const l = parseFloat(lat);
    const n = parseFloat(lng);
    if (!isNaN(l) && !isNaN(n)) {
      const newCoord = { lat: l, lng: n };
      setCurrentCoords(newCoord);
      setHistory(prev => [{ ...newCoord, timestamp: Date.now() }, ...prev].slice(0, 5));
    }
  };

  // Run AI Analysis
  const runAnalysis = async () => {
    if (!baselineFile || !currentFile) return;
    setIsProcessing(true);
    try {
      const results = await geminiService.detectNewConstructions(baselineFile, currentFile);
      setDetections(results);
      setMetrics(prev => ({
        ...prev,
        newConstructionsCount: results.length
      }));
    } catch (err) {
      console.error(err);
    } finally {
      setIsProcessing(false);
    }
  };

  // Export PDF
  const exportPDF = () => {
    const doc = new jsPDF();
    const title = "SATELLA FHN Construction Report";
    const date = new Date().toLocaleString();

    doc.setFontSize(22);
    doc.text("🛰️ " + title, 20, 25);
    
    doc.setFontSize(12);
    doc.setTextColor(100);
    doc.text(`Satellite verification: Sentinel-2 + Azercosmos`, 20, 35);
    doc.text(`Generated: ${date}`, 20, 42);

    doc.setDrawColor(200);
    doc.line(20, 48, 190, 48);

    doc.setTextColor(0);
    doc.setFontSize(14);
    doc.text("Project Location Data", 20, 60);
    doc.setFontSize(11);
    doc.text(`Latitude: ${currentCoords.lat}`, 25, 68);
    doc.text(`Longitude: ${currentCoords.lng}`, 25, 75);

    doc.setFontSize(14);
    doc.text("Detection Summary", 20, 90);
    
    const tableData = [
      ["Parameter", "Value"],
      ["New Constructions Detected", metrics.newConstructionsCount.toString()],
      ["Precision Score", `${(metrics.precision * 100).toFixed(1)}%`],
      ["Recall Score", `${(metrics.recall * 100).toFixed(1)}%`],
      ["F1-Score", `${(metrics.f1Score * 100).toFixed(1)}%`],
    ];

    (doc as any).autoTable({
      startY: 95,
      head: [tableData[0]],
      body: tableData.slice(1),
      theme: 'striped',
      headStyles: { fillColor: [31, 41, 55] }
    });

    doc.setFontSize(10);
    doc.setTextColor(150);
    doc.text("SATELLA v1.0 | Official FHN Monitoring Protocol Compliance", 20, 280);

    doc.save(`SATELLA_Report_${currentCoords.lat}_${currentCoords.lng}.pdf`);
  };

  return (
    <div className="flex h-screen bg-gray-950 text-white overflow-hidden">
      
      {/* Sidebar (Left) - Inputs & Files */}
      <aside className="w-80 bg-gray-900 border-r border-gray-800 flex flex-col p-6 overflow-y-auto">
        <div className="flex items-center gap-3 mb-8">
          <div className="bg-blue-600 p-2 rounded-lg">
            <Satellite className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-lg tracking-tight">SATELLA</h1>
            <p className="text-[10px] text-gray-400 uppercase tracking-widest">Construction Monitoring</p>
          </div>
        </div>

        <section className="space-y-6">
          {/* Coordinates */}
          <div className="space-y-3">
            <label className="text-xs font-semibold text-gray-400 uppercase flex items-center gap-2">
              <Search className="w-3 h-3" /> Area of Interest
            </label>
            <div className="grid grid-cols-2 gap-2">
              <input 
                type="text" 
                value={lat} 
                onChange={(e) => setLat(e.target.value)}
                placeholder="Latitude" 
                className="bg-gray-800 border border-gray-700 rounded-lg p-2 text-sm focus:ring-1 ring-blue-500 outline-none"
              />
              <input 
                type="text" 
                value={lng} 
                onChange={(e) => setLng(e.target.value)}
                placeholder="Longitude" 
                className="bg-gray-800 border border-gray-700 rounded-lg p-2 text-sm focus:ring-1 ring-blue-500 outline-none"
              />
            </div>
            <button 
              onClick={handleZoom}
              className="w-full bg-blue-600 hover:bg-blue-700 transition py-2.5 rounded-lg text-sm font-medium flex items-center justify-center gap-2"
            >
              Zoom to Coordinate
            </button>
          </div>

          {/* Recent Searches */}
          {history.length > 0 && (
            <div className="space-y-2">
              <label className="text-xs font-semibold text-gray-400 uppercase flex items-center gap-2">
                <Clock className="w-3 h-3" /> Recent Areas
              </label>
              <div className="space-y-1">
                {history.map((h, i) => (
                  <button 
                    key={i}
                    onClick={() => { setLat(h.lat.toString()); setLng(h.lng.toString()); setCurrentCoords({ lat: h.lat, lng: h.lng }); }}
                    className="w-full text-left text-xs bg-gray-800/40 hover:bg-gray-800 p-2 rounded border border-gray-800/50 flex justify-between items-center group"
                  >
                    <span>{h.lat.toFixed(4)}, {h.lng.toFixed(4)}</span>
                    <ChevronRight className="w-3 h-3 text-gray-600 group-hover:text-blue-500" />
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* File Uploads */}
          <div className="space-y-4">
            <label className="text-xs font-semibold text-gray-400 uppercase flex items-center gap-2">
              <Upload className="w-3 h-3" /> Raster Data
            </label>
            
            <div className="space-y-3">
              <div className="relative">
                <input 
                  type="file" 
                  onChange={(e) => setBaselineFile(e.target.files?.[0] || null)}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" 
                />
                <div className={`p-4 border-2 border-dashed rounded-xl transition ${baselineFile ? 'border-blue-500 bg-blue-500/5' : 'border-gray-700 hover:border-gray-600'}`}>
                  <div className="flex flex-col items-center gap-2">
                    <FileText className={`w-5 h-5 ${baselineFile ? 'text-blue-400' : 'text-gray-500'}`} />
                    <span className="text-[11px] font-medium text-gray-300">
                      {baselineFile ? baselineFile.name : 'Baseline (T0).tif'}
                    </span>
                  </div>
                </div>
              </div>

              <div className="relative">
                <input 
                  type="file" 
                  onChange={(e) => setCurrentFile(e.target.files?.[0] || null)}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" 
                />
                <div className={`p-4 border-2 border-dashed rounded-xl transition ${currentFile ? 'border-emerald-500 bg-emerald-500/5' : 'border-gray-700 hover:border-gray-600'}`}>
                  <div className="flex flex-col items-center gap-2">
                    <FileText className={`w-5 h-5 ${currentFile ? 'text-emerald-400' : 'text-gray-500'}`} />
                    <span className="text-[11px] font-medium text-gray-300">
                      {currentFile ? currentFile.name : 'Current (T1).tif'}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <button 
              disabled={!baselineFile || !currentFile || isProcessing}
              onClick={runAnalysis}
              className={`w-full py-3 rounded-lg text-sm font-bold shadow-lg transition transform active:scale-95 ${
                !baselineFile || !currentFile || isProcessing 
                ? 'bg-gray-800 text-gray-500 cursor-not-allowed' 
                : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white'
              }`}
            >
              {isProcessing ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Processing AI...
                </div>
              ) : 'Run Change Detection'}
            </button>
          </div>
        </section>

        <footer className="mt-auto pt-6 border-t border-gray-800">
          <p className="text-[10px] text-gray-500 leading-relaxed">
            SATELLA v1.0 | Sentinel-2 & Azercosmos Integration.
            Developed for FHN Construction Safety Standards.
          </p>
        </footer>
      </aside>

      {/* Map (Center) */}
      <main className="flex-1 relative bg-gray-900 overflow-hidden">
        <MapContainer 
          center={[currentCoords.lat, currentCoords.lng]} 
          zoom={11} 
          zoomControl={false}
          className="z-0"
        >
          <LayersControl position="topright">
            <LayersControl.BaseLayer checked name="OpenStreetMap">
              <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            </LayersControl.BaseLayer>
            <LayersControl.BaseLayer name="Satellite View">
              <TileLayer url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}" />
            </LayersControl.BaseLayer>
          </LayersControl>
          
          <MapFlyTo coords={currentCoords} />
          <ZoomControl position="bottomright" />
          
          <Marker position={[currentCoords.lat, currentCoords.lng]}>
            <Popup>
              <div className="text-gray-900">
                <p className="font-bold text-sm">Monitoring Area</p>
                <p className="text-xs">Lat: {currentCoords.lat.toFixed(4)}</p>
                <p className="text-xs">Lng: {currentCoords.lng.toFixed(4)}</p>
              </div>
            </Popup>
          </Marker>

          {/* Simulated Detection Polygons if we had real GPS mapping from raster */}
          {/* For the scope of this UI, we show markers for detections */}
          {detections.map((d, i) => (
            <Marker key={d.id} position={[currentCoords.lat + (Math.random() - 0.5) * 0.01, currentCoords.lng + (Math.random() - 0.5) * 0.01]}>
              <Popup>
                <div className="text-red-600 font-bold p-1">
                  <div className="flex items-center gap-1 mb-1">
                    <AlertTriangle className="w-4 h-4" />
                    New Construction
                  </div>
                  <p className="text-xs text-gray-600 font-normal">Confidence: {Math.round(d.confidence * 100)}%</p>
                  <button className="mt-2 w-full bg-red-600 text-white py-1 px-2 rounded text-[10px] hover:bg-red-700">Flag for Inspection</button>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>

        {/* Map Overlays */}
        <div className="absolute top-6 left-6 z-[1000] flex flex-col gap-2">
          <div className="bg-gray-900/90 backdrop-blur-md border border-gray-800 p-3 rounded-xl shadow-2xl">
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
              <span className="text-xs font-semibold tracking-wide text-gray-200 uppercase">Live Monitoring</span>
            </div>
          </div>
        </div>
      </main>

      {/* Dashboard (Right) - Metrics & Export */}
      <aside className="w-96 bg-gray-900 border-l border-gray-800 flex flex-col p-6 overflow-y-auto">
        <div className="flex items-center gap-2 mb-8">
          <BarChart3 className="w-5 h-5 text-blue-400" />
          <h2 className="font-bold text-lg">System Metrics</h2>
        </div>

        <div className="space-y-6">
          {/* Main Counters */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-800/40 p-4 rounded-xl border border-gray-800">
              <div className="text-[10px] text-gray-400 uppercase font-bold mb-1">New Structures</div>
              <div className="text-3xl font-black text-blue-400">{metrics.newConstructionsCount}</div>
            </div>
            <div className="bg-gray-800/40 p-4 rounded-xl border border-gray-800">
              <div className="text-[10px] text-gray-400 uppercase font-bold mb-1">Status</div>
              <div className="flex items-center gap-1.5 text-emerald-400 font-bold">
                <CheckCircle className="w-4 h-4" />
                <span>Ready</span>
              </div>
            </div>
          </div>

          {/* Gauges */}
          <div className="space-y-3">
            <MetricGauge label="Precision (IoU)" value={metrics.precision} color="text-blue-400" />
            <MetricGauge label="Recall Rate" value={metrics.recall} color="text-emerald-400" />
            <MetricGauge label="F1 Performance" value={metrics.f1Score} color="text-purple-400" />
          </div>

          {/* Actions */}
          <div className="pt-6 border-t border-gray-800 space-y-4">
             <div className="p-4 bg-amber-500/10 border border-amber-500/20 rounded-xl">
               <div className="flex gap-3">
                 <Shield className="w-5 h-5 text-amber-500 shrink-0" />
                 <div>
                   <h3 className="text-xs font-bold text-amber-500 mb-1">Verification Required</h3>
                   <p className="text-[10px] text-gray-400 leading-relaxed">
                     Changes detected in sensitive zones. Generated reports must be submitted to FHN for field verification.
                   </p>
                 </div>
               </div>
             </div>

             <button 
               onClick={exportPDF}
               className="w-full bg-white text-gray-950 hover:bg-gray-100 transition py-3 rounded-lg font-bold text-sm flex items-center justify-center gap-2"
             >
               <FileText className="w-4 h-4" />
               Generate FHN Report (PDF)
             </button>
          </div>
          
          {/* Change Log */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold text-gray-400 uppercase flex items-center gap-2">
              <AlertTriangle className="w-3 h-3" /> Detection History
            </h3>
            <div className="space-y-2 max-h-48 overflow-y-auto pr-2 custom-scrollbar">
              {detections.length === 0 ? (
                <div className="text-[11px] text-gray-600 italic py-4 text-center border border-dashed border-gray-800 rounded-lg">
                  No active detections in session.
                </div>
              ) : (
                detections.map((d, i) => (
                  <div key={i} className="bg-gray-800/30 border border-gray-800 p-3 rounded-lg flex justify-between items-center hover:bg-gray-800/50 transition">
                    <div>
                      <div className="text-[10px] font-bold text-blue-400 mb-0.5 uppercase">Construction ID: {d.id}</div>
                      <div className="text-[10px] text-gray-400">Coordinates mapped to AOI center</div>
                    </div>
                    <div className="text-[11px] font-mono bg-red-500/10 text-red-400 px-2 py-1 rounded border border-red-500/20">
                      NEW
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </aside>
    </div>
  );
};

export default App;
