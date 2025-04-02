#api.py

import requests
import json
import os
from pprint import pprint
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URL for the SLAM-Based Fleet API
BASE_URL = "https://fleetbots-production.up.railway.app/api"

def start_session():
    """Start a new session and return the session ID."""
    response = requests.post(f"{BASE_URL}/session/start")
    data = response.json()
    print("\n=== NEW SESSION STARTED ===")
    print(f"Session ID: {data.get('session_id')}")
    
    # Save the session ID to .env file
    with open('.env', 'w') as f:
        f.write(f"SESSION_ID={data.get('session_id')}")
    
    return data.get('session_id')

def get_session_id():
    """Get the session ID from .env file or start a new session if none exists."""
    session_id = os.getenv("SESSION_ID")
    
    if not session_id:
        print("No existing session ID found. Starting a new session...")
        return start_session()
    
    print(f"\n=== USING EXISTING SESSION ===")
    print(f"Session ID: {session_id}")
    return session_id

def get_fleet_status(session_id):
    """Get the status of the entire fleet."""
    response = requests.get(f"{BASE_URL}/fleet/status", params={"session_id": session_id})
    print("\n=== FLEET STATUS ===")
    try:
        pprint(response.json())
        return response.json()
    except json.JSONDecodeError:
        print(f"Error decoding JSON. Response: {response.text}")
        # If session expired, start a new one
        if "session expired" in response.text.lower() or "invalid session" in response.text.lower():
            print("Session may have expired. Starting a new one...")
            new_session_id = start_session()
            return get_fleet_status(new_session_id)
        return None

def get_rover_status(session_id, rover_id):
    """Get the status of a specific rover."""
    response = requests.get(f"{BASE_URL}/rover/{rover_id}/status", params={"session_id": session_id})
    print(f"\n=== ROVER STATUS: {rover_id} ===")
    try:
        pprint(response.json())
        return response.json()
    except json.JSONDecodeError:
        print(f"Error decoding JSON. Response: {response.text}")
        # If session expired, start a new one
        if "session expired" in response.text.lower() or "invalid session" in response.text.lower():
            print("Session may have expired. Starting a new one...")
            new_session_id = start_session()
            return get_rover_status(new_session_id, rover_id)
        return None

def get_sensor_data(session_id, rover_id):
    """Get sensor data from a specific rover."""
    response = requests.get(f"{BASE_URL}/rover/{rover_id}/sensor-data", params={"session_id": session_id})
    print(f"\n=== SENSOR DATA: {rover_id} ===")
    try:
        pprint(response.json())
        return response.json()
    except json.JSONDecodeError:
        print(f"Error decoding JSON. Response: {response.text}")
        # If session expired, start a new one
        if "session expired" in response.text.lower() or "invalid session" in response.text.lower():
            print("Session may have expired. Starting a new one...")
            new_session_id = start_session()
            return get_sensor_data(new_session_id, rover_id)
        return None

def get_battery_level(session_id, rover_id):
    """Get battery level of a specific rover."""
    response = requests.get(f"{BASE_URL}/rover/{rover_id}/battery", params={"session_id": session_id})
    print(f"\n=== BATTERY LEVEL: {rover_id} ===")
    try:
        pprint(response.json())
        return response.json()
    except json.JSONDecodeError:
        print(f"Error decoding JSON. Response: {response.text}")
        # If session expired, start a new one
        if "session expired" in response.text.lower() or "invalid session" in response.text.lower():
            print("Session may have expired. Starting a new one...")
            new_session_id = start_session()
            return get_battery_level(new_session_id, rover_id)
        return None

def get_coordinates(session_id, rover_id):
    """Get coordinates of a specific rover."""
    response = requests.get(f"{BASE_URL}/rover/{rover_id}/coordinates", params={"session_id": session_id})
    print(f"\n=== COORDINATES: {rover_id} ===")
    try:
        pprint(response.json())
        return response.json()
    except json.JSONDecodeError:
        print(f"Error decoding JSON. Response: {response.text}")
        # If session expired, start a new one
        if "session expired" in response.text.lower() or "invalid session" in response.text.lower():
            print("Session may have expired. Starting a new one...")
            new_session_id = start_session()
            return get_coordinates(new_session_id, rover_id)
        return None

def fetch_all_data():
    """Fetch all data from the API without moving rovers or assigning tasks."""
    # Get or create session ID
    session_id = get_session_id()
    
    # Test fleet status
    fleet_status = get_fleet_status(session_id)
    
    # Get the list of rovers (from the guide we know there are 5 rovers)
    rovers = ["Rover-1", "Rover-2", "Rover-3", "Rover-4", "Rover-5"]
    
    # For each rover, fetch all data
    for rover_id in rovers:
        # Get rover status
        get_rover_status(session_id, rover_id)
        
        # Get sensor data
        get_sensor_data(session_id, rover_id)
        
        # Get battery level
        get_battery_level(session_id, rover_id)
        
        # Get coordinates
        get_coordinates(session_id, rover_id)
    
    print("\n=== DATA RETRIEVAL COMPLETE ===")

if __name__ == "__main__":
    try:
        fetch_all_data()
    except Exception as e:
        print(f"An error occurred: {e}")