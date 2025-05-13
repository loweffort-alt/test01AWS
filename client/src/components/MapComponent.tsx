import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

interface MapComponentProps {
  onPolygonCreated: (polygon: any) => void;
}

const MapComponent: React.FC<MapComponentProps> = ({ onPolygonCreated }) => {
  const mapRef = useRef<L.Map | null>(null);
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const drawLayerRef = useRef<L.FeatureGroup | null>(null);

  useEffect(() => {
    if (!mapContainerRef.current || mapRef.current) return;

    // Initialize map
    const map = L.map(mapContainerRef.current).setView([0, 0], 2);
    mapRef.current = map;

    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Initialize drawing feature group
    const drawLayer = new L.FeatureGroup();
    drawLayerRef.current = drawLayer;
    map.addLayer(drawLayer);

    // Add drawing controls
    const drawControl = new L.Control.Draw({
      draw: {
        rectangle: false,
        circle: false,
        circlemarker: false,
        marker: false,
        polyline: false,
        polygon: {
          allowIntersection: false,
          showArea: true
        }
      },
      edit: {
        featureGroup: drawLayer
      }
    });
    map.addControl(drawControl);

    // Handle created polygons
    map.on(L.Draw.Event.CREATED, (e: any) => {
      const layer = e.layer;
      drawLayer.addLayer(layer);
      const geoJSON = layer.toGeoJSON();
      onPolygonCreated(geoJSON);
    });

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, [onPolygonCreated]);

  return (
    <div 
      ref={mapContainerRef} 
      style={{ height: '500px', width: '100%' }}
    />
  );
};

export default MapComponent; 