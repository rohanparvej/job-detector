from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ml.predict import predict
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(message)s"
)
logger = logging.getLogger("my_app")

app = FastAPI()

# Optional: You can keep CORS open or restrict it since frontend/backend are bundled
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, images) so your HTML can load assets
# Assumes a folder named 'static' in your root directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates directory for your index.html
templates = Jinja2Templates(directory="templates")

class JobRequest(BaseModel):
    text: str
    extra_features: list

@app.get("/")
async def serve_frontend(request: Request):
    logger.info("--- Frontend Loaded ---")
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )

@app.get("/health")
def health_check():
    logger.info("--- Health Check Triggered ---")
    return {"status": "✅online"}

@app.post("/predict")
async def run_prediction(data: JobRequest):
    result = predict(data.text, data.extra_features)
    logger.info(f"Prediction made: {result}")
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
