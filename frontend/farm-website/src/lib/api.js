const BASE_URL = "https://fleetbots-production.up.railway.app/api";

// Utility function to handle timeouts
const fetchWithTimeout = async (url, options = {}, timeout = 8000) => {
  const controller = new AbortController();
  const { signal } = controller;
  
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  
  try {
    const response = await fetch(url, {
      ...options,
      signal
    });
    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      throw new Error('Request timeout. The server took too long to respond.');
    }
    throw error;
  }
};

/**
 * Start a new session and return the session ID
 */
export async function startSession() {
  try {
    const response = await fetchWithTimeout(`${BASE_URL}/session/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      }
    });
    
    if (!response.ok) {
      const text = await response.text();
      throw new Error(`API error: ${response.status} - ${text}`);
    }
    
    const data = await response.json();
    
    // Save the session ID to localStorage
    if (typeof window !== 'undefined') {
      localStorage.setItem('SESSION_ID', data.session_id);
    }
    
    return data.session_id;
  } catch (error) {
    console.error("Error starting session:", error);
    throw error;
  }
}

/**
 * Get the session ID from localStorage or start a new session if none exists
 */
export async function getSessionId() {
  // Check if we're on the client side
  if (typeof window === 'undefined') {
    return null; // We'll handle this later
  }
  
  // Try localStorage (client-side)
  let sessionId = localStorage.getItem('SESSION_ID');
  
  if (!sessionId) {
    console.log("No existing session ID found. Starting a new session...");
    sessionId = await startSession();
  }
  
  return sessionId;
}

/**
 * Handle API call with session renewal
 */
async function apiCall(url, currentSessionId) {
  try {
    const response = await fetchWithTimeout(url, {
      headers: {
        'Accept': 'application/json',
      }
    });
    
    if (!response.ok) {
      const text = await response.text();
      
      // If session expired, start a new one
      if (text.toLowerCase().includes("session expired") || 
          text.toLowerCase().includes("invalid session")) {
        console.log("Session expired. Starting a new one...");
        const newSessionId = await startSession();
        
        // Update localStorage
        if (typeof window !== 'undefined') {
          localStorage.setItem('SESSION_ID', newSessionId);
        }
        
        // Retry with new session ID
        return apiCall(url.replace(`session_id=${currentSessionId}`, `session_id=${newSessionId}`), newSessionId);
      }
      
      throw new Error(`API error: ${response.status} - ${text}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`Error calling API ${url}:`, error);
    throw error;
  }
}

/**
 * Get the status of the entire fleet
 */
export async function getFleetStatus(sessionId) {
  return apiCall(`${BASE_URL}/fleet/status?session_id=${sessionId}`, sessionId);
}

/**
 * Get the status of a specific rover
 */
export async function getRoverStatus(sessionId, roverId) {
  return apiCall(`${BASE_URL}/rover/${roverId}/status?session_id=${sessionId}`, sessionId);
}

/**
 * Get sensor data from a specific rover
 */
export async function getSensorData(sessionId, roverId) {
  return apiCall(`${BASE_URL}/rover/${roverId}/sensor-data?session_id=${sessionId}`, sessionId);
}

/**
 * Get battery level of a specific rover
 */
export async function getBatteryLevel(sessionId, roverId) {
  return apiCall(`${BASE_URL}/rover/${roverId}/battery?session_id=${sessionId}`, sessionId);
}

/**
 * Get coordinates of a specific rover
 */
export async function getCoordinates(sessionId, roverId) {
  return apiCall(`${BASE_URL}/rover/${roverId}/coordinates?session_id=${sessionId}`, sessionId);
}

/**
 * Fetch data for all rovers
 */
export async function fetchAllRoverData() {
  try {
    // Make sure we're on client side
    if (typeof window === 'undefined') {
      throw new Error("Cannot fetch rover data server-side");
    }
    
    // Get or create session ID
    const sessionId = await getSessionId();
    
    if (!sessionId) {
      throw new Error("Could not obtain a valid session ID");
    }
    
    // Get the list of rovers
    const rovers = ["Rover-1", "Rover-2", "Rover-3", "Rover-4", "Rover-5"];
    
    // Get fleet status
    const fleetStatus = await getFleetStatus(sessionId);
    
    // Collect all rover data
    const allRoverData = {};
    
    // Fetch data for each rover sequentially to avoid overwhelming the API
    for (const roverId of rovers) {
      try {
        const status = await getRoverStatus(sessionId, roverId);
        const sensorData = await getSensorData(sessionId, roverId);
        const battery = await getBatteryLevel(sessionId, roverId);
        const coordinates = await getCoordinates(sessionId, roverId);
        
        allRoverData[roverId] = {
          status,
          sensorData,
          battery,
          coordinates
        };
      } catch (error) {
        console.error(`Failed to fetch data for ${roverId}:`, error);
        // Still include the rover with an error state
        allRoverData[roverId] = { 
          error: error.message,
          status: { operational: false, state: "error" },
          battery: { level: 0, charging: false }
        };
      }
    }
    
    return {
      fleetStatus,
      roverData: allRoverData
    };
  } catch (error) {
    console.error("Error fetching all rover data:", error);
    throw error;
  }
}