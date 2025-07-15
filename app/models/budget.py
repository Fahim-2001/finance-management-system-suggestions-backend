from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SubBudget(BaseModel):
    id: Optional[int] = None
    title: str
    amount: float
    date: str
    created_at: Optional[str] = None
    budget_id: Optional[int] = None

class Budget(BaseModel):
    id: Optional[int] = None
    title: str
    total_amount: float
    remaining: float
    type: str
    start_date: str
    end_date: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    user_id: Optional[int] = None
    subEvents: List[SubBudget] = []

class BudgetSuggestion(BaseModel):
    title: str
    description: str
    priority: str
    created_at: Optional[str] = datetime.now().isoformat()