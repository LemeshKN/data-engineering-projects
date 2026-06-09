import psycopg2
from dotenv import load_dotenv
import os
from clean_data  import fetch_matches, clean_matches  # reuse your Day 2 functions

load_dotenv()


def get_connection():
    """Create and return a PostgreSQL connection."""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn


def create_table(conn):
    """Create the matches table if it doesn't already exist."""
    query = """
        CREATE TABLE IF NOT EXISTS matches (
            match_id    TEXT PRIMARY KEY,
            name        TEXT,
            status      TEXT,
            match_type  TEXT,
            venue       TEXT,
            date        TEXT,
            team1       TEXT,
            team2       TEXT,
            score       TEXT
        );
    """
    with conn.cursor() as cur:
        cur.execute(query)
    conn.commit()
    print("Table ready.")


def insert_matches(conn, matches):
    """
    Insert cleaned match records into the database.
    ON CONFLICT DO NOTHING means: if a match_id already exists,
    skip it instead of crashing. This prevents duplicate rows
    every time you run the script.
    """
    query = """
        INSERT INTO matches (match_id, name, status, match_type, venue, date, team1, team2, score)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (match_id) DO NOTHING;
    """
    inserted = 0
    skipped = 0

    with conn.cursor() as cur:
        for match in matches:
            # Skip records with no match_id — can't store without a primary key
            if not match.get("match_id"):
                skipped += 1
                continue

            cur.execute(query, (
                match["match_id"],
                match["name"],
                match["status"],
                match["match_type"],
                match["venue"],
                match["date"],
                match["team1"],
                match["team2"],
                match["score"],
            ))

            if cur.rowcount == 1:
                inserted += 1
            else:
                skipped += 1

    conn.commit()
    print(f"Inserted: {inserted} new rows | Skipped (duplicates or missing ID): {skipped}")


def main():
    print("Fetching matches...")
    raw = fetch_matches()
    print(f"Fetched: {len(raw)} matches")

    cleaned = clean_matches(raw)

    print("Connecting to database...")
    conn = get_connection()

    create_table(conn)
    insert_matches(conn, cleaned)

    conn.close()
    print("Done. Connection closed.")


if __name__ == "__main__":
    main()