---
name: csv-parser
description: Parse CSV/delimited files into universal document envelope JSON.
---

# CSV Parser Sub-Skill

Parses delimited files (`.csv`, `.tsv`, `.txt`) with automatic delimiter detection and encoding handling (including Arabic Windows-1256 and UTF-8).

## Execution
Run the standalone deterministic script:
```bash
python3 ~/.hermes/skills/csv-parser/scripts/parse_csv.py /path/to/file.csv > output.json
```

## Envelope Output
Returns a structured JSON envelope with:
- `document_metadata`: File details, detected delimiter, and detected encoding.
- `payload.tables`: Extracted table headers and row objects.
- `data_health`: Row counts and column statistics.
