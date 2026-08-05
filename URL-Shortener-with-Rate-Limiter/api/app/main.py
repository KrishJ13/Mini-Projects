from fastapi import FastAPI
from .database import get_cursor

app = FastAPI(title="URL_Shortener")

# Define an initial health endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Define a db check endpoint
@app.get("/db-check")
async def db_check():
    # Use the contextmanager defined in database.py
    with get_cursor() as cursor:
        cursor.execute("SELECT version();")
        response = cursor.fetchone()
    return {"postgres_version" : response[0]}

