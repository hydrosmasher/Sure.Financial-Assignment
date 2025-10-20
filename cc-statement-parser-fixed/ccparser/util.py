import hashlib, re
from dateutil import parser as dateparser

CURRENCY_PAT = re.compile(r'([₹$€]?)\s?([+-]?[0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)')

def clean_amount(s: str):
    if not s: return None
    m = CURRENCY_PAT.search(s)
    if not m: return None
    num = m.group(2).replace(',', '')
    try:
        return float(num)
    except:
        return None

def parse_date(s: str):
    if not s: return None
    try:
        d = dateparser.parse(s, dayfirst=False, fuzzy=True)
        return d.strftime('%Y-%m-%d')
    except:
        return None

def simhash(tokens):
    h = hashlib.sha1(' '.join(tokens).encode()).hexdigest()
    return h[:16]

def normalize_spaces(s: str):
    import re
    return re.sub(r'\s+', ' ', s or '').strip()
