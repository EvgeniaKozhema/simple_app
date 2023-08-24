from fastapi import FastAPI, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import uvicorn

app = FastAPI()

def get_db():
    with psycopg2.connect(
        user = os.environ.get("POSTGRES_USER"),
        password = os.environ.get("POSTGRES_PASSWORD"),
        host = os.environ.get("POSTGRES_HOST"),
        port = os.environ.get("POSTGRES_PORT"),
        database = os.environ.get("POSTGRES_DATABASE")
    ) as conn:
        return conn

@app.get("/user")
def get_all_users(limit: int = 10, db= Depends(get_db)):
    with db.cursor(cursor_factory = RealDictCursor) as cursor:
        cursor.execute(f"""
    SELECT *
    FROM "user"
    LIMIT {limit}
    """)
        return cursor.fetchall()

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app)

