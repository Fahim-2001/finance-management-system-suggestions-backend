from pydantic import BaseModel, Field
from typing import List

class GoalEntry(BaseModel):
    id: int
    amount: float
    current_amount: float
    entry_date: str
    created_at: str
    updated_at: str
    goal_id: int

class SavingsGoal(BaseModel):
    id: int
    title: str
    target_amount: float
    current_amount: float
    start_date: str
    end_date: str | None = None  # Allow null end_date
    status: str
    goal_entries: List[GoalEntry]