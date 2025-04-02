// components/FleetOverview.js
import React from 'react';

export default function FleetOverview({ fleetStatus }) {
  // Check if fleetStatus is available and extract values with defaults
  const activeRovers = fleetStatus?.active_rovers || fleetStatus?.activeRovers || 0;
  const totalRovers = fleetStatus?.total_rovers || fleetStatus?.totalRovers || 0;
  const fleetHealth = fleetStatus?.health || fleetStatus?.fleet_health || 'unknown';
  const missionStatus = fleetStatus?.mission_status || fleetStatus?.missionStatus || 'unknown';
  
  // Calculate percentage for active rovers
  const activePercentage = totalRovers > 0 ? (activeRovers / totalRovers) * 100 : 0;
  
  return (
    <div style={{ 
      backgroundColor: 'rgba(255, 255, 255, 0.9)', 
      padding: '20px', 
      borderRadius: '10px',
      border: '1px solid rgba(46, 125, 50, 0.3)',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      marginBottom: '20px'
    }}>
      <h2 style={{ color: '#2e7d32', marginBottom: '15px' }}>Fleet Overview</h2>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
        {/* Active Rovers */}
        <div style={{ 
          padding: '15px', 
          backgroundColor: 'rgba(46, 125, 50, 0.1)', 
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>
            ACTIVE ROVERS
          </div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#2e7d32' }}>
            {activeRovers} / {totalRovers}
          </div>
          <div style={{ 
            width: '100%', 
            height: '6px', 
            backgroundColor: 'rgba(0, 0, 0, 0.1)',
            borderRadius: '3px',
            marginTop: '8px',
            overflow: 'hidden'
          }}>
            <div style={{ 
              width: `${activePercentage}%`, 
              height: '100%', 
              backgroundColor: '#2e7d32',
              borderRadius: '3px'
            }}></div>
          </div>
        </div>
        
        {/* Fleet Health */}
        <div style={{ 
          padding: '15px', 
          backgroundColor: 'rgba(0, 0, 0, 0.05)', 
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>
            FLEET HEALTH
          </div>
          <div style={{ 
            fontSize: '24px', 
            fontWeight: 'bold',
            color: 
              fleetHealth === 'excellent' || fleetHealth === 'good' ? '#2e7d32' : 
              fleetHealth === 'fair' ? '#ed6c02' : 
              fleetHealth === 'poor' ? '#d32f2f' : '#666'
          }}>
            {typeof fleetHealth === 'string' ? fleetHealth.toUpperCase() : fleetHealth}
          </div>
        </div>
        
        {/* Mission Status */}
        <div style={{ 
          padding: '15px', 
          backgroundColor: 'rgba(0, 0, 0, 0.05)', 
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>
            MISSION STATUS
          </div>
          <div style={{ 
            fontSize: '24px', 
            fontWeight: 'bold',
            color: 
              missionStatus === 'completed' || missionStatus === 'success' ? '#2e7d32' : 
              missionStatus === 'in_progress' || missionStatus === 'inProgress' ? '#1976d2' : 
              missionStatus === 'paused' ? '#ed6c02' : 
              missionStatus === 'failed' ? '#d32f2f' : '#666'
          }}>
            {typeof missionStatus === 'string' ? 
              missionStatus.replace('_', ' ').toUpperCase() : missionStatus}
          </div>
        </div>
      </div>
    </div>
  );
}