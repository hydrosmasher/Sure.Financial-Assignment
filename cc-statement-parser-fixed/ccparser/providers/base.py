from typing import List, Dict, Any
import re
from ..util import normalize_spaces, clean_amount, parse_date, simhash

class BaseProvider:
    name = "base"
    KEYWORDS: List[str] = []

    def score_layout(self, pages_text: List[str]) -> float:
        return 0.1

    def evidence(self, page_idx: int, method: str, snippet: str, score: float=1.0):
        return {"page": page_idx, "method": method, "snippet": snippet[:120], "score": score}

    def extract(self, pages_text: List[str]) -> Dict[str, Any]:
        raise NotImplementedError
