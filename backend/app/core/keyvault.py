from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
import os

# Load environment variables (used locally to fetch Key Vault URL)
load_dotenv()

# Azure Key Vault endpoint URL
vault_url = os.getenv("KEY_VAULT_URL")

# Uses Azure's default credential chain (CLI, managed identity, environment, etc.)
credential = DefaultAzureCredential()

# Client to interact with Azure Key Vault for secret retrieval
client = SecretClient(vault_url=vault_url, credential=credential)

# In-memory cache to avoid repeated network calls for secrets
cache = {}

# Fetch secret from Key Vault with caching for performance optimization
def get_secret(name):

    # Return cached value if already fetched
    if name in cache:
        return cache[name]

    # Retrieve secret securely from Azure Key Vault
    value = client.get_secret(name).value

    # Store in cache to reduce latency and API calls
    cache[name] = value

    return value