import base64
import io
import random
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel
from typing import Annotated

app = FastAPI(title="AI Voice Detection API")

# My security key
VALID_API_KEY = "echolyze_secure_hackathon_key_2026"

# 1. Submission Request Model
class DetectionRequest(BaseModel):
    language: str        # Tamil, English, Hindi, Malayalam, Telugu
    audioFormat: str     # mp3
    audioBase64: str     # The encoded audio string

# 2. Required Response Model
class DetectionResponse(BaseModel):
    status: str
    language: str
    classification: str   # AI_GENERATED or HUMAN
    confidenceScore: float # 0.0 to 1.0
    explanation: str

@app.post("/detect", response_model=DetectionResponse)
async def detect_voice(
    request: DetectionRequest, 
    x_api_key: Annotated[str | None, Header()] = None
):
    # AUTHENTICATION CHECK
    if x_api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid API Key"
        )

    try:
        # AUDIO PROCESSING
        # Decode the base64 string back into audio bytes
        audio_bytes = base64.b64decode(request.audioBase64)
        
        # Check if the file is at least a valid size (e.g., > 100 bytes)
        if len(audio_bytes) < 100:
            raise ValueError("Audio file too small or corrupt")

        # --- AI LOGIC GOES HERE ---
        # For the hackathon, integrate your model here. 
        # For testing the endpoint connection:
        is_ai = random.choice([True, False])
        score = round(random.uniform(0.75, 0.98), 2)
        # --------------------------

        return {
            "status": "success",
            "language": request.language,
            "classification": "AI_GENERATED" if is_ai else "HUMAN",
            "confidenceScore": score,
            "explanation": "High-frequency robotic artifacts detected in speech." if is_ai else "Natural breathing and pitch variations detected."
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

import os
import uvicorn

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(app, host="0.0.0.0", port=port)