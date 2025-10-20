from typing import List
import pdfplumber
from .models import ParseResult, ExtractedField, FieldEvidence, Transaction
from .detect import detect_provider

def parse_pdf(path: str) -> ParseResult:
    pages_text: List[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            pages_text.append(t)

    provider = detect_provider(pages_text)
    raw = provider.extract(pages_text)

    def mk(name):
        item = raw.get(name, {})
        return ExtractedField(
            value=item.get("value"),
            confidence=item.get("confidence", 0.0),
            evidence=[FieldEvidence(**ev) for ev in item.get("evidence",[])],
        )

    tx = [Transaction(**t) for t in raw.get("transactions", [])]

    return ParseResult(
        issuer=mk("issuer"),
        card_last4=mk("card_last4"),
        billing_start=mk("billing_start"),
        billing_end=mk("billing_end"),
        due_date=mk("due_date"),
        statement_balance=mk("statement_balance"),
        transactions=tx,
        meta={"provider": provider.name, "pages": len(pages_text)},
    )
