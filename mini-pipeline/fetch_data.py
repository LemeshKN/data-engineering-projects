import requests
import json
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("CRICKET_API_KEY")

# URL to get current cricket matches
url = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0"

# Fetch the data
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.Timeout:
    print("API request timed out. Check your internet connection.")
    exit()
except requests.exceptions.ConnectionError:
    print("Connection error - cannot reach CricAPI.")
    exit()
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
    exit()

# Check if it worked
if response.status_code == 200:
    data = response.json()
    print("Data fetched successfully!")
    print(json.dumps(data, indent=2))
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
