from typing import List, Type
from .providers.base import BaseProvider
from .providers import amex, chase, citi, capitalone, discover

PROVIDERS: List[Type[BaseProvider]] = [
    amex.AmexProvider,
    chase.ChaseProvider,
    citi.CitiProvider,
    capitalone.CapitalOneProvider,
    discover.DiscoverProvider,
]

def detect_provider(pages_text: List[str]) -> BaseProvider:
    joined = '\n'.join(pages_text).lower()
    for P in PROVIDERS:
        for kw in P.KEYWORDS:
            if kw in joined:
                return P()
    best = None
    best_score = -1.0
    for P in PROVIDERS:
        p = P()
        score = p.score_layout(pages_text)
        if score > best_score:
            best, best_score = p, score
    return best
