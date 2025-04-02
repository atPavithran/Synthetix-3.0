'use client';

import { useState } from 'react';
import VncViewer from '../../components/VncViewer';
import Header from '../../components/Header';
import Image from 'next/image';

export default function VncPage() {
  const [vncConfig, setVncConfig] = useState({
    host: '192.168.28.108',
    port: '6080',
    path: 'websockify',
    password: 'niggaballs', // Original password restored
    autoconnect: true
  });
  
  const [selectedRover, setSelectedRover] = useState(1);
  const [streamType, setStreamType] = useState('vnc'); // 'vnc' or 'camera'
  
  const rovers = [
    { id: 1, name: 'Rover 1' },
    { id: 2, name: 'Rover 2' },
    { id: 3, name: 'Rover 3' },
    { id: 4, name: 'Rover 4' },
    { id: 5, name: 'Rover 5' },
    { id: 0, name: 'No Rover' },
  ];

  // URL for the camera stream
  const getCameraStreamUrl = (roverId) => {
    if (roverId === 0) return '';
    return `http://localhost:8080/stream?topic=/robot${roverId}/camera/image_raw&type=mjpeg&quality=50&width=320&height=240`;
  };

  // Fixed camera URL
  const fixedCameraUrl = "http://localhost:8080/stream?topic=/fixed_camera/fixed_camera/image_raw";

  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      {/* Background Image */}
      <Image
        src="/images/bg.png"
        alt="Farm background"
        fill
        priority
        className="object-cover z-[-1]"
      />
      
      {/* Header */}
      <Header />
      
      {/* Main Content */}
      <div className="w-full pt-[70px] pb-8 px-2">
        <div className="w-full max-w-6xl mx-auto bg-white/90 backdrop-blur-sm rounded-lg shadow-lg border-2 border-blue-700 p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-blue-800 text-2xl font-bold">Live Farm Monitoring</h2>
            
            {/* Stream Toggle Button */}
            <button 
              className="bg-orange-600 text-white px-4 py-2 rounded-md hover:bg-orange-700 transition-all font-semibold"
              onClick={() => setStreamType(streamType === 'vnc' ? 'camera' : 'vnc')}
            >
              Switch to {streamType === 'vnc' ? 'Camera' : 'VNC'} Stream
            </button>
          </div>
          
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="mb-1 font-medium text-gray-700">Farm Monitoring System</div>
              <div className="w-full border border-gray-300 rounded">
                {/* Stream Container */}
                <div className="w-full h-[52vh] bg-gray-800 flex overflow-scroll items-center justify-center">
                  {streamType === 'vnc' ? (
                    <VncViewer 
                      host={vncConfig.host}
                      port={vncConfig.port}
                      path={vncConfig.path}
                      password={vncConfig.password}
                      autoconnect={vncConfig.autoconnect}
                    />
                  ) : (
                    selectedRover !== 0 ? (
                      <>
                        {/* Display fixed camera raw image when in camera mode */}
                        <img 
                          src={fixedCameraUrl}
                          className="w-full h-full object-contain"
                          alt={`Rover ${selectedRover} Camera Stream`}
                        />
                      </>
                    ) : (
                      <div className="text-white text-center">
                        <p>No rover selected. Please select a rover to view camera stream.</p>
                      </div>
                    )
                  )}
                </div>
              </div>
            </div>
            
            {/* Rover Selection Buttons */}
            <div className="w-full md:w-56">
              <div className="text-right mb-2 text-blue-800 font-bold">Select Rover</div>
              <div className="space-y-2">
                {rovers.map(rover => {
                  const name = rover.id === 0 ? 'No Rover' : `Rover ${rover.id}`;
                  return (
                    <button
                      key={rover.id}
                      className={`w-full py-2 px-4 rounded-md transition-all font-medium text-center ${
                        selectedRover === rover.id 
                          ? 'bg-blue-600 text-white' 
                          : 'bg-white border border-blue-600 text-blue-800 hover:bg-blue-100'
                      }`}
                      onClick={() => setSelectedRover(rover.id)}
                    >
                      {name}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
          
          {/* Rover Controls */}
          <div className="mt-6 text-center">
            <div className="text-blue-800 font-bold mb-2">Rover Controls</div>
            
            <div className="flex flex-wrap justify-center gap-4">
              <button className="bg-red-600 text-white px-8 py-3 rounded-md hover:bg-red-700 transition-all font-medium">
                Start/Stop
              </button>
              
              <button className="bg-blue-600 text-white py-3 px-8 rounded-md hover:bg-blue-700 transition-all font-medium">
                Forward
              </button>
              
              <button className="bg-blue-600 text-white py-3 px-8 rounded-md hover:bg-blue-700 transition-all font-medium">
                Left
              </button>
              
              <button className="bg-blue-600 text-white py-3 px-8 rounded-md hover:bg-blue-700 transition-all font-medium">
                Back
              </button>
              
              <button className="bg-blue-600 text-white py-3 px-8 rounded-md hover:bg-blue-700 transition-all font-medium">
                Right
              </button>
            </div>
            
            <div className="mt-4 text-center text-sm text-blue-800">
              <p>
                Secure remote {streamType === 'vnc' ? 'VNC' : 'camera'} monitoring connection established. 
                {selectedRover !== 0 
                  ? ` Controlling Rover ${selectedRover}.` 
                  : ' No rover selected.'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}