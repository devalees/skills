---
name: excel-parser
description: Parse Excel (.xlsx/.xls) into universal document envelope JSON.
---

# Excel Parser Sub-Skill

Extracts tabular matrices from Excel workbooks (`.xlsx`, `.xls`) across all sheets.

## Execution
Run the standalone deterministic script:
```bash
python3 ~/.hermes/skills/excel-parser/scripts/parse_excel.py /path/to/file.xlsx > output.json
```

## Envelope Output
Returns a structured JSON envelope with:
- `document_metadata`: File details, structure type (`tabular`), and sheet count.
- `payload.tables`: List of extracted sheets with detected header row, column names, and row dictionaries.
- `data_health`: Total rows extracted and processing status.
