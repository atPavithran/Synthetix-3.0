'use client';

import { useState, useEffect } from 'react';
import Layout from '../../components/Layout';
import FleetOverview from '../../components/FleetOverview';
import RoverStatusCard from '../../components/RoverStatusCard';
import RecentActivities from '../../components/RecentActivities';
import useRoverData from '../../hooks/useRoverData';

export default function Dashboard() {
  const { data, loading, error, refetch } = useRoverData(15000); // Refresh every 15 seconds
  const [selectedRoverId, setSelectedRoverId] = useState(null);
  
  // Select the first rover when data loads
  useEffect(() => {
    if (data?.roverData) {
      const roverIds = Object.keys(data.roverData);
      if (roverIds.length > 0 && !selectedRoverId) {
        setSelectedRoverId(roverIds[0]);
      }
    }
  }, [data, selectedRoverId]);

  return (
    <Layout>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1 style={{ color: '#2e7d32' }}>Rover Fleet Dashboard</h1>
        <button 
          onClick={refetch}
          style={{
            backgroundColor: '#2e7d32',
            color: 'white',
            border: 'none',
            padding: '8px 16px',
            borderRadius: '4px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '5px'
          }}
        >
          <span>Refresh Data</span>
        </button>
      </div>
      
      {loading && !data && (
        <div style={{ 
          padding: '20px', 
          textAlign: 'center', 
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          borderRadius: '10px',
          marginBottom: '20px'
        }}>
          <p>Loading rover data...</p>
        </div>
      )}
      
      {error && (
        <div style={{ 
          padding: '20px', 
          textAlign: 'center', 
          backgroundColor: 'rgba(211, 47, 47, 0.1)',
          borderRadius: '10px',
          marginBottom: '20px',
          color: '#d32f2f'
        }}>
          <p>Error: {error}</p>
          <button 
            onClick={refetch}
            style={{
              backgroundColor: '#2e7d32',
              color: 'white',
              border: 'none',
              padding: '8px 16px',
              borderRadius: '4px',
              cursor: 'pointer',
              marginTop: '10px'
            }}
          >
            Retry
          </button>
        </div>
      )}
      
      {data && (
        <>
          {/* Fleet Overview */}
          <FleetOverview fleetStatus={data.fleetStatus} />
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '20px', marginBottom: '30px' }}>
            {/* Rover List */}
            <div style={{ 
              backgroundColor: 'rgba(255, 255, 255, 0.9)', 
              padding: '20px', 
              borderRadius: '10px',
              border: '1px solid rgba(46, 125, 50, 0.3)',
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
            }}>
              <h2 style={{ color: '#2e7d32', marginBottom: '15px' }}>Rovers</h2>
              <ul style={{ 
                padding: '0',
                margin: '0',
                listStyle: 'none'
              }}>
                {Object.keys(data.roverData).map((roverId) => {
                  const isOperational = data.roverData[roverId]?.status?.operational;
                  // Handle different possible battery level fields
                  const batteryLevel = data.roverData[roverId]?.battery?.level !== undefined ? 
                                     data.roverData[roverId]?.battery?.level : 
                                     data.roverData[roverId]?.battery?.percentage || 0;
                  
                  return (
                    <li 
                      key={roverId}
                      style={{ 
                        padding: '12px', 
                        marginBottom: '8px',
                        backgroundColor: selectedRoverId === roverId ? 'rgba(46, 125, 50, 0.1)' : 'transparent',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        border: '1px solid rgba(0, 0, 0, 0.1)'
                      }}
                      onClick={() => setSelectedRoverId(roverId)}
                    >
                      <div style={{ display: 'flex', alignItems: 'center' }}>
                        <div style={{
                          width: '10px',
                          height: '10px',
                          borderRadius: '50%',
                          backgroundColor: isOperational ? '#2e7d32' : '#d32f2f',
                          marginRight: '10px'
                        }}></div>
                        <span style={{ fontWeight: selectedRoverId === roverId ? 'bold' : 'normal' }}>
                          {roverId}
                        </span>
                      </div>
                      
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px'
                      }}>
                        <div style={{
                          fontSize: '12px',
                          color: data.roverData[roverId]?.status?.state === 'idle' ? '#666' : 
                                data.roverData[roverId]?.status?.state === 'moving' ? '#2e7d32' :
                                data.roverData[roverId]?.status?.state === 'error' ? '#d32f2f' : '#666'
                        }}>
                          {data.roverData[roverId]?.status?.state || 'unknown'}
                        </div>
                        
                        <div style={{
                          backgroundColor: batteryLevel > 70 ? 'rgba(46, 125, 50, 0.1)' : 
                                        batteryLevel > 30 ? 'rgba(237, 108, 2, 0.1)' : 'rgba(211, 47, 47, 0.1)',
                          padding: '4px 8px',
                          borderRadius: '4px',
                          fontSize: '12px',
                          fontWeight: 'bold',
                          color: batteryLevel > 70 ? '#2e7d32' : 
                                batteryLevel > 30 ? '#ed6c02' : '#d32f2f'
                        }}>
                          {batteryLevel}%
                        </div>
                      </div>
                    </li>
                  );
                })}
              </ul>
            </div>
            
            {/* Selected Rover Details */}
            <div>
              {selectedRoverId && data.roverData[selectedRoverId] && (
                <RoverStatusCard roverData={data.roverData[selectedRoverId]} />
              )}
            </div>
          </div>
          
          {/* Recent Activities */}
          <RecentActivities roverData={data.roverData} />
        </>
      )}
    </Layout>
  );
}



