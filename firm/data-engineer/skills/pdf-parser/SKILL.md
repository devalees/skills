---
name: pdf-parser
description: Parse digital PDF documents into universal document envelope JSON.
---

# PDF Parser Sub-Skill

Extracts structured tables and text layers from digital vector PDFs using `pdfplumber`.

## Execution
Run the standalone deterministic script:
```bash
python3 ~/.hermes/skills/pdf-parser/scripts/parse_pdf.py /path/to/file.pdf > output.json
```

## Envelope Output
Returns a structured JSON envelope with:
- `document_metadata`: File details, structure type (`tabular`, `narrative_text`, or `hybrid`), and page count.
- `payload.pages`: List of pages with extracted tables, headers, and text snippets.
- `data_health`: Number of tables extracted and page count.
