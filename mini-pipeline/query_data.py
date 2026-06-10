import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

def run_query(conn, title, query):
    """Run a SQL query and print results in a readable format."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        headers = [desc[0] for desc in cur.description]
        print(" | ".join(headers))
        print("-" * 60)
        for row in rows:
            print(" | ".join(str(val) for val in row))
    print(f"Total rows: {len(rows)}")

def main():
    conn = get_connection()

    # Q1: How many matches are stored?
    run_query(conn, "Total matches in database", """
        SELECT COUNT(*) AS total_matches FROM matches;
    """)

    # Q2: How many matches per match type?
    run_query(conn, "Matches by type (T20, ODI, Test)", """
        SELECT match_type, COUNT(*) AS total
        FROM matches
        GROUP BY match_type
        ORDER BY total DESC;
    """)

    # Q3: Which teams appear most often?
    run_query(conn, "Top 10 most active teams", """
        SELECT team1 AS team, COUNT(*) AS appearances
        FROM matches
        WHERE team1 IS NOT NULL
        GROUP BY team1
        ORDER BY appearances DESC
        LIMIT 10;
    """)

    # Q4: Matches that are still in progress
    run_query(conn, "Live / in-progress matches", """
        SELECT name, status
        FROM matches
        WHERE status ILIKE '%progress%'
           OR status ILIKE '%live%'
           OR status ILIKE '%yet to bat%';
    """)

    # Q5: Matches with no result (rain, cancelled)
    run_query(conn, "Matches with no result", """
        SELECT name, status
        FROM matches
        WHERE status ILIKE '%no result%'
           OR status ILIKE '%rain%'
           OR status ILIKE '%cancel%';
    """)

    conn.close()

if __name__ == "__main__":
    main()