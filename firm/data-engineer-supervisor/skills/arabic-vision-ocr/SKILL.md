---
name: arabic-vision-ocr
description: Extract structured data from scanned Arabic invoices, contracts, and Commercial Registers.
---

# Arabic Vision OCR Sub-Skill

Handles scanned Arabic documents (contracts, tax invoices, bank confirmations, and Commercial Registers / السجل التجاري) where traditional OCR engines fail due to Arabic fonts, handwriting, or stamps.

## Execution Pattern
1. Inspect image/page via `vision_analyze` using the system prompt defined in `scripts/ocr_arabic_document.py`.
2. Post-process the extracted values with `arabic_normalizer.py` to ensure Eastern Arabic numerals (٠-٩) and letter variants (أ/إ/آ, ة/ه) are converted to standard format.

## Envelope Output
Returns the standard Universal Document Envelope:
- `document_metadata`: Category (`commercial_register`, `tax_invoice`, etc.), file name, structure type.
- `payload.key_values`: Cleaned entity names, registration numbers, dates, and amounts.
- `payload.tables`: Line items, statement rows, or transaction matrices.
- `data_health`: Legibility score, stamp/signature detection flags.
