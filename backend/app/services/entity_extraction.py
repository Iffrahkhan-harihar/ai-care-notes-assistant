from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from app.core.keyvault import get_secret

# Retrieve Azure Language service credentials securely from Key Vault
azure_endpoint = get_secret("azure-language-endpoint")
subscription_key = get_secret("language-key")

# Initialize Azure Text Analytics client for entity recognition
client = TextAnalyticsClient(endpoint=azure_endpoint, credential=AzureKeyCredential(subscription_key))

# Extract named entities (medical, temporal, objects, etc.) from input text
def extract_entities(text: str):
    try:
        # Call Azure NLP service to recognize entities in the text
        response = client.recognize_entities([text])[0]

        # Return empty list if API response contains an error
        if response.is_error:
            return []

        # Normalize entity output into structured JSON format
        return [
            {
                "text": entity.text,
                "category": entity.category,
                "confidence": entity.confidence_score
            }
            for entity in response.entities
        ]

    except Exception as e:
        # Handle API or runtime failures gracefully
        print("❌ Entity extraction error:", e)
        return []