from fastapi import FastAPI, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import uvicorn
import yaml
from pathlib import Path

app = FastAPI()

def get_db():
    with psycopg2.connect( # переменные окружения
        user = os.environ.get("POSTGRES_USER"),
        password = os.environ.get("POSTGRES_PASSWORD"),
        host = os.environ.get("POSTGRES_HOST"),
        port = os.environ.get("POSTGRES_PORT"),
        database = os.environ.get("POSTGRES_DATABASE")
    ) as conn:
        return conn

def config(): # вынесение настроек в конфиг
    # __file__ -> .../git/pythonProject/src/app.py
    # Path(__file__).patent -> .../git/pythonProject/src/
    # Path(__file__).parent.parent -> .../git/pythonProject/
    with open(Path(__file__).parent.parent / "params.yaml", "r") as f:
        return yaml.safe_load(f)

@app.get("/user")
def get_all_users(limit: int = 10, db= Depends(get_db)):
    with db.cursor(cursor_factory = RealDictCursor) as cursor:
        cursor.execute(f"""
    SELECT *
    FROM "user"
    LIMIT %(limit_user)s  -- экранирование: защита от доп sql запросов (sql инъекции)
    """,
        {"limit_user" : limit})
        return cursor.fetchall()

@app.get("/user/feed")
def get_user_feed(user_id : int, limit : int = 10, db = Depends(get_db), config : dict = Depends(config)):
    with db.cursor() as cursor:
        cursor.execute(f"""
        SELECT *
        FROM feed_action
        WHERE user_id  = %(user_id)s
        AND time >= %(start_date)s
        ORDER BY time
        LIMIT %(limit)s
""", {"user_id" : user_id, "limit" : limit, "start_date" : config["feed_start_date"]})
        return cursor.fetchall()

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app)

