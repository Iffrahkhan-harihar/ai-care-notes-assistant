from app.db.database import engine
from sqlalchemy import text
import json

# Persists processed AI output (summary, risks, actions) into database
def save_summary(data):
    try:
        # Use transactional scope to ensure atomic write
        with engine.begin() as conn:
            summary_data = data.get("summary", {})

            # Insert structured summary data into summaries table
            query = text("""
            INSERT INTO summaries 
            (job_id, file_name, original_text, masked_text, summary, risks, actions)
            VALUES (:job_id, :file_name, :original_text, :masked_text, :summary, :risks, :actions)
            """)

            conn.execute(query, {
                "job_id": data.get("job_id"),
                "file_name": data.get("file_name"),

                # NOTE: original_text should already be cleaned (and ideally masked before storage)
                "original_text": data.get("cleaned_text"),

                # Store PHI-masked version for safe downstream usage
                "masked_text": data.get("masked_text"),

                # Store summary as plain text
                "summary": summary_data.get("summary"),

                # Serialize structured fields as JSON strings for DB storage
                "risks": json.dumps(summary_data.get("risks", [])),
                "actions": json.dumps(summary_data.get("actions", []))
            })

            print("✅ Saved to DB")

    except Exception as e:
        # Log DB failure and propagate exception for upstream handling
        print("❌ DB ERROR:", str(e))
        raise e


# Updates job tracking table with current status and result payload
def update_job_status(job_id, status, result=None):

    # Transaction ensures status and result update happen together
    with engine.begin() as conn:
        res = conn.execute(text("""
            UPDATE jobs
            SET status = :status,
                result = :result
            WHERE job_id = :job_id
        """), {
            "job_id": job_id,
            "status": status,

            # Store minimal result payload (avoid storing sensitive/full raw data)
            "result": json.dumps({
                        "file_name": result.get("file_name"),
                        "masked_text": result.get("masked_text"),
                        "summary": result.get("summary")
                    }) if result else None
        })

        # Debug logs for tracking async job updates
        print(f"🧠 Updating job_id: {job_id}")
        print(f"📊 Rows updated: {res.rowcount}")