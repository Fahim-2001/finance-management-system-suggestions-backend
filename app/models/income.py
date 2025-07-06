from pydantic import BaseModel, Field
from typing import List, Optional

class Income(BaseModel):
    amount: float
    source: str
    category: str
    date: str
    user_id: int
    notes: str | None = None

class IncomeSuggestionResponse(BaseModel):
    suggestion: str
    
class IncomeSuggestions(BaseModel):
    suggestions: List[IncomeSuggestionResponse]