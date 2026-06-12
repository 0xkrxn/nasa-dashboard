"""
data_processors.py
Module for processing raw NASA API data into clean Pandas DataFrames
"""

import pandas as pd
from typing import Dict, Optional
from config import HAZARD_THRESHOLD_KM


def process_asteroids(raw_data: Dict) -> Optional[pd.DataFrame]:
    """
    Convert raw asteroid JSON from NASA API into a clean Pandas DataFrame.
    
    This function:
    1. Extracts asteroid data from the raw JSON
    2. Creates columns for: name, date, diameter, distance, speed, hazard_level
    3. Converts units (km to miles where needed)
    4. Handles missing values
    5. Sorts by closest approach first
    
    Args:
        raw_data (Dict): Raw JSON response from fetch_asteroids()
    
    Returns:
        pd.DataFrame: Processed asteroid data with columns:
                      - name: Asteroid name
                      - date: Date of closest approach
                      - diameter_km: Estimated diameter (kilometers)
                      - diameter_miles: Estimated diameter (miles)
                      - distance_km: Distance from Earth (kilometers)
                      - distance_miles: Distance from Earth (miles)
                      - speed_kmh: Relative velocity (km/hour)
                      - speed_mph: Relative velocity (miles/hour)
                      - is_hazardous: Boolean, NASA's hazard classification
                      - hazard_level: Our custom classification (SAFE/MONITOR/HAZARDOUS)
        None: If processing fails
    
    Example:
        >>> asteroids_df = process_asteroids(raw_data)
        >>> print(asteroids_df.head())
        >>> print(asteroids_df.info())
    """
    
    try:
        # Step 1: Extract asteroid data from nested JSON
        print("\n📊 Processing asteroid data with Pandas...")
        
        asteroids_list = []
        
        # The raw data has structure: near_earth_objects[date][list of asteroids]
        near_earth_objects = raw_data.get('near_earth_objects', {})
        
        # Loop through each date
        for date, asteroids_on_date in near_earth_objects.items():
            
            # Loop through each asteroid on that date
            for asteroid in asteroids_on_date:
                
                # Extract basic info
                name = asteroid.get('name', 'Unknown')
                is_hazardous = asteroid.get('is_potentially_hazardous_asteroid', False)
                
                # Extract diameter info
                diameter_data = asteroid.get('estimated_diameter', {})
                diameter_km_range = diameter_data.get('kilometers', {})
                diameter_miles_range = diameter_data.get('miles', {})
                
                # Use average of min and max diameter
                diameter_km = (
                    (diameter_km_range.get('estimated_diameter_min', 0) + 
                     diameter_km_range.get('estimated_diameter_max', 0)) / 2
                ) if diameter_km_range else None
                
                diameter_miles = (
                    (diameter_miles_range.get('estimated_diameter_min', 0) + 
                     diameter_miles_range.get('estimated_diameter_max', 0)) / 2
                ) if diameter_miles_range else None
                
                # Extract close approach data (there might be multiple)
                close_approach_data = asteroid.get('close_approach_data', [])
                
                if close_approach_data:
                    # Use the first (closest) approach
                    approach = close_approach_data[0]
                    
                    # Extract date
                    approach_date = approach.get('close_approach_date', date)
                    
                    # Extract distance
                    distance_data = approach.get('miss_distance', {})
                    distance_km = float(distance_data.get('kilometers', 0))
                    distance_miles = float(distance_data.get('miles', 0))
                    
                    # Extract speed
                    velocity_data = approach.get('relative_velocity', {})
                    speed_kmh = float(velocity_data.get('kilometers_per_hour', 0))
                    speed_mph = float(velocity_data.get('miles_per_hour', 0))
                    
                    # Create a row for this asteroid
                    asteroid_row = {
                        'name': name,
                        'date': approach_date,
                        'diameter_km': diameter_km,
                        'diameter_miles': diameter_miles,
                        'distance_km': distance_km,
                        'distance_miles': distance_miles,
                        'speed_kmh': speed_kmh,
                        'speed_mph': speed_mph,
                        'is_hazardous': is_hazardous
                    }
                    
                    asteroids_list.append(asteroid_row)
        
        # Step 2: Create DataFrame from list of dictionaries
        if not asteroids_list:
            print("❌ No asteroid data found to process")
            return None
        
        df = pd.DataFrame(asteroids_list)
        
        # Step 3: Add hazard level classification (our custom column)
        df['hazard_level'] = df.apply(_classify_hazard, axis=1)
        
        # Step 4: Sort by closest approach (distance)
        df = df.sort_values('distance_km').reset_index(drop=True)
        
        # Step 5: Convert data types
        df['date'] = pd.to_datetime(df['date'])
        df['is_hazardous'] = df['is_hazardous'].astype(bool)
        
        print(f"✅ Successfully processed {len(df)} asteroids")
        print(f"   Date range: {df['date'].min().date()} to {df['date'].max().date()}")
        print(f"   Closest approach: {df['distance_km'].min():.2f} km away")
        print(f"   Farthest approach: {df['distance_km'].max():.2f} km away")
        
        return df
    
    except Exception as e:
        print(f"❌ Error processing asteroid data: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def _classify_hazard(row):
    """
    Helper function to classify asteroid hazard level based on distance.
    
    Classification:
    - HAZARDOUS: Less than 0.05 million km (very close)
    - MONITOR: Between 0.05 and 0.1 million km (getting closer)
    - SAFE: More than 0.1 million km (far away)
    
    Args:
        row: DataFrame row with distance_km
    
    Returns:
        str: Hazard level classification
    """
    distance_km = row['distance_km']
    
    if distance_km < 50000:  # 0.05 million km
        return 'HAZARDOUS'
    elif distance_km < 100000:  # 0.1 million km
        return 'MONITOR'
    else:
        return 'SAFE'


def get_summary_stats(df: pd.DataFrame) -> Dict:
    """
    Get summary statistics about the asteroid data.
    
    Args:
        df (pd.DataFrame): Processed asteroid DataFrame
    
    Returns:
        Dict: Summary statistics including:
              - total_count: Total number of asteroids
              - hazardous_count: Count of hazardous asteroids
              - average_diameter: Average diameter in km
              - largest_diameter: Largest asteroid
              - closest_approach: Closest distance in km
              - average_speed: Average speed in km/h
    
    Example:
        >>> stats = get_summary_stats(df)
        >>> print(f"Found {stats['hazardous_count']} hazardous asteroids")
    """
    
    try:
        stats = {
            'total_count': len(df),
            'hazardous_count': len(df[df['is_hazardous'] == True]),
            'monitor_count': len(df[df['hazard_level'] == 'MONITOR']),
            'safe_count': len(df[df['hazard_level'] == 'SAFE']),
            'average_diameter_km': df['diameter_km'].mean(),
            'largest_diameter_km': df['diameter_km'].max(),
            'smallest_diameter_km': df['diameter_km'].min(),
            'closest_approach_km': df['distance_km'].min(),
            'farthest_approach_km': df['distance_km'].max(),
            'average_speed_kmh': df['speed_kmh'].mean(),
            'fastest_speed_kmh': df['speed_kmh'].max(),
        }
        return stats
    
    except Exception as e:
        print(f"❌ Error calculating statistics: {str(e)}")
        return None


def get_hazardous_asteroids(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter and return only the hazardous asteroids.
    
    Args:
        df (pd.DataFrame): Processed asteroid DataFrame
    
    Returns:
        pd.DataFrame: Subset of df with only hazardous asteroids
    
    Example:
        >>> hazardous = get_hazardous_asteroids(df)
        >>> print(f"Watch out! {len(hazardous)} hazardous asteroids approaching!")
    """
    
    hazardous = df[df['hazard_level'] == 'HAZARDOUS'].copy()
    return hazardous.sort_values('distance_km')


def get_asteroids_by_date(df: pd.DataFrame) -> Dict:
    """
    Group asteroids by their closest approach date.
    
    Args:
        df (pd.DataFrame): Processed asteroid DataFrame
    
    Returns:
        Dict: Dictionary with dates as keys and DataFrames as values
    
    Example:
        >>> by_date = get_asteroids_by_date(df)
        >>> for date, asteroids in by_date.items():
        ...     print(f"{date}: {len(asteroids)} asteroids")
    """
    
    grouped = {}
    for date, group in df.groupby('date'):
        grouped[date.strftime('%Y-%m-%d')] = group
    
    return grouped


def print_asteroid_summary(df: pd.DataFrame):
    """
    Print a nice summary of the asteroid data to console.
    
    Args:
        df (pd.DataFrame): Processed asteroid DataFrame
    
    Example:
        >>> print_asteroid_summary(df)
    """
    
    stats = get_summary_stats(df)
    
    print("\n" + "=" * 70)
    print("📊 ASTEROID DATA SUMMARY")
    print("=" * 70)
    
    print(f"\n🔢 Total Asteroids: {stats['total_count']}")
    print(f"\n⚠️  Hazard Classification:")
    print(f"   🔴 HAZARDOUS (< 50,000 km): {stats['hazardous_count']}")
    print(f"   🟡 MONITOR (50k - 100k km): {stats['monitor_count']}")
    print(f"   🟢 SAFE (> 100,000 km): {stats['safe_count']}")
    
    print(f"\n📏 Diameter:")
    print(f"   Largest: {stats['largest_diameter_km']:.2f} km")
    print(f"   Average: {stats['average_diameter_km']:.2f} km")
    print(f"   Smallest: {stats['smallest_diameter_km']:.2f} km")
    
    print(f"\n📍 Distance from Earth:")
    print(f"   Closest: {stats['closest_approach_km']:.2f} km")
    print(f"   Farthest: {stats['farthest_approach_km']:.2f} km")
    
    print(f"\n⚡ Speed:")
    print(f"   Fastest: {stats['fastest_speed_kmh']:.2f} km/h")
    print(f"   Average: {stats['average_speed_kmh']:.2f} km/h")
    
    print("\n" + "=" * 70)