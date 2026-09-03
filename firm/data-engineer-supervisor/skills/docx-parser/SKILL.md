---
name: docx-parser
description: Parse Word (.docx) files into universal document envelope JSON.
---

# Word Docx Parser Sub-Skill

Extracts paragraphs and tables from Word documents (`.docx`) using `python-docx`.

## Execution
Run the standalone deterministic script:
```bash
python3 ~/.hermes/skills/docx-parser/scripts/parse_docx.py /path/to/document.docx > output.json
```

## Envelope Output
Returns a structured JSON envelope with:
- `document_metadata`: File details, structure type (`narrative_text`, `tabular`, or `hybrid`), paragraph count, and table count.
- `payload`: Contains extracted `paragraphs` list and `tables` list with row objects.
- `data_health`: Extraction stats and status.
