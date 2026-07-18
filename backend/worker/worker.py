# Background worker that continuously consumes messages from Azure Service Bus,
# processes notes through the pipeline, updates job status, and stores results

from pathlib import Path
import sys

# Ensure project root is in path so worker can import app modules correctly
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.db_service import save_summary, update_job_status
from app.services.pipeline import process_note
from azure.servicebus import ServiceBusClient
from app.core.keyvault import get_secret
from app.db.database import engine
from sqlalchemy import text
import json

# Load Service Bus connection details securely from Azure Key Vault
connection_str = get_secret("service-bus-connection")
queue_name = "notes-queue"

# Main worker loop that listens to queue, processes jobs, and handles success/failure states
def start_worker():
    with ServiceBusClient.from_connection_string(conn_str=connection_str) as client:
        # Initialize queue receiver with manual message completion for reliability
        receiver = client.get_queue_receiver(
            queue_name=queue_name,
            max_wait_time=1,
            auto_complete_messages=False
        )

        with receiver:
            print("🚀 Worker started (continuous mode)...")

            # Infinite loop to continuously poll and process incoming messages
            while True:
                # Pull a batch of messages from the queue (max 10 at a time)
                messages = receiver.receive_messages(max_message_count=10, max_wait_time=1)

                # If no messages available, wait and retry polling
                if not messages:
                    print("⏳ No messages... waiting")
                    continue

                # Process each message individually to isolate failures
                for msg in messages:
                    job_id = None
                    try:
                        # Decode and parse message payload into JSON
                        data = json.loads(b"".join(msg.body).decode("utf-8"))
                        job_id = data.get("job_id")

                        print(f"📩 Received job_id: {job_id}")

                        note_text = data["note_text"]

                        # Run full pipeline: clean → mask PHI → store → extract entities → summarize
                        result = process_note(note_text)

                        # Handle pipeline failure and mark job as failed
                        if "error" in result:
                            update_job_status(job_id, "failed", result)
                            receiver.complete_message(msg)  # ❗ don’t abandon
                            continue

                        # Update job status to completed and store result snapshot
                        update_job_status(job_id, "completed", result)

                        print(f"🧠 Updated job_id: {job_id}")

                        # Debug check to confirm job status update in database
                        with engine.connect() as conn:
                            check = conn.execute(text("""
                                SELECT status FROM dbo.jobs WHERE job_id = :job_id
                            """), {"job_id": job_id}).fetchone()

                            print("🧪 Worker sees status:", check.status if check else "NOT FOUND")

                        result["job_id"] = job_id

                        # Persist final processed output into summaries table
                        save_summary(result)

                        # Mark message as completed to prevent reprocessing
                        receiver.complete_message(msg)
                        print("✅ Processed")

                    # Catch unexpected errors, mark job as failed, and prevent retry loop
                    except Exception as e:
                        print("❌ Error:", e)

                        if job_id:
                            update_job_status(job_id, "failed", str(e))

                        receiver.complete_message(msg)  # ❗ avoid infinite retry loop

# Entry point to start worker when script is executed directly
if __name__ == "__main__":
    start_worker()