# Orchestrates end-to-end processing: cleaning → PHI masking → storage → AI analysis
from app.services.entity_extraction import extract_entities
from app.services.llm_service import summarize_text
from app.services.phi_detection import mask_phi
from app.utils.preprocessing import clean_text
from app.storage.storage import upload_note
import uuid

# Processes a caregiver note through the full AI pipeline and returns structured results
def process_note(note_text: str):
    try:
        # Normalize and clean raw input text
        cleaned = clean_text(note_text)

        # Mask PHI before any storage or AI processing (critical for compliance)
        masked = mask_phi(cleaned)

        # Generate unique filename for storing processed note
        file_name = f"{uuid.uuid4()}.txt"

        # Store only masked text to prevent PHI exposure
        upload_note(masked, file_name)

        # Extract structured entities from masked text
        entities = extract_entities(masked)

        # Generate structured summary, risks, and actions using LLM
        summary = summarize_text(masked)

        # Handle LLM failure or invalid structured output
        if "error" in summary:
            return {
                "status": "failed",
                "reason": summary
            }

        # Aggregate pipeline outputs into final response object
        result = {
            "file_name": file_name,
            "masked_text": masked,
            "entities": entities,
            "summary": summary
        }

        # Return final processed result
        return result

    # Handle unexpected pipeline failures
    except Exception as e:
        print("❌ Pipeline error:", e)
        return {"error": str(e)}