from pydantic import BaseModel, Field
from typing import List, Optional

class Expense(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    date: str
    created_at: str
    updated_at: str
    user_id: int

    class Config:
        schema_extra = {
            "example": {
                "id": 20,
                "title": "Bus Fare",
                "amount": 300.5,
                "category": "Travel",
                "date": "2025-06-20 08:15:00",
                "created_at": "2025-05-04 01:03:05",
                "updated_at": "2025-05-04 01:03:05",
                "user_id": 1
            }
        }

class ExpenseSuggestionResponse(BaseModel):
    suggestion: str

class ExpenseSuggestions(BaseModel):
    suggestions: List[ExpenseSuggestionResponse]