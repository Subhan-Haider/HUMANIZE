from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import uvicorn
from dotenv import load_dotenv

# Import the core engine
from transformer.neural import NeuralTextHumanizer

# Initialize Environment
load_dotenv()

app = FastAPI(
    title="BlizFlow API",
    description="Backend API for BlizFlow Neural Humanizer",
    version="3.1.5"
)

# CORS (Allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Engine Instance (Lazy Loading)
neural_engine = None

def get_engine():
    global neural_engine
    if neural_engine is None:
        print("⚡ Loading Neural Engine...")
        neural_engine = NeuralTextHumanizer()
    return neural_engine

# --- Models ---
class HumanizeRequest(BaseModel):
    text: str
    stealth_level: int = 3
    tone: str = "Balanced"
    audience: str = "General"
    preserve_formatting: bool = True
    use_emojis: bool = False
    use_artifacts: bool = False

class HumanizeResponse(BaseModel):
    original_length: int
    humanized_text: str
    humanized_length: int
    processing_time: float

# --- Routes ---
@app.get("/")
def health_check():
    return {"status": "online", "engine": "BlizFlow v3.1.5"}

@app.post("/api/humanize")
async def humanize_text(request: HumanizeRequest):
    try:
        engine = get_engine()
        import time
        start_time = time.time()
        
        # Call the actual Python engine
        result = engine.humanize(
            text=request.text,
            stealth_level=request.stealth_level,
            tone=request.tone,
            audience=request.audience,
            preserve_formatting=request.preserve_formatting,
            use_emojis=request.use_emojis,
            use_artifacts=request.use_artifacts
        )
        
        duration = time.time() - start_time
        
        return {
            "original_length": len(request.text),
            "humanized_text": result,
            "humanized_length": len(result),
            "processing_time": duration
        }
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
