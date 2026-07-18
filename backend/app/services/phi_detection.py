# Detects and masks Personally Identifiable Information (PHI) using Azure Language service
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from app.core.keyvault import get_secret

# Retrieve Azure Language service credentials securely from Key Vault
azure_endpoint = get_secret("azure-language-endpoint")
subscription_key = get_secret("language-key")

# Initialize Text Analytics client for PHI detection
client = TextAnalyticsClient(endpoint=azure_endpoint, credential=AzureKeyCredential(subscription_key))

# Identifies and redacts PHI entities from input text to ensure privacy compliance
def mask_phi(text: str) -> str:
    # Call Azure PII detection API to identify sensitive entities
    try:
        response = client.recognize_pii_entities([text])[0]

        # Return error indicator if API response fails
        if response.is_error:
            return "[REDACTION_FAILED]"

        # Replace detected PHI entities with [REDACTED] using reverse order to preserve offsets
        redacted = text
        for entity in sorted(response.entities, key=lambda x: x.offset, reverse=True):
            start = entity.offset
            end = start + entity.length
            redacted = redacted[:start] + "[REDACTED]" + redacted[end:]

        # Return fully redacted text
        return redacted

    # Handle unexpected errors during PHI detection
    except Exception as e:
        print("❌ PHI masking error:", e)
        return "PHI detection error"