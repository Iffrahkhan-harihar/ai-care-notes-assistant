# Handles secure storage of processed notes in Azure Blob Storage
from azure.storage.blob import BlobServiceClient
from app.core.keyvault import get_secret

# Retrieve Azure Blob Storage credentials securely from Key Vault
connection_string = get_secret("connection-string")
container_name = get_secret("container-name")

# Initialize Blob Service client for interacting with storage account
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Uploads masked note text to Azure Blob Storage for persistence
def upload_note(note_text: str, file_name: str):
    try:
        # Create a blob client for the target container and file
        blob_client = blob_service_client.get_blob_client(
            container=container_name,
            blob=file_name
        )

        # Upload note text to blob storage (overwrite if file already exists)
        blob_client.upload_blob(note_text, overwrite=True)

    # Handle storage upload failures
    except Exception as e:
        print("❌ Blob upload error:", e)