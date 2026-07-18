# Handles text normalization and basic preprocessing for clinical notes
import re

# Cleans and standardizes raw text input for better downstream processing
def clean_text(text: str) -> str:
    # Normalize whitespace by removing extra spaces, tabs, and line breaks
    text = re.sub(r'\s+', ' ', text)

    # Expand common clinical abbreviations for improved NLP and LLM accuracy
    abbreviations = {
        "pt": "patient",
        "bp": "blood pressure",
        "hr": "heart rate",
        "c/o": "complains of",
        "h/o": "history of",
        "s/p": "status post",
        "w/": "with",
        "w/o": "without",
        "dx": "diagnosis",
        "tx": "treatment",
        "rx": "prescription",
        "sx": "symptoms",
        "d/c": "discharge",
        "q": "every",
        "qd": "every day",
        "bid": "twice a day",
        "tid": "three times a day",
        "qid": "four times a day",
        "prn": "as needed",
        "po": "by mouth",
        "iv": "intravenous",
        "im": "intramuscular",
        "subq": "subcutaneous",
        "npo": "nothing by mouth",
        "stat": "immediately",
        "pr": "per rectum",
        "sl": "sublingual",
        "gtt": "drops",
        "mcg": "micrograms",
        "mg": "milligrams",
        "ml": "milliliters",
        "l": "liters",
        "hrly": "hourly",
        "q4h": "every 4 hours",
        "q6h": "every 6 hours",
        "q8h": "every 8 hours",
        "q12h": "every 12 hours",
        "q24h": "every 24 hours"
    }

    # Replace abbreviations with full forms (case-insensitive)
    for short, full in abbreviations.items():
        text = re.sub(rf"\b{short}\b", full, text, flags=re.IGNORECASE)

    # Return cleaned and normalized text
    return text.strip()