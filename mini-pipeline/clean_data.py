import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("CRICKET_API_KEY")

def fetch_matches():
    """Fetch raw match data from CricAPI."""
    url = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: API returned status {response.status_code}")
        return []
    
    data = response.json()
    return data.get("data", [])  # Returns empty list if 'data' key is missing


def clean_matches(raw_matches):
    """Extract useful fields from raw match list."""
    cleaned = []

    for match in raw_matches:
        # .get() returns None if the key doesn't exist — no crash
        record = {
            "match_id":   match.get("id"),
            "name":       match.get("name"),
            "status":     match.get("status"),
            "match_type": match.get("matchType"),
            "venue":      match.get("venue"),
            "date":       match.get("date"),
            "team1":      match.get("teams", [None, None])[0],
            "team2":      match.get("teams", [None, None])[1],
            "score":      extract_score(match.get("score", [])),
        }
        cleaned.append(record)

    return cleaned


def extract_score(score_list):
    """
    score_list looks like:
    [{"r": 245, "w": 6, "o": 48.3, "inning": "India Inning 1"}, ...]
    
    We join all innings into one readable string.
    If no scores yet (match not started), return 'No score yet'.
    """
    if not score_list:
        return "No score yet"
    
    parts = []
    for inning in score_list:
        inning_name = inning.get("inning", "Unknown Inning")
        runs        = inning.get("r", 0)
        wickets     = inning.get("w", 0)
        overs       = inning.get("o", 0)
        parts.append(f"{inning_name}: {runs}/{wickets} ({overs} ov)")
    
    return " | ".join(parts)


def main():
    print("Fetching matches...")
    raw_matches = fetch_matches()
    print(f"Total matches fetched: {len(raw_matches)}\n")

    if not raw_matches:
        print("No data to clean.")
        return

    cleaned = clean_matches(raw_matches)

    # Create DataFrame
    df = pd.DataFrame(cleaned)

    # Pandas display settings — show full text, no truncation
    pd.set_option("display.max_colwidth", 50)
    pd.set_option("display.max_rows", 100)
    pd.set_option("display.width", 200)

    print("=== Cleaned Match Data ===\n")
    print(df.to_string(index=False))
    print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")


if __name__ == "__main__":
    main()