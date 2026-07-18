from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os

# Load environment variables from .env file at startup
load_dotenv()

# Retrieve API key securely from environment variables
API_KEY = os.getenv("API_KEY")

# Dependency function to validate incoming request API key header
def verify_api_key(x_api_key: str = Header(...)):

    # Reject request if API key does not match expected value
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    # Return validated API key for downstream use
    return x_api_key