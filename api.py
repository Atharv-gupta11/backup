from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import json
from main import analyze_post

app = FastAPI(title="ShieldAI API", version="2.5")

# FIX: Allow CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static files to serve images back to the frontend
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

@app.get("/")
def health_check():
    return {"status": "online", "model": "ShieldAI v2.5 (Groq/Llama 3.3)"}

@app.post("/analyze")
async def analyze_media(file: UploadFile = File(...), claim: str = Form(...)):
    try:
        # 1. Save File Locally
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 2. Run Analysis Pipeline
        # We reuse the exact same logic from main.py to ensure consistency
        results = analyze_post(file_path, claim)
        
        # 3. Augment results with URL for the frontend
        results["media_url"] = f"http://localhost:8000/static/{file.filename}"
        
        return results
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
async def log_feedback(
    file_name: str = Form(...), 
    feedback_type: str = Form(...), # "false_positive" or "false_negative"
    notes: str = Form(None)
):
    """
    Deliverable #7: User Feedback Loop
    Logs user corrections to a JSON line file for future fine-tuning.
    """
    log_entry = {
        "file": file_name,
        "type": feedback_type,
        "notes": notes or "User flagged via GUI"
    }
    
    with open("feedback_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
        
    return {"status": "logged", "message": "Feedback received. Thank you for training ShieldAI!"}

@app.get("/evaluate/cache")
async def get_cached_metrics():
    """Retrieve the last saved evaluation results instantly."""
    metrics_file = "evaluation_metrics.json"
    if os.path.exists(metrics_file):
        with open(metrics_file, "r") as f:
            return json.load(f)
    return None

@app.post("/evaluate")
async def trigger_evaluation():
    """Run the full evaluation pipeline and return new metrics."""
    try:
        # Import dynamically to ensure it picks up the latest changes
        from scripts.evaluate import run_evaluation
        metrics = run_evaluation()
        return metrics
    except Exception as e:
        print(f"Evaluation Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
