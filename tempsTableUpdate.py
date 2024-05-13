#As I forgot to initially create the serial id in the temperatures table I have to update it to not loose the data

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("DATABASE_URL"),
    port=os.getenv("PORT")
)
conn.autocommit = True
modify_temps_table = """ALTER TABLE temperatures ADD COLUMN id SERIAL PRIMARY KEY;"""

try:
    with conn.cursor() as cur:
        cur.execute(modify_temps_table)
        conn.commit()

    print({"message": "Table temperatures modified successfully."}, 200)
except psycopg2.DatabaseError as db_error:
    # Handle database-related errors
    print("Database error: %s", str(db_error))
except Exception as e:
    # Log unexpected errors
    print("An unexpected error occurred: %s", str(e))

conn.close()
