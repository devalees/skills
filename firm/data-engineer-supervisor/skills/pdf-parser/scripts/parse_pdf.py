import os
import sys
import json
import pdfplumber

def parse_pdf(file_path):
    pages_data = []
    total_tables = 0
    total_text_length = 0

    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_num = i + 1
            extracted_text = page.extract_text() or ""
            total_text_length += len(extracted_text)
            
            raw_tables = page.extract_tables()
            formatted_tables = []
            
            for t_idx, table in enumerate(raw_tables):
                clean_table = [[cell.strip() if cell is not None else "" for cell in row] for row in table if any(cell for cell in row)]
                if not clean_table:
                    continue
                
                headers = clean_table[0]
                rows = []
                for r in clean_table[1:]:
                    row_dict = {}
                    for c_idx, h in enumerate(headers):
                        col_key = h if h != "" else f"col_{c_idx+1}"
                        row_dict[col_key] = r[c_idx] if c_idx < len(r) else ""
                    rows.append(row_dict)
                
                formatted_tables.append({
                    "table_index": t_idx + 1,
                    "headers": headers,
                    "row_count": len(rows),
                    "rows": rows
                })
            
            total_tables += len(formatted_tables)
            pages_data.append({
                "page": page_num,
                "tables": formatted_tables,
                "text_snippet": extracted_text[:500] if extracted_text else ""
            })

    structure = "tabular" if total_tables > 0 else "narrative_text"
    if total_tables > 0 and total_text_length > 1000:
        structure = "hybrid"

    envelope = {
        "document_metadata": {
            "file_name": os.path.basename(file_path),
            "file_type": "pdf",
            "structure_type": structure,
            "page_count": len(pages_data)
        },
        "payload": {
            "pages": pages_data
        },
        "data_health": {
            "tables_extracted": total_tables,
            "total_pages": len(pages_data),
            "status": "success"
        }
    }
    return envelope

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parse_pdf.py <path_to_pdf_file>")
        sys.exit(1)
    result = parse_pdf(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))
