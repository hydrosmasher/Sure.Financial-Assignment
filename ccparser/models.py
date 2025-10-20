from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class FieldEvidence(BaseModel):
    page: int
    method: str
    snippet: str
    score: float = 1.0

class ExtractedField(BaseModel):
    value: Optional[str] = None
    confidence: float = 0.0
    evidence: List[FieldEvidence] = []

class Transaction(BaseModel):
    date: str
    description: str
    amount: float

class ParseResult(BaseModel):
    issuer: ExtractedField
    card_last4: ExtractedField
    billing_start: ExtractedField
    billing_end: ExtractedField
    due_date: ExtractedField
    statement_balance: ExtractedField
    transactions: List[Transaction] = []
    meta: Dict[str, Any] = Field(default_factory=dict)
