// components/RoverStatusCard.js
import React from 'react';
import SensorDataDisplay from './SensorDataDisplay';

export default function RoverStatusCard({ roverData }) {
  if (!roverData) {
    return <div>No rover data available</div>;
  }

  const { status, battery, coordinates, sensorData } = roverData;
  
  // Ensure we have valid data or provide defaults
  const isOperational = status?.operational !== undefined ? status.operational : false;
  const currentState = status?.state || 'unknown';
  const batteryLevel = battery?.level !== undefined ? battery.level : 
                     (battery?.percentage !== undefined ? battery.percentage : 0);
  const isCharging = battery?.charging !== undefined ? battery.charging : false;
  
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '20px'
    }}>
      {/* Status Card */}
      <div style={{ 
        backgroundColor: 'rgba(255, 255, 255, 0.9)', 
        padding: '20px', 
        borderRadius: '10px',
        border: '1px solid rgba(46, 125, 50, 0.3)',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
      }}>
        <h2 style={{ color: '#2e7d32', marginBottom: '15px' }}>Rover Status</h2>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '15px' }}>
          {/* Operational Status */}
          <div style={{ 
            padding: '15px', 
            backgroundColor: isOperational ? 'rgba(46, 125, 50, 0.1)' : 'rgba(211, 47, 47, 0.1)', 
            borderRadius: '8px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>
              STATUS
            </div>
            <div style={{ 
              fontSize: '18px', 
              fontWeight: 'bold',
              color: isOperational ? '#2e7d32' : '#d32f2f'
            }}>
              {isOperational ? 'OPERATIONAL' : 'OFFLINE'}
            </div>
          </div>
          
          {/* State */}
          <div style={{ 
            padding: '15px', 
            backgroundColor: 'rgba(0, 0, 0, 0.05)', 
            borderRadius: '8px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>
              STATE
            </div>
            <div style={{ 
              fontSize: '18px', 
              fontWeight: 'bold'
            }}>
              {currentState.toUpperCase()}
            </div>
          </div>
          
          {/* Battery Level */}
          <div style={{ 
            padding: '15px', 
            backgroundColor: 
              batteryLevel > 70 ? 'rgba(46, 125, 50, 0.1)' : 
              batteryLevel > 30 ? 'rgba(237, 108, 2, 0.1)' : 
              'rgba(211, 47, 47, 0.1)', 
            borderRadius: '8px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>
              BATTERY
            </div>
            <div style={{ 
              fontSize: '18px', 
              fontWeight: 'bold',
              color: 
                batteryLevel > 70 ? '#2e7d32' : 
                batteryLevel > 30 ? '#ed6c02' : 
                '#d32f2f'
            }}>
              {batteryLevel}%
              {isCharging && ' (Charging)'}
            </div>
          </div>
          
          {/* Coordinates */}
          <div style={{ 
            padding: '15px', 
            backgroundColor: 'rgba(0, 0, 0, 0.05)', 
            borderRadius: '8px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>
              LOCATION
            </div>
            <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
              {coordinates?.x !== undefined && coordinates?.y !== undefined ? 
                `(${coordinates.x.toFixed(2)}, ${coordinates.y.toFixed(2)})` : 
                coordinates?.latitude !== undefined && coordinates?.longitude !== undefined ?
                `(${coordinates.latitude.toFixed(2)}, ${coordinates.longitude.toFixed(2)})` :
                'Unknown'}
            </div>
          </div>
        </div>
      </div>
      
      {/* Sensor Data Display */}
      <SensorDataDisplay sensorData={sensorData} />
    </div>
  );
}