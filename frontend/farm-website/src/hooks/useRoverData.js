// hooks/useRoverData.js
import { useState, useEffect, useCallback } from 'react';

// Update this to your FastAPI server's address
const API_BASE_URL = "http://localhost:8000/api";

export default function useRoverData(refreshInterval = null) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${API_BASE_URL}/all-rover-data`);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API error: ${response.status} - ${errorText}`);
      }
      
      const result = await response.json();
      
      if (result.status !== 'success') {
        throw new Error(`API returned error status: ${JSON.stringify(result)}`);
      }
      
      setData(result.data);
      return result.data;
    } catch (err) {
      console.error('Error fetching rover data:', err);
      setError('Failed to retrieve API data: ' + (err.message || 'Unknown error'));
      return null;
    } finally {
      setLoading(false);
    }
  }, []);
  
  const refetch = useCallback(async () => {
    setLoading(true);
    return await fetchData();
  }, [fetchData]);
  
  useEffect(() => {
    // Only fetch data on client side
    if (typeof window !== 'undefined') {
      // Initial data fetch
      fetchData();
      
      // Set up interval for refreshing data
      let intervalId = null;
      if (refreshInterval && refreshInterval > 0) {
        intervalId = setInterval(() => {
          fetchData().catch(err => {
            console.error('Error in refresh interval:', err);
          });
        }, refreshInterval);
      }
      
      // Clean up interval on component unmount
      return () => {
        if (intervalId) {
          clearInterval(intervalId);
        }
      };
    }
  }, [fetchData, refreshInterval]);
  
  return { data, loading, error, refetch };
}