
export interface Coordinate {
  lat: number;
  lng: number;
}

export interface BuildingDetection {
  bbox: [number, number, number, number]; // [ymin, xmin, ymax, xmax]
  confidence: number;
  id: string;
  isNew: boolean;
}

export interface MonitoringMetrics {
  precision: number;
  recall: number;
  f1Score: number;
  newConstructionsCount: number;
}

export interface HistoryItem {
  lat: number;
  lng: number;
  timestamp: number;
}
