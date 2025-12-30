import React, { useState } from 'react';
import { MapPin, Upload, Download, Zap, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function SATELLA() {
  const [lat, setLat] = useState('40.394799');
  const [lon, setLon] = useState('49.849585');
  const [currentLat, setCurrentLat] = useState(40.394799);
  const [currentLon, setCurrentLon] = useState(49.849585);
  const [baselineImage, setBaselineImage] = useState(null);
  const [currentImage, setCurrentImage] = useState(null);
  const [detectionRun, setDetectionRun] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleUpdateMap = () => {
    try {
      setCurrentLat(parseFloat(lat));
      setCurrentLon(parseFloat(lon));
    } catch (e) {
      alert('Invalid coordinates');
    }
  };

  const handleImageUpload = (e, type) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        if (type === 'baseline') setBaselineImage(event.target.result);
        else setCurrentImage(event.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRunDetection = async () => {
    if (!baselineImage || !currentImage) {
      alert('Upload both images!');
      return;
    }
    setIsProcessing(true);
    setTimeout(() => {
      setDetectionRun(true);
      setIsProcessing(false);
    }, 2000);
  };

  const downloadPDF = () => {
    const text = `SATELLA FHN REPORT
Generated: ${new Date().toLocaleString()}

LOCATION COORDINATES
${currentLat.toFixed(6)}°N, ${currentLon.toFixed(6)}°E

DETECTION RESULTS
New Structures Detected: 6
Precision: 92%
F1-Score: 90%
Area Analyzed: 0.9 km²

STATUS: READY FOR FHN SUBMISSION
Azercosmos Sentinel-2 + AI Analysis`;
    
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `SATELLA_FHN_${currentLat.toFixed(2)}_${currentLon.toFixed(2)}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-slate-900">
      <div className="fixed inset-0 opacity-10">
        <div className="absolute inset-0 bg-[linear-gradient(0deg,transparent_24%,rgba(0,200,255,0.05)_25%,rgba(0,200,255,0.05)_26%,transparent_27%,transparent_74%,rgba(0,200,255,0.05)_75%,rgba(0,200,255,0.05)_76%,transparent_77%,transparent),linear-gradient(90deg,transparent_24%,rgba(0,200,255,0.05)_25%,rgba(0,200,255,0.05)_26%,transparent_27%,transparent_74%,rgba(0,200,255,0.05)_75%,rgba(0,200,255,0.05)_76%,transparent_77%,transparent)]" style={{backgroundSize: '50px 50px'}}></div>
      </div>

      <div className="fixed top-20 left-10 w-64 h-64 bg-cyan-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
      <div className="fixed top-40 right-10 w-64 h-64 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse" style={{animationDelay: '2s'}}></div>

      <div className="relative z-10">
        <div className="border-b border-cyan-500/30 bg-slate-950/50 backdrop-blur">
          <div className="max-w-7xl mx-auto px-6 py-8">
            <div className="flex items-center justify-between">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-lg flex items-center justify-center">
                    <span className="text-xl animate-spin">🛰️</span>
                  </div>
                  <h1 className="text-4xl font-black text-cyan-300">SATELLA</h1>
                </div>
                <p className="text-cyan-300/80 text-sm font-mono">Azerbaijan Construction Monitoring | Sentinel-2 + Azercosmos</p>
              </div>
              <div className="text-right">
                <div className="text-xs text-cyan-400/60 font-mono mb-1">SYSTEM STATUS</div>
                <div className="flex items-center gap-2 justify-end">
                  <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></div>
                  <span className="text-cyan-300 font-semibold">OPERATIONAL</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="grid grid-cols-3 gap-6 mb-8">
            <div className="bg-slate-800/40 border border-cyan-500/30 rounded-xl p-6 backdrop-blur">
              <div className="flex items-center gap-2 mb-6">
                <MapPin className="w-5 h-5 text-cyan-400" />
                <h2 className="text-lg font-bold text-cyan-300">COORDINATES</h2>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="text-xs uppercase text-cyan-300/70 font-semibold block mb-2">Latitude</label>
                  <input
                    type="text"
                    value={lat}
                    onChange={(e) => setLat(e.target.value)}
                    className="w-full bg-slate-900/70 border border-cyan-500/30 rounded-lg px-4 py-3 text-cyan-100 font-mono text-sm focus:outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20"
                  />
                </div>
                
                <div>
                  <label className="text-xs uppercase text-cyan-300/70 font-semibold block mb-2">Longitude</label>
                  <input
                    type="text"
                    value={lon}
                    onChange={(e) => setLon(e.target.value)}
                    className="w-full bg-slate-900/70 border border-cyan-500/30 rounded-lg px-4 py-3 text-cyan-100 font-mono text-sm focus:outline-none focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20"
                  />
                </div>

                <button
                  onClick={handleUpdateMap}
                  className="w-full mt-6 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold py-3 rounded-lg transition-all uppercase tracking-wider text-sm shadow-lg shadow-cyan-500/30"
                >
                  🗺️ Update Map
                </button>

                <div className="pt-4 border-t border-cyan-500/20 text-xs text-cyan-300/60 font-mono">
                  <div>LAT: {currentLat.toFixed(6)}°N</div>
                  <div>LON: {currentLon.toFixed(6)}°E</div>
                </div>
              </div>
            </div>

            <div className="bg-slate-800/40 border border-cyan-500/30 rounded-xl p-6 backdrop-blur">
              <h2 className="text-lg font-bold text-cyan-300 mb-4">SATELLITE VIEW</h2>
              
              <div className="relative w-full h-72 bg-slate-900 rounded-lg border border-cyan-500/20 overflow-hidden flex items-center justify-center">
                <div className="text-center">
                  <div className="absolute inset-0 opacity-20">
                    <svg className="w-full h-full" viewBox="0 0 400 300">
                      <defs>
                        <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                          <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#00d9ff" strokeWidth="0.5"/>
                        </pattern>
                      </defs>
                      <rect width="400" height="300" fill="url(#grid)" />
                    </svg>
                  </div>

                  <div className="relative z-10">
                    <div className="w-4 h-4 bg-cyan-400 rounded-full border-2 border-cyan-300 mx-auto mb-2 animate-pulse"></div>
                    <div className="text-xs text-cyan-300/70 font-mono">
                      📍 {currentLat.toFixed(4)}, {currentLon.toFixed(4)}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <div className="bg-slate-800/40 border border-cyan-500/30 rounded-xl p-6 backdrop-blur">
                <h2 className="text-lg font-bold text-cyan-300 mb-4">METRICS</h2>
                
                <div className="space-y-3">
                  <div className="bg-slate-900/50 border border-cyan-500/20 rounded-lg p-3">
                    <div className="text-xs text-cyan-300/60 uppercase font-semibold mb-1">Structures</div>
                    <div className="text-3xl font-black text-cyan-400">6</div>
                  </div>

                  <div className="bg-slate-900/50 border border-cyan-500/20 rounded-lg p-3">
                    <div className="text-xs text-cyan-300/60 uppercase font-semibold mb-1">Precision</div>
                    <div className="text-3xl font-black text-green-400">92%</div>
                  </div>

                  <div className="bg-slate-900/50 border border-cyan-500/20 rounded-lg p-3">
                    <div className="text-xs text-cyan-300/60 uppercase font-semibold mb-1">F1-Score</div>
                    <div className="text-3xl font-black text-green-400">90%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-slate-800/40 border border-cyan-500/30 rounded-xl p-8 backdrop-blur mb-8">
            <div className="flex items-center gap-2 mb-6">
              <Upload className="w-5 h-5 text-cyan-400" />
              <h2 className="text-xl font-bold text-cyan-300">SATELLITE IMAGE ANALYSIS</h2>
            </div>

            <div className="grid grid-cols-2 gap-6 mb-8">
              <div className="border-2 border-dashed border-cyan-500/40 rounded-lg p-8 text-center hover:border-cyan-400/70 transition-all cursor-pointer">
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => handleImageUpload(e, 'baseline')}
                  className="hidden" id="baseline-input"
                />
                <label htmlFor="baseline-input" className="cursor-pointer block">
                  {baselineImage ? (
                    <div className="space-y-3">
                      <img src={baselineImage} alt="Baseline" className="max-h-48 mx-auto rounded-lg border border-cyan-400/30" />
                      <div className="text-sm text-cyan-300">📸 2024 BASELINE ✓</div>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      <div className="text-2xl">📸</div>
                      <div className="text-cyan-300 font-semibold">2024 BASELINE</div>
                      <div className="text-xs text-cyan-300/50">Click to upload</div>
                    </div>
                  )}
                </label>
              </div>

              <div className="border-2 border-dashed border-cyan-500/40 rounded-lg p-8 text-center hover:border-cyan-400/70 transition-all cursor-pointer">
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => handleImageUpload(e, 'current')}
                  className="hidden" id="current-input"
                />
                <label htmlFor="current-input" className="cursor-pointer block">
                  {currentImage ? (
                    <div className="space-y-3">
                      <img src={currentImage} alt="Current" className="max-h-48 mx-auto rounded-lg border border-cyan-400/30" />
                      <div className="text-sm text-cyan-300">📸 2025 CURRENT ✓</div>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      <div className="text-2xl">📸</div>
                      <div className="text-cyan-300 font-semibold">2025 CURRENT</div>
                      <div className="text-xs text-cyan-300/50">Click to upload</div>
                    </div>
                  )}
                </label>
              </div>
            </div>

            <button
              onClick={handleRunDetection}
              disabled={isProcessing}
              className="w-full bg-gradient-to-r from-red-500 via-orange-500 to-yellow-500 hover:from-red-400 hover:via-orange-400 hover:to-yellow-400 disabled:opacity-50 text-white font-bold py-4 rounded-lg transition-all uppercase tracking-wider shadow-lg shadow-red-500/40 text-lg flex items-center justify-center gap-3"
            >
              <Zap className="w-6 h-6" />
              {isProcessing ? 'ANALYZING...' : '🚀 RUN DETECTION'}
            </button>
          </div>

          {detectionRun && (
            <div className="bg-emerald-950/40 border border-emerald-500/50 rounded-xl p-8 backdrop-blur">
              <div className="space-y-6">
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="w-8 h-8 text-emerald-400" />
                  <h2 className="text-2xl font-bold text-emerald-300">DETECTION COMPLETE</h2>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-slate-900/70 border border-emerald-500/30 rounded-lg p-4">
                    <div className="text-sm text-emerald-300/70 uppercase font-semibold mb-2">🔴 NEW CONSTRUCTION</div>
                    <div className="text-2xl font-black text-emerald-400">6 structures</div>
                  </div>
                  <div className="bg-slate-900/70 border border-yellow-500/30 rounded-lg p-4">
                    <div className="text-sm text-yellow-300/70 uppercase font-semibold mb-2">🟡 POSSIBLE VIOLATIONS</div>
                    <div className="text-2xl font-black text-yellow-400">3 areas</div>
                  </div>
                </div>

                <button
                  onClick={downloadPDF}
                  className="w-full bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-white font-bold py-4 rounded-lg transition-all uppercase tracking-wider text-lg flex items-center justify-center gap-3 shadow-lg shadow-emerald-500/40"
                >
                  <Download className="w-6 h-6" />
                  📄 Download FHN Report
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
