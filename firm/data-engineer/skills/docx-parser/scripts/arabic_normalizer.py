import re

ARABIC_INDIC_DIGITS = {
    '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
    '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
}

def normalize_arabic_digits(text: str) -> str:
    """Converts Eastern Arabic numerals (٠-٩) to Western standard numerals (0-9)."""
    if not isinstance(text, str):
        return text
    for ar, en in ARABIC_INDIC_DIGITS.items():
        text = text.replace(ar, en)
    return text

def clean_arabic_text(text: str) -> str:
    """Normalizes Arabic letters: alef variants, teh marbuta, and strips redundant tatweel."""
    if not isinstance(text, str):
        return text
    text = normalize_arabic_digits(text)
    # Strip tatweel (kashida)
    text = re.sub(r'ـ+', '', text)
    # Normalize Alefs
    text = re.sub(r'[إأآا]', 'ا', text)
    # Normalize Teh Marbuta
    text = re.sub(r'ة\b', 'ه', text)
    # Normalize duplicate whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_arabic_number(val) -> float | None:
    """Safely extracts a float from a string containing Arabic or English currency formats."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    
    clean_val = normalize_arabic_digits(str(val))
    # Remove currency words (ريال, ر.س, SAR, USD)
    clean_val = re.sub(r'(ريال|ر\.س|SAR|USD|\$)', '', clean_val, flags=re.IGNORECASE).strip()
    # Replace Arabic decimal comma if used as decimal
    clean_val = clean_val.replace('،', ',')
    # If commas are thousands separators
    if ',' in clean_val and '.' in clean_val:
        clean_val = clean_val.replace(',', '')
    elif ',' in clean_val and '.' not in clean_val:
        # Check if comma is decimal (e.g., 100,50)
        parts = clean_val.split(',')
        if len(parts) == 2 and len(parts[1]) <= 2:
            clean_val = clean_val.replace(',', '.')
        else:
            clean_val = clean_val.replace(',', '')

    # Extract first valid decimal number
    match = re.search(r'[-+]?\d*\.?\d+', clean_val)
    if match:
        try:
            return float(match.group())
        except ValueError:
            return None
    return None
