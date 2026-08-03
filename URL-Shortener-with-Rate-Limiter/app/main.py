from fastapi import FastAPI

app = FastAPI(title="URL_Shortener")

# Define an initial health endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}