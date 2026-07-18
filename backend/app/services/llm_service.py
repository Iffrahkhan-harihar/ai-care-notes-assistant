# Handles interaction with Azure OpenAI and enforces structured clinical output
from app.models.schemas import SummaryOutput
from app.core.keyvault import get_secret
from pydantic import ValidationError
from openai import AzureOpenAI
import json

# Azure OpenAI configuration (API version, model, and deployment name)
api_version = "2024-12-01-preview"
model_name = "gpt-4o"
deployment = "gpt-4o-deploy"

# Retrieve Azure OpenAI credentials securely from Key Vault
subscription_key = get_secret("azure-openai-key")
azure_endpoint = get_secret("azure-openai-endpoint")

# Initialize Azure OpenAI client for LLM inference
client = AzureOpenAI(
    api_key=subscription_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)

# Generates structured clinical summary, risks, and actions from caregiver note using LLM
def summarize_text(note_text: str):
    # Construct strict prompt to enforce JSON-only structured output from LLM
    prompt = f"""
You are a clinical assistant.

Your task is to analyze a caregiver note and return STRICT JSON ONLY.

You MUST follow this schema exactly:

{{
  "summary": "string",
  "risks": [
    {{
      "type": "string",
      "severity": "Low | Medium | High | Critical"
    }}
  ],
  "actions": ["string"]
}}

STRICT RULES:
- Output MUST be valid JSON (no trailing commas, no comments)
- DO NOT include markdown, explanations, or extra text
- DO NOT change key names
- DO NOT nest objects differently
- If no risks → return "risks": []
- If no actions → return "actions": []
- Ensure "risks" is ALWAYS an array of objects
- Ensure "actions" is ALWAYS an array of strings
- Ensure "summary" is ALWAYS a string

If you cannot comply, return:
{{"summary": "", "risks": [], "actions": []}}

Note:
{note_text}
"""

    # Call Azure OpenAI chat completion endpoint
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a strict clinical AI that outputs only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4096,
        temperature=0.2,
        top_p=1.0
    )

    # Extract raw text output from LLM response
    output = response.choices[0].message.content

    if not output:
        return {"error": "Empty response from LLM"}

    # Parse LLM output and validate against Pydantic schema
    try:
        parsed = json.loads(output)
        validated = SummaryOutput(**parsed)  # 🔥 validation happens here
        return validated.dict()

    # Handle schema validation failures (LLM returned incorrect structure)
    except ValidationError as ve:
        return {
            "error": "Schema validation failed",
            "details": ve.errors(),
            "raw_output": output
        }

    # Handle invalid JSON or unexpected response format
    except Exception:
        return {
            "error": "Invalid JSON output",
            "raw_output": output
        }
