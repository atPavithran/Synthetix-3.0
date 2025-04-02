'use client';

import { useEffect, useRef } from 'react';

const VncViewer = ({ 
  host = 'localhost', 
  port = '6080', 
  path = 'websockify', 
  password = null,
  autoconnect = true 
}) => {
  const iframeRef = useRef(null);

  useEffect(() => {
    // When the component mounts, set the iframe source with all necessary parameters
    if (iframeRef.current) {
      // Build the URL with query parameters
      let vncUrl = `http://${host}:${port}/vnc.html?host=${host}&port=${port}&path=${path}`;
      
      // Add autoconnect parameter
      if (autoconnect) {
        vncUrl += '&autoconnect=true';
      }
      
      // Add password parameter if provided
      // Note: This is sent in the URL which isn't secure for production
      // but works for development purposes
      if (password) {
        vncUrl += `&password=${encodeURIComponent(password)}`;
      }
      
      // Set resize parameter to remote to scale the remote desktop
      vncUrl += '&resize=remote';
      
      // Set the iframe source to the noVNC viewer HTML with parameters
      iframeRef.current.src = vncUrl;
    }
  }, [host, port, path, password, autoconnect]);

  return (
    <div className="w-full h-full flex flex-col">
      <iframe 
        ref={iframeRef}
        className="flex-grow w-full h-full border border-gray-300 rounded"
        allow="fullscreen"
      ></iframe>
    </div>
  );
};

export default VncViewer;