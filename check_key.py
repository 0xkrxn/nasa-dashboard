from config import NASA_API_KEY

print(f"API Key being used: {NASA_API_KEY}")
print(f"Lenght: {len(NASA_API_KEY) if NASA_API_KEY else 0}")
print(f"First 10 chars: {NASA_API_KEY[:10] if NASA_API_KEY else 'NONE'}")

if NASA_API_KEY == 'DEMO_KEY':
	print("\n⚠️ You're using DEMO_KEY - this has very limited access!")
	print("		Get your own key at: https://api.nasa.gov")