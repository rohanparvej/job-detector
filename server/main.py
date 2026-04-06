from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ml.predict import predict  # Import our clean function
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(message)s" # Matches Uvicorn style
)
logger = logging.getLogger("my_app")

app = FastAPI()
# THIS IS THE FIX FOR THE CORS ERROR
origins = ["http://localhost:5500",          # For local testing (Live Server)
    "http://127.0.0.1:5500",         # For local testing
    "https://job-detector.pages.dev" # Your ACTUAL Cloudflare URL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allow your Live Server origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobRequest(BaseModel):
    text: str
    extra_features: list

@app.post("/predict")
async def run_prediction(data: JobRequest):
    # Now it clearly calls the imported function
    result = predict(data.text, data.extra_features)
    logger.info(f"Prediction made: {result}")
    return result

@app.get("/")
def health_check():
    logger.info("--- Health Check Triggered ---")
    return {"status": "✅online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
