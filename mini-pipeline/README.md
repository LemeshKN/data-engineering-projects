

# Cricket Data Pipeline

A data engineering mini-project that fetches live cricket match data, 
cleans it, stores it in a PostgreSQL database, and runs SQL queries on it.

## What this pipeline does

1. Fetches live cricket match data from CricAPI (59+ matches)
2. Cleans raw JSON and extracts useful fields into a structured format
3. Stores cleaned data in a PostgreSQL database table
4. Runs analytical SQL queries on the stored data

## Tech stack

- Python 3.11
- requests, pandas, psycopg2, python-dotenv
- PostgreSQL 16
- CricAPI (free tier)

## Project structure

```
mini-pipeline/
├── pipeline.py       # Main script — runs all steps in order
├── fetch_data.py     # Step 1: fetch from CricAPI
├── clean_data.py     # Step 2: clean raw JSON
├── store_data.py     # Step 3: store in PostgreSQL
├── query_data.py     # Step 4: SQL analytical queries
├── .env.example      # Environment variable template
├── .gitignore        # Hides .env and pycache
└── README.md
```

## How to run

1. Clone the repo
2. Install dependencies: pip install requests pandas psycopg2-binary python-dotenv
3. Copy `.env.example` to `.env` and fill in your API key and database credentials
4. Create a PostgreSQL database called `cricket_db`
5. Run the pipeline: python pipeline.py

## Sample output

============================================================
  CRICKET DATA PIPELINE STARTING
============================================================

[Step 1/4] Fetching live match data from CricAPI...
  Fetched: 25 matches

[Step 2/4] Cleaning and extracting useful fields...
  Cleaned: 25 records ready

[Step 3/4] Storing data in PostgreSQL...
Table ready.
Inserted: 13 new rows | Skipped (duplicates or missing ID): 12

[Step 4/4] Running analytical queries on stored data...

============================================================
  Total matches in database
============================================================
total_matches
------------------------------------------------------------
38
Total rows: 1

============================================================
  Matches by type
============================================================
match_type | total
------------------------------------------------------------
t20 | 35
odi | 3
Total rows: 2

============================================================
  Top 5 most active teams
============================================================
team | appearances
------------------------------------------------------------
Bundelkhand Bulls | 3
Indore Pink Panthers | 2
Nigeria Women | 2
Royal Nimar Eagles | 2
Netherlands Women | 2
Total rows: 5

============================================================
  PIPELINE COMPLETE
============================================================

## What I learned

- How to consume a REST API and handle JSON responses
- Data cleaning with pandas
- Connecting Python to PostgreSQL using psycopg2
- Writing analytical SQL (GROUP BY, ORDER BY, aggregations)
- Structuring code into a reusable pipeline
- Git version control and GitHub
