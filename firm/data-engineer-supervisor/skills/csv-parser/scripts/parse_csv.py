import os
import sys
import json
import csv

def parse_csv(file_path):
    # Try detecting encoding
    encodings = ['utf-8', 'utf-8-sig', 'windows-1256', 'latin-1']
    chosen_encoding = 'utf-8'
    sample = None

    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                sample = f.read(4096)
                chosen_encoding = enc
                break
        except Exception:
            continue

    if not sample:
        with open(file_path, 'r', encoding='latin-1', errors='replace') as f:
            sample = f.read(4096)
            chosen_encoding = 'latin-1 (forced)'

    # Detect delimiter
    try:
        dialect = csv.Sniffer().sniff(sample)
        delimiter = dialect.delimiter
    except Exception:
        delimiter = ','

    rows_data = []
    headers = []

    with open(file_path, 'r', encoding=chosen_encoding.split()[0], errors='replace') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for i, row in enumerate(reader):
            if not row or not any(c.strip() for c in row):
                continue
            if not headers:
                headers = [str(c).strip() if str(c).strip() else f"col_{idx+1}" for idx, c in enumerate(row)]
            else:
                row_dict = {}
                for idx, col in enumerate(headers):
                    val = row[idx].strip() if idx < len(row) else ""
                    row_dict[col] = val
                rows_data.append(row_dict)

    envelope = {
        "document_metadata": {
            "file_name": os.path.basename(file_path),
            "file_type": "csv",
            "structure_type": "tabular",
            "detected_delimiter": delimiter,
            "detected_encoding": chosen_encoding
        },
        "payload": {
            "tables": [
                {
                    "name": "csv_data",
                    "headers": headers,
                    "row_count": len(rows_data),
                    "rows": rows_data
                }
            ]
        },
        "data_health": {
            "total_rows_extracted": len(rows_data),
            "column_count": len(headers),
            "status": "success"
        }
    }
    return envelope

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parse_csv.py <path_to_csv_file>")
        sys.exit(1)
    result = parse_csv(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
