import psycopg2
from dotenv import load_dotenv
import os

# Import all functions from your existing files
from clean_data import fetch_matches, clean_matches
from store_data import get_connection, create_table, insert_matches
from query_data import run_query

load_dotenv()


def run_pipeline():
    print("\n" + "="*60)
    print("  CRICKET DATA PIPELINE STARTING")
    print("="*60)

    # STEP 1: Fetch
    print("\n[Step 1/4] Fetching live match data from CricAPI...")
    raw_matches = fetch_matches()
    print(f"  Fetched: {len(raw_matches)} matches")

    if not raw_matches:
        print("  No data returned. Check your API key or internet connection.")
        return

    # STEP 2: Clean
    print("\n[Step 2/4] Cleaning and extracting useful fields...")
    cleaned = clean_matches(raw_matches)
    print(f"  Cleaned: {len(cleaned)} records ready")

    # STEP 3: Store
    print("\n[Step 3/4] Storing data in PostgreSQL...")
    conn = get_connection()
    create_table(conn)
    insert_matches(conn, cleaned)

    # STEP 4: Query
    print("\n[Step 4/4] Running analytical queries on stored data...")

    run_query(conn, "Total matches in database", """
        SELECT COUNT(*) AS total_matches FROM matches;
    """)

    run_query(conn, "Matches by type", """
        SELECT match_type, COUNT(*) AS total
        FROM matches
        GROUP BY match_type
        ORDER BY total DESC;
    """)

    run_query(conn, "Top 5 most active teams", """
        SELECT team1 AS team, COUNT(*) AS appearances
        FROM matches
        WHERE team1 IS NOT NULL
        GROUP BY team1
        ORDER BY appearances DESC
        LIMIT 5;
    """)

    conn.close()

    print("\n" + "="*60)
    print("  PIPELINE COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_pipeline()