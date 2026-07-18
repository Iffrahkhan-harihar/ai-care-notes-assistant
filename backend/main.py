# Import speech-to-text service to convert audio → transcript
from app.services.speech_service import transcribe_audio

# Enable CORS for frontend-backend communication
from fastapi.middleware.cors import CORSMiddleware

# Queue service to send jobs for async processing
from app.queue.queue_service import send_to_queue

# FastAPI core imports for API creation and file handling
from fastapi import FastAPI, UploadFile, File

# API key authentication dependency
from app.core.auth import verify_api_key

# Database engine for SQL operations
from app.db.database import engine

# Dependency injection for API security
from fastapi import Depends

# SQL query execution
from sqlalchemy import text

# Utilities for unique job IDs and JSON handling
import uuid
import json
import os

# Initialize FastAPI application
app = FastAPI()

# Endpoint to upload audio, transcribe it, and trigger async processing
@app.post("/summarize-audio")
async def summarize_audio(file: UploadFile = File(...), api_key: str = Depends(verify_api_key)):

    # Generate unique job ID for tracking
    job_id = str(uuid.uuid4())

    # Temporarily save uploaded audio file
    file_path = f"temp_{job_id}.mp3"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Convert audio → text using Azure Speech Service
    transcript = transcribe_audio(file_path)

    # Delete temp file after processing
    os.remove(file_path)

    # Insert job into DB with initial "processing" status
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO jobs (job_id, status)
            VALUES (:job_id, 'processing')
        """), {"job_id": job_id})

    # Send transcript to Service Bus queue for background processing
    send_to_queue({
        "job_id": job_id,
        "note_text": transcript
    })

    # Return job ID so frontend can poll status
    return {
        "status": "queued",
        "job_id": job_id,
        "transcript_preview": transcript[:100]  # small preview for UX
    }


# Endpoint to check job status and fetch result
@app.get("/job/{job_id}")
def get_job_status(job_id: str, api_key: str = Depends(verify_api_key)):

    # Log incoming job request for debugging
    print(f"🔎 API fetching job_id: {job_id}")

    # Query DB for job status and result
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT status, result
            FROM dbo.jobs
            WHERE job_id = :job_id
        """), {"job_id": job_id}).fetchone()

    # Handle case where job does not exist
    if not result:
        print("❌ API: Job NOT FOUND")
        return {"error": "Job not found"}

    print(f"📊 API sees status: {result.status}")

    # If processing complete → return parsed JSON result
    if result.status == "completed":
        return {
            "status": "completed",
            "result": json.loads(result.result)
        }

    # Otherwise return current status (processing/failed)
    return {"status": result.status}


# Enable CORS (allow frontend access — restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ open for dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)