// components/RecentActivities.js
import React from 'react';

export default function RecentActivities({ roverData }) {
  // Generate some mock activities based on rover data
  const generateActivities = () => {
    const activities = [];
    const currentTime = new Date();
    
    Object.entries(roverData).forEach(([roverId, data]) => {
      // Add activity based on rover status
      const state = data?.status?.state;
      if (state) {
        const time = new Date(currentTime);
        time.setMinutes(time.getMinutes() - Math.floor(Math.random() * 30));
        
        let activity = '';
        if (state === 'idle') {
          activity = `${roverId} entered idle state`;
        } else if (state === 'moving') {
          activity = `${roverId} started moving`;
        } else if (state === 'scanning') {
          activity = `${roverId} initiated environmental scan`;
        } else if (state === 'error') {
          activity = `ERROR: ${roverId} encountered a problem`;
        } else {
          activity = `${roverId} status changed to ${state}`;
        }
        
        activities.push({
          id: `activity-${roverId}-${state}`,
          time,
          rover: roverId,
          activity,
          type: state === 'error' ? 'error' : 'info'
        });
      }
      
      // Add battery related activity if battery is low
      const batteryLevel = data?.battery?.level !== undefined ? 
                         data?.battery?.level : 
                         data?.battery?.percentage;
      if (batteryLevel !== undefined && batteryLevel < 30) {
        const time = new Date(currentTime);
        time.setMinutes(time.getMinutes() - Math.floor(Math.random() * 15));
        
        activities.push({
          id: `activity-${roverId}-battery`,
          time,
          rover: roverId,
          activity: `WARNING: ${roverId} battery level is low (${batteryLevel}%)`,
          type: 'warning'
        });
      }
    });
    
    // Sort activities by time (most recent first)
    return activities.sort((a, b) => b.time - a.time);
  };
  
  const activities = generateActivities();
  
  return (
    <div style={{ 
      backgroundColor: 'rgba(255, 255, 255, 0.9)', 
      padding: '20px', 
      borderRadius: '10px',
      border: '1px solid rgba(46, 125, 50, 0.3)',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
    }}>
      <h2 style={{ color: '#2e7d32', marginBottom: '15px' }}>Recent Activities</h2>
      
      {activities.length === 0 ? (
        <p style={{ color: '#666', fontStyle: 'italic' }}>No recent activities</p>
      ) : (
        <ul style={{ 
          padding: '0',
          margin: '0',
          listStyle: 'none'
        }}>
          {activities.map((activity) => (
            <li 
              key={activity.id}
              style={{ 
                padding: '12px', 
                marginBottom: '8px',
                backgroundColor: 
                  activity.type === 'error' ? 'rgba(211, 47, 47, 0.1)' : 
                  activity.type === 'warning' ? 'rgba(237, 108, 2, 0.1)' : 
                  'rgba(25, 118, 210, 0.1)',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                border: '1px solid rgba(0, 0, 0, 0.1)'
              }}
            >
              <div>
                <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>
                  {activity.activity}
                </div>
                <div style={{ fontSize: '12px', color: '#666' }}>
                  {activity.rover}
                </div>
              </div>
              
              <div style={{ fontSize: '12px', color: '#666' }}>
                {activity.time.toLocaleTimeString()}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}