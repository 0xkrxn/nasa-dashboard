print("=" * 70)
print("🔍 Debugging API Key Setup")
print("=" * 70)

print("\n[STEP 1] Checking .env file...")
import os

if os.path.exists('.env'):
	print("✅ .env file exists")
	with open('.env', 'r') as f:
		content = f.read()
		print(f"Content: {content}")
else:
	print("❌ .env file NOT found")


print("\n[STEP 2] Checking config.py imports...")
try:
	from config import NASA_API_KEY, NEO_ENDPOINT
	print("✅ config.py imported successfully")
	print(f"	NASA_API_KEY = '{NASA_API_KEY}'")
	print(f"	NEO_ENDPOINT = '{NEO_ENDPOINT}'")
except Exception as e:
	print(f"❌ Error importing config: {e}")

print("\n[STEP 3] API Key Details...")
from config import NASA_API_KEY

if NASA_API_KEY:
	print(f"✅ API Key is set")
	print(f"   Length: {len(NASA_API_KEY)} characters")
	print(f"   First 5 chars: {NASA_API_KEY[:5]}")
	print(f"   Last 5 chars: {NASA_API_KEY[-5:]}")

	if NASA_API_KEY == 'DEMO_KEY':
		print(f"	⚠️ Using DEMO_KEY (limited access)")
	else:
		print(f"	✅ Using a real API key")
else:
	print(f"❌ API Key is empty or None")


print("\n[STEP 4] Testing API connection...")
import requests
from datetime import datetime, timedelta

try:
    today = datetime.now()
    start_date = today.strftime('%Y-%m-%d')
    end_date = (today + timedelta(days=1)).strftime('%Y-%m-%d')
    
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': NASA_API_KEY
    }
    
    print(f"Making request with:")
    print(f"   Start: {start_date}")
    print(f"   End: {end_date}")
    print(f"   API Key: {NASA_API_KEY[:10]}...")
    
    response = requests.get(
        'https://api.nasa.gov/neo/rest/v1/feed',
        params=params,
        timeout=10
    )
    
    print(f"\n📡 Response Status: {response.status_code}")

    if response.status_code == 200:
        print("✅ SUCCESS! API is working!")
        data = response.json()
        print(f"   Found {data.get('element_count')} asteroids")
    elif response.status_code == 403:
        print("❌ ERROR 403 (Forbidden)")
        print("   Your API key is invalid or doesn't have access")
        print("   Get a new key at: https://api.nasa.gov")
    elif response.status_code == 401:
        print("❌ ERROR 401 (Unauthorized)")
        print("   Invalid API key format")
    else:
        print(f"❌ ERROR {response.status_code}")
        print(f"   Response: {response.text[:200]}")

except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {str(e)}")

print("\n" + "=" * 70)