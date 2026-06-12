import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

try:
    NASA_API_KEY = st.secrets["NASA_API_KEY"]
except:
    NASA_API_KEY = os.getenv('NASA_API_KEY', 'DEMO_KEY')
if NASA_API_KEY == 'DEMO_KEY':
	print("⚠️  Warning: Using DEMO_KEY - limited API calls allowed")
	print("   Get your own key at https://api.nasa.gov for full access")

BASE_URL = "https://api.nasa.gov"

NEO_ENDPOINT = f"{BASE_URL}/neo/rest/v1/feed"
APOD_ENDPOINT = f"{BASE_URL}/planetary/apod"
DSCOVER_ENDPOINT = f"{BASE_URL}/planetary/earth/imagery"

HAZARD_THRESHOLD_KM = 0.05
DISPLAY_DAYS = 7
DEFAULT_APOD_COUNT = 30

DATA_FOLDER = "data"

ASTEROIDS_FILE = f"{DATA_FOLDER}/asteroids.json"
APOD_FILE = f"{DATA_FOLDER}/apod.json"
EARTH_IMAGE_FILE = f"{DATA_FOLDER}/earth_image.json"

DEBUG_MODE = False

PRINT_API_RESPONSES = False