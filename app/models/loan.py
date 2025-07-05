from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

# Enums
class PaymentFrequency(str, Enum):
    WEEKLY = "Weekly"
    BIWEEKLY = "BiWeekly"
    MONTHLY = "Monthly"

class LoanStatus(str, Enum):
    ACTIVE = "Active"
    PAID_OFF = "PaidOff"
    DEFAULT = "Default"

class Suggestion(BaseModel):
    text: str
    type: str  # "increase", "frequency", "early", "summary"

class LoanPayment(BaseModel):
    id: int
    payment_date: str = Field(..., description="ISO 8601 date string (e.g., '2025-01-15T14:00:00Z')")
    amount_paid: float
    principal_paid: float
    interest_paid: float
    remaining_balance: float
    notes: Optional[str] = None
    created_at: Optional[str] = None
    loan_id: Optional[int] = None

class Loan(BaseModel):
    id: int
    loan_type: str
    lender_name: str
    principal_amount: float
    total_payable: float
    total_paid: float
    due: float
    interest_rate: float
    number_of_payments: int
    remaining_payments: int
    start_date: str = Field(..., description="ISO 8601 date string (e.g., '2025-01-05T10:30:00Z')")
    end_date: Optional[str] = Field(None, description="ISO 8601 date string")
    next_payment_date: Optional[str] = Field(None, description="ISO 8601 date string")
    payment_frequency: PaymentFrequency
    status: LoanStatus
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    user_id: Optional[int] = None
    payments: Optional[List[LoanPayment]] = None

class LoanSuggestion(BaseModel):
    loan_id: int
    lender_name: str
    loan_type: str
    start_date: str
    end_date: Optional[str] = None
    suggestions: List[Suggestion]

    class Config:
        schema_extra = {
            "example": {
                "loan_id": 1,
                "lender_name": "DBBL",
                "loan_type": "Business Loan",
                "start_date": "2025-03-05T09:45:00Z",
                "end_date": "2025-06-05T23:59:59Z",
                "suggestions": [
                    {"text": "Increase biweekly payment by 20%", "type": "increase"},
                    {"text": "Pay off early", "type": "early"}
                ]
            }
        }