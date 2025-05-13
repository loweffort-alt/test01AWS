import React, { useState } from 'react';
import MapComponent from './components/MapComponent';
import ShapefileUpload from './components/ShapefileUpload';
import 'leaflet/dist/leaflet.css';

interface SourceZone {
  geometry: any;
  type: 'interface' | 'intraslab' | 'crustal';
}

function App() {
  const [sourceZones, setSourceZones] = useState<SourceZone[]>([]);
  const [currentType, setCurrentType] = useState<'interface' | 'intraslab' | 'crustal'>('interface');
  const [shapefiles, setShapefiles] = useState<FileList | null>(null);

  const handleFileUpload = (files: FileList) => {
    setShapefiles(files);
    // Shapefile processing will be implemented later
  };

  const handlePolygonCreated = (polygon: any) => {
    setSourceZones([...sourceZones, {
      geometry: polygon,
      type: currentType
    }]);
  };

  const handleSubmit = () => {
    // API submission will be implemented later
    console.log('Source Zones:', sourceZones);
    console.log('Shapefiles:', shapefiles);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>Seismic Source Zone Editor</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <ShapefileUpload onFileUpload={handleFileUpload} />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ marginRight: '10px' }}>Source Type:</label>
        <select 
          value={currentType}
          onChange={(e) => setCurrentType(e.target.value as any)}
          style={{ padding: '5px' }}
        >
          <option value="interface">Interface</option>
          <option value="intraslab">Intraslab</option>
          <option value="crustal">Crustal</option>
        </select>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <MapComponent onPolygonCreated={handlePolygonCreated} />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>Defined Source Zones:</h3>
        <ul>
          {sourceZones.map((zone, index) => (
            <li key={index}>
              Source Zone {index + 1} - Type: {zone.type}
            </li>
          ))}
        </ul>
      </div>

      <button 
        onClick={handleSubmit}
        style={{
          padding: '10px 20px',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer'
        }}
      >
        Submit Data
      </button>
    </div>
  );
}

export default App;
