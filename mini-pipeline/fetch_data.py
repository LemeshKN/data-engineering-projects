import requests
import json

# Your API key from cricapi.com
API_KEY = "78bcad75-8cc6-4dc7-aba1-85bc69ad2598"

# URL to get current cricket matches
url = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0"

# Fetch the data
response = requests.get(url)

# Check if it worked
if response.status_code == 200:
    data = response.json()
    print("Data fetched successfully!")
    print(json.dumps(data, indent=2))  # prints clean readable JSON
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")