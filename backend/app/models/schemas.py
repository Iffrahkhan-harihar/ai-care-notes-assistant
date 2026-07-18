# Defines structured response schemas to validate and enforce consistent LLM output format
from pydantic import BaseModel, Field
from typing import List

# Represents a detected clinical risk with type and severity level
class Risk(BaseModel):
    # Short description of the identified risk
    type: str = Field(..., min_length=1)

    # Severity level of the risk (Low, Medium, High, Critical)
    severity: str

# Represents the structured summary output generated from the caregiver note
class SummaryOutput(BaseModel):
    # Concise clinical summary of the note
    summary: str = Field(..., min_length=5)

    # List of identified risks extracted from the note
    risks: List[Risk]

    # Recommended actions based on identified risks
    actions: List[str]