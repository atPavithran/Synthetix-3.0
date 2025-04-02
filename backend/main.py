from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from typing import Dict, Any, Optional
import logging
import asyncio
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fleet API Middleware")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Base URL for the Fleet API
BASE_URL = "https://fleetbots-production.up.railway.app/api"

# Store session ID in memory
# In production, consider using a more persistent storage
SESSION_ID = None

# Model for API responses
class ApiResponse(BaseModel):
    status: str
    data: Dict[str, Any]

async def get_session_id():
    """Get the current session ID or create a new one."""
    global SESSION_ID
    
    if SESSION_ID:
        return SESSION_ID
    
    try:
        # Start a new session
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/session/start")
            response.raise_for_status()
            data = response.json()
            SESSION_ID = data.get("session_id")
            logger.info(f"Created new session: {SESSION_ID}")
            return SESSION_ID
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")

async def handle_api_call(url: str, session_id: str):
    """Handle API calls with retry logic for expired sessions."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            
            # Check if session expired
            if response.status_code == 401 or (response.status_code == 400 and 
                                             ("session expired" in response.text.lower() or 
                                              "invalid session" in response.text.lower())):
                logger.info("Session expired. Creating a new one...")
                global SESSION_ID
                SESSION_ID = None
                new_session_id = await get_session_id()
                # Retry with new session
                new_url = url.replace(f"session_id={session_id}", f"session_id={new_session_id}")
                return await handle_api_call(new_url, new_session_id)
            
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        raise HTTPException(status_code=e.response.status_code, 
                           detail=f"API error: {e.response.text}")
    except Exception as e:
        logger.error(f"Error calling {url}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to call API: {str(e)}")

@app.get("/api/fleet/status")
async def get_fleet_status(session_id: str = Depends(get_session_id)):
    """Get the status of the entire fleet."""
    url = f"{BASE_URL}/fleet/status?session_id={session_id}"
    result = await handle_api_call(url, session_id)
    return {"status": "success", "data": result}

@app.get("/api/rover/{rover_id}/status")
async def get_rover_status(rover_id: str, session_id: str = Depends(get_session_id)):
    """Get the status of a specific rover."""
    url = f"{BASE_URL}/rover/{rover_id}/status?session_id={session_id}"
    result = await handle_api_call(url, session_id)
    return {"status": "success", "data": result}

@app.get("/api/rover/{rover_id}/sensor-data")
async def get_sensor_data(rover_id: str, session_id: str = Depends(get_session_id)):
    """Get sensor data from a specific rover."""
    url = f"{BASE_URL}/rover/{rover_id}/sensor-data?session_id={session_id}"
    result = await handle_api_call(url, session_id)
    return {"status": "success", "data": result}

@app.get("/api/rover/{rover_id}/battery")
async def get_battery_level(rover_id: str, session_id: str = Depends(get_session_id)):
    """Get battery level of a specific rover."""
    url = f"{BASE_URL}/rover/{rover_id}/battery?session_id={session_id}"
    result = await handle_api_call(url, session_id)
    return {"status": "success", "data": result}

@app.get("/api/rover/{rover_id}/coordinates")
async def get_coordinates(rover_id: str, session_id: str = Depends(get_session_id)):
    """Get coordinates of a specific rover."""
    url = f"{BASE_URL}/rover/{rover_id}/coordinates?session_id={session_id}"
    result = await handle_api_call(url, session_id)
    return {"status": "success", "data": result}

@app.get("/api/all-rover-data")
async def get_all_rover_data(session_id: str = Depends(get_session_id)):
    """Get data for all rovers."""
    try:
        # Get fleet status
        fleet_status = await handle_api_call(f"{BASE_URL}/fleet/status?session_id={session_id}", session_id)
        
        # Get data for each rover
        rovers = ["Rover-1", "Rover-2", "Rover-3", "Rover-4", "Rover-5"]
        rover_data = {}
        
        for rover_id in rovers:
            try:
                # Fetch each rover's data sequentially
                status = await handle_api_call(f"{BASE_URL}/rover/{rover_id}/status?session_id={session_id}", session_id)
                sensor_data = await handle_api_call(f"{BASE_URL}/rover/{rover_id}/sensor-data?session_id={session_id}", session_id)
                battery = await handle_api_call(f"{BASE_URL}/rover/{rover_id}/battery?session_id={session_id}", session_id)
                coordinates = await handle_api_call(f"{BASE_URL}/rover/{rover_id}/coordinates?session_id={session_id}", session_id)
                
                rover_data[rover_id] = {
                    "status": status,
                    "sensorData": sensor_data,
                    "battery": battery,
                    "coordinates": coordinates
                }
            except Exception as e:
                logger.error(f"Error fetching data for {rover_id}: {str(e)}")
                rover_data[rover_id] = {
                    "error": str(e),
                    "status": {"operational": False, "state": "error"},
                    "battery": {"level": 0, "percentage": 0, "charging": False},
                    "coordinates": {"x": 0, "y": 0},  # Add default coordinates
                    "sensorData": {}  # Add empty sensor data when there's an error
                }
        
        return {
            "status": "success",
            "data": {
                "fleetStatus": fleet_status,
                "roverData": rover_data
            }
        }
    except Exception as e:
        logger.error(f"Error in get_all_rover_data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch all rover data: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint that confirms the server is running."""
    return {"status": "success", "message": "Fleet API middleware server is running"}

if __name__ == "__main__":
    import uvicorn
    # Run the server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)