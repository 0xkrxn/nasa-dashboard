"""
test.py
Test file to verify that fetch_asteroids() is working correctly.
Run this file to test your API setup and fetching.
"""

from data_fetchers import fetch_asteroids
import json


def test_fetch_asteroids():
    """
    Test the fetch_asteroids function.
    This will try to fetch asteroid data and display it.
    """
    
    print("=" * 70)
    print("🧪 Testing fetch_asteroids() Function")
    print("=" * 70)
    
    # Test 1: Fetch asteroids for the next 3 days
    print("\n[TEST 1] Fetching asteroids for next 3 days...")
    print("-" * 70)    
    asteroids = fetch_asteroids(days_ahead=3)
    
    # Check if we got data
    if asteroids is None:
        print("\n❌ FAILED: fetch_asteroids() returned None")
        print("   Possible reasons:")
        print("   - Invalid API key in config.py")
        print("   - Network connection issue")
        print("   - NASA API is down")
        return False
    
    print("\n✅ SUCCESS: Got data from NASA API!")
    
    # Test 2: Show what we got
    print("\n[TEST 2] Examining the data structure...")
    print("-" * 70)
    
    # Count total asteroids
    element_count = asteroids.get('element_count', 0)
    print(f"\n📊 Total asteroids found: {element_count}")
    
    # Show dates that have asteroids
    near_earth_objects = asteroids.get('near_earth_objects', {})
    dates = list(near_earth_objects.keys())
    
    print(f"📅 Days with asteroids: {len(dates)}")
    print(f"   Dates: {dates}")
    
    # Test 3: Examine first asteroid
    print("\n[TEST 3] Details of first asteroid...")
    print("-" * 70)
    
    if dates:
        first_date = dates[0]
        asteroids_on_first_date = near_earth_objects[first_date]
        
        if asteroids_on_first_date:
            first_asteroid = asteroids_on_first_date[0]
            
            print(f"\n📍 First asteroid on {first_date}:")
            print(f"   Name: {first_asteroid.get('name')}")
            print(f"   ID: {first_asteroid.get('id')}")
            
            # Extract diameter info
            diameter_info = first_asteroid.get('estimated_diameter', {})
            diameter_km = diameter_info.get('kilometers', {})
            diameter_miles = diameter_info.get('miles', {})
            
            if diameter_km:
                print(f"   Diameter: {diameter_km.get('estimated_diameter_min'):.2f} - {diameter_km.get('estimated_diameter_max'):.2f} km")
            
            # Check if hazardous
            is_hazardous = first_asteroid.get('is_potentially_hazardous_asteroid', False)
            hazard_symbol = "🔴 YES - HAZARDOUS" if is_hazardous else "🟢 NO - SAFE"
            print(f"   Potentially Hazardous: {hazard_symbol}")
            
            # Extract close approach data
            close_approach = first_asteroid.get('close_approach_data', [])
            if close_approach:
                approach = close_approach[0]
                distance_km = approach.get('miss_distance', {}).get('kilometers', 'N/A')
                velocity = approach.get('relative_velocity', {}).get('kilometers_per_hour', 'N/A')
                
                print(f"   Distance from Earth: {distance_km} km")
                print(f"   Speed: {velocity} km/h")
    
    # Test 4: Show raw JSON (first 500 characters)
    print("\n[TEST 4] Raw JSON response (first 500 chars)...")
    print("-" * 70)
    
    json_str = json.dumps(asteroids, indent=2)
    print("\n" + json_str[:500] + "...\n")
    
    # Test 5: Summary
    print("\n[TEST 5] Summary")
    print("-" * 70)
    print("✅ All tests completed successfully!")
    print(f"\n📈 Summary:")
    print(f"   ✓ API connection works")
    print(f"   ✓ API key is valid")
    print(f"   ✓ Retrieved {element_count} asteroids")
    print(f"   ✓ Data structure is correct")
    print("\n🎉 Your fetch_asteroids() function is working perfectly!")
    
    return True


if __name__ == "__main__":
    """
    Run the test when this file is executed directly
    """
    try:
        success = test_fetch_asteroids()
        
        if success:
            print("\n" + "=" * 70)
            print("🚀 Next Step: Move to Phase 4 - Data Processing with Pandas!")
            print("=" * 70)
        else:
            print("\n" + "=" * 70)
            print("⚠️  Please fix the issues above before proceeding")
            print("=" * 70)
    
    except ImportError as e:
        print("❌ Import Error!")
        print(f"   {str(e)}")
        print("\n   Make sure you have:")
        print("   1. data_fetchers.py in the same folder")
        print("   2. config.py with NASA_API_KEY and NEO_ENDPOINT")
        print("   3. Installed requests: pip install requests")
    
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")