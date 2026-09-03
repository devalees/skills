import os
import sys
import json
import base64
from pathlib import Path
from arabic_normalizer import clean_arabic_text, parse_arabic_number

def encode_image(image_path: str) -> str:
    """Encode local image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def build_vision_ocr_prompt() -> str:
    """Returns the structured prompt for extracting Arabic scanned documents."""
    return """
You are an expert Arabic document OCR parser.
Analyze this document (scanned invoice, contract, or Commercial Register - السجل التجاري).
Extract all structured data and return STRICTLY a JSON object matching this schema:

{
  "document_metadata": {
    "file_type": "scanned_image",
    "structure_type": "key_value_form | tabular | hybrid",
    "document_category": "commercial_register | tax_invoice | bank_confirmation | contract | other"
  },
  "payload": {
    "key_values": {
      "cr_number": "...",
      "company_name": "...",
      "issue_date": "...",
      "expiry_date": "...",
      "total_amount": 0.0,
      "vat_amount": 0.0
    },
    "tables": [
      {
        "table_name": "items_or_entries",
        "headers": ["...", "..."],
        "rows": [{"col1": "val1"}]
      }
    ],
    "raw_text_summary": "..."
  },
  "data_health": {
    "legibility_score": 0.95,
    "has_official_stamp": true,
    "has_signature": true,
    "confidence_status": "high | medium | low"
  }
}
Do not include markdown prose outside the JSON block.
"""

def prepare_envelope(file_path: str, vision_json_response: dict) -> dict:
    """Wraps and normalizes the vision model output into the standard envelope."""
    payload = vision_json_response.get("payload", {})
    key_vals = payload.get("key_values", {})
    
    # Normalize Arabic texts and numbers
    cleaned_kv = {}
    for k, v in key_vals.items():
        if isinstance(v, str):
            cleaned_kv[k] = clean_arabic_text(v)
        else:
            cleaned_kv[k] = v

    vision_json_response["document_metadata"]["file_name"] = os.path.basename(file_path)
    vision_json_response["payload"]["key_values"] = cleaned_kv
    return vision_json_response

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ocr_arabic_document.py <path_to_image_or_scanned_pdf>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    print(f"Prepared Vision OCR payload template for {file_path}")
    print("Prompt specification:")
    print(build_vision_ocr_prompt())
