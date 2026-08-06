from fastapi import FastAPI, HTTPException
from .database import get_cursor
from .schemas import ShortenRequest, ShortenResponse
from psycopg2.errors import UniqueViolation
import random
import string

app = FastAPI(title="URL_Shortener")

# Let's define a random string generation
def generate_code() -> str:
    chars = string.ascii_letters + string.digits
    # Generate a random code of 6 ascii letters and digits
    random_code = "".join(random.choices(chars, k=6))
    return random_code

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

# Define the POST request to Shorten a URL
# We get the url to shorten as a query parameter, not a path parameter
@app.post("/shorten", response_model=ShortenResponse)
def shorten(url: ShortenRequest):
    # Handle if we generate the same random code. 
    for attempt in range(5):
        short_code = generate_code()
        try:
            # commit = True because we need to write to the database
            with get_cursor(commit=True) as cursor:
                cursor.execute("INSERT INTO urls (short_code, long_url) VALUES (%s, %s) RETURNING short_code", (short_code, str(url.url)))
                response = cursor.fetchone()
                return {"short_code": response[0]}
        except UniqueViolation:
            continue
    raise HTTPException(500, "Failed to generate a unique code after 5 attempts")

