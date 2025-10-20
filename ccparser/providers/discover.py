from typing import List, Dict, Any
import re
from .base import BaseProvider
from ..util import normalize_spaces, parse_date, clean_amount, simhash

class DiscoverProvider(BaseProvider):
    name = "Discover"
    KEYWORDS = ['discover','discover bank','discover it']

    def score_layout(self, pages_text: List[str]) -> float:
        joined = "\n".join(pages_text).lower()
        for kw in self.KEYWORDS:
            if kw in joined:
                return 0.9
        return 0.3

    def extract(self, pages_text: List[str]) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        out["issuer"] = {"value": "Discover", "confidence": 0.95, "evidence": [self.evidence(0, "provider", "Discover")]}

        lines = []
        for i, t in enumerate(pages_text):
            for line in t.splitlines():
                L = normalize_spaces(line)
                if L:
                    lines.append((i, L))

        # last4
        last4_val, last4_ev = None, []
        for i, L in lines[:60]:
            m = re.search(r"(?:Card|Acct|Account|Number|Ending)\D*(\d{4})\b", L, re.I)
            if m:
                last4_val = m.group(1)
                last4_ev.append(self.evidence(i, "regex:last4", L))
                break
        out["card_last4"] = {"value": last4_val, "confidence": 0.8 if last4_val else 0.0, "evidence": last4_ev}

        # due date
        due_val, due_ev = None, []
        for i, L in lines:
            if re.search(r"due\s*date", L, re.I):
                tail = re.sub(r".*due\s*date\s*[:\-]?\s*", "", L, flags=re.I)
                d = parse_date(tail)
                if d:
                    due_val = d
                    due_ev.append(self.evidence(i, "regex:due", L))
                    break
        out["due_date"] = {"value": due_val, "confidence": 0.85 if due_val else 0.0, "evidence": due_ev}

        # statement balance
        bal_val, bal_ev = None, []
        for i, L in lines:
            if re.search(r"(statement\s*balance|total\s*amount\s*due)", L, re.I):
                amt = clean_amount(L)
                if amt is not None:
                    bal_val = f"{amt:.2f}"
                    bal_ev.append(self.evidence(i, "regex:balance", L))
                    break
        out["statement_balance"] = {"value": bal_val, "confidence": 0.9 if bal_val else 0.0, "evidence": bal_ev}

        # billing cycle
        bstart, bend, b_ev = None, None, []
        for i, L in lines[:120]:
            if re.search(r"(billing\s*cycle|statement\s*period)", L, re.I):
                seg = re.sub(r".*?(billing\s*cycle|statement\s*period)\s*[:\-]?\s*", "", L, flags=re.I)
                parts = re.split(r"\bto\b|\-|–|—", seg, maxsplit=1)
                if parts:
                    a = parts[0].strip()
                    b = parts[1].strip() if len(parts) > 1 else None
                    a = parse_date(a)
                    b = parse_date(b) if b else None
                    bstart, bend = a, b
                    b_ev.append(self.evidence(i, "regex:cycle", L))
                    break
        out["billing_start"] = {"value": bstart, "confidence": 0.8 if bstart else 0.0, "evidence": b_ev}
        out["billing_end"]   = {"value": bend,   "confidence": 0.8 if bend   else 0.0, "evidence": b_ev}

        # transactions
        tx = []
        for i, L in lines:
            m = re.match(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+(.+?)\s+([+-]?[\$€₹]?[0-9,]+(?:\.[0-9]{2})?)$", L)
            if m:
                d = parse_date(m.group(1))
                desc = m.group(2).strip()
                amt = clean_amount(m.group(3))
                if d and amt is not None:
                    tx.append({"date": d, "description": desc, "amount": amt})
        out["transactions"] = tx
        return out
