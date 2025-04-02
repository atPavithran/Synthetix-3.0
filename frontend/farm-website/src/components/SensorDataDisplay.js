// components/SensorDataDisplay.js
import React from 'react';

export default function SensorDataDisplay({ sensorData }) {
  if (!sensorData) {
    return (
      <div style={{ 
        padding: '15px', 
        backgroundColor: 'rgba(0, 0, 0, 0.05)', 
        borderRadius: '8px',
        textAlign: 'center'
      }}>
        <p>No sensor data available</p>
      </div>
    );
  }

  return (
    <div style={{ 
      backgroundColor: 'rgba(255, 255, 255, 0.9)', 
      padding: '20px', 
      borderRadius: '10px',
      border: '1px solid rgba(46, 125, 50, 0.3)',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
    }}>
      <h2 style={{ color: '#2e7d32', marginBottom: '15px' }}>Sensor Readings</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '15px' }}>
        {Object.entries(sensorData).map(([key, value]) => {
          // Skip the non-sensor data properties
          if (key === 'timestamp' || key === 'rover_id') {
            return null;
          }
          
          return (
            <div 
              key={key}
              style={{ 
                padding: '12px', 
                backgroundColor: 'rgba(46, 125, 50, 0.05)',
                borderRadius: '8px',
                border: '1px solid rgba(0, 0, 0, 0.1)'
              }}
            >
              <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>
                {key.replace(/_/g, ' ').toUpperCase()}
              </div>
              <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
                {typeof value === 'number' ? value.toFixed(2) : value}
                {getUnitByType(key)}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function getUnitByType(sensorType) {
  const units = {
    temperature: '°C',
    humidity: '%',
    pressure: ' hPa',
    radiation: ' mSv',
    speed: ' m/s',
    altitude: ' m',
    gas_level: ' ppm',
    light_level: ' lux',
    dust: ' µg/m³',
    sound: ' dB'
  };
  
  for (const type in units) {
    if (sensorType.includes(type)) {
      return units[type];
    }
  }
  
  return '';
}