"""
data_fetchers.py
Module for fetching data from NASA APIs
"""

import requests
from datetime import datetime, timedelta
from typing import Optional, Dict
from config import NASA_API_KEY, NEO_ENDPOINT


def fetch_asteroids(days_ahead: int = 7) -> Optional[Dict]:
    """
    Fetch near-Earth asteroids for the next N days from NASA's NEO API.
    """
    
    # Validate API key
    if not NASA_API_KEY:
        print("❌ Error: NASA_API_KEY not found in config.py")
        return None
    
    try:
        # Calculate date range
        today = datetime.now()
        start_date = today.strftime('%Y-%m-%d')
        end_date = (today + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
        
        print(f"\n📡 Fetching asteroids from {start_date} to {end_date}...")
        print(f"   Looking {days_ahead} days ahead")
        
        # Build API parameters
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'api_key': NASA_API_KEY
        }
        
        # Make GET request
        response = requests.get(NEO_ENDPOINT, params=params, timeout=10)
        response.raise_for_status()
        
        # Parse and return JSON
        data = response.json()
        
        element_count = data.get('element_count', 0)
        num_days = len(data.get('near_earth_objects', {}))
        
        print(f"✅ Success! Found {element_count} asteroids across {num_days} days")
        
        return data
    
    except requests.exceptions.Timeout:
        print("❌ Error: Request timed out (took too long)")
        return None
    
    except requests.exceptions.ConnectionError:
        print("❌ Error: Network connection failed")
        return None
    
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        
        if status_code == 401:
            print("❌ Error: Invalid API key")
            print("   Fix: Check NASA_API_KEY in config.py or .env file")
        elif status_code == 429:
            print("❌ Error: Rate limit exceeded. Wait a few seconds and try again.")
        else:
            print(f"❌ HTTP Error {status_code}")
        
        return None
    
    except ValueError as e:
        print(f"❌ Error: Invalid response from API - {str(e)}")
        return None
    
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {str(e)}")
        return None