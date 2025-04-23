import re
import spacy

# Load a small English model for name detection
nlp = spacy.load('en_core_web_sm')

# Regex patterns for various PII
PII_PATTERNS = {
    'email': r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+",
    'phone_number': r"(?:\+?\d{1,3}[\s-]?)?(?:\d{10}|\d{5}[\s-]\d{5}|\d{3}[\s-]\d{3}[\s-]\d{4})",
    'dob': r"\b(?:\d{1,2}[/-]){2}\d{2,4}\b",  # matches dd/mm/yyyy or mm-dd-yy
    'aadhar_num': r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    'credit_debit_no': r"\b(?:\d[ -]*?){13,16}\b",
    'cvv_no': r"\b\d{3,4}\b",
    'expiry_no': r"\b(?:0[1-9]|1[0-2])[/-]\d{2,4}\b"
}


def detect_names(text):
    """
    Detect PERSON entities using SpaCy's named entity recognition.
    Returns a list of (start_char, end_char, text).
    """
    doc = nlp(text)
    names = []
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            names.append((ent.start_char, ent.end_char, ent.text))
    return names


def mask_pii(text: str):
    """
    Mask all PII in the input text.

    Returns:
      - masked_text: the text with each PII replaced by [entity_type]
      - entities: a list of dicts with keys 'position', 'classification', 'entity'
    """
    entities = []

    # 1. Detect names via SpaCy
    for start, end, name in detect_names(text):
        entities.append({'position': [start, end], 'classification': 'full_name', 'entity': name})

    # 2. Detect regex-based PII
    for label, pattern in PII_PATTERNS.items():
        for m in re.finditer(pattern, text):
            entities.append({'position': [m.start(), m.end()], 'classification': label, 'entity': m.group()})

    # Sort entities by start index
    entities = sorted(entities, key=lambda x: x['position'][0])

    # Build masked text by replacing from end to avoid offset issues
    masked = text
    offset = 0
    for ent in entities:
        start, end = ent['position']
        start += offset
        end += offset
        placeholder = f"[{ent['classification']}]"
        masked = masked[:start] + placeholder + masked[end:]
        offset += len(placeholder) - (ent['position'][1] - ent['position'][0])

    return masked, entities


def restore_pii(masked_text: str, entities: list):
    """
    Given masked_text and the entities list returned from mask_pii,
    restore the original PII values.
    """
    restored = masked_text
    offset = 0
    for ent in entities:
        placeholder = f"[{ent['classification']}]"
        idx = restored.find(placeholder, offset)
        if idx == -1:
            continue
        start = idx
        end = idx + len(placeholder)
        restored = restored[:start] + ent['entity'] + restored[end:]
        offset = start + len(ent['entity'])
    return restored
