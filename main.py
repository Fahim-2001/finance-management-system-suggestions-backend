from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import List
from fastapi.middleware.cors import CORSMiddleware
#
from app.models.income import Income, IncomeSuggestionResponse, IncomeSuggestions
from app.models.loan import Loan, LoanSuggestion
from app.models.expense import Expense, ExpenseSuggestions
from app.models.savings import SavingsGoal
from app.services.income import IncomeService
from app.services.loan import generate_payment_optimization
from app.services.expense import ExpenseService
from app.services.savings import predict_monthly_savings, suggest_expense_cuts, forecast_savings_growth


app = FastAPI(title="Loan Management API", version="1.0.0")

# Enable CORS
origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1:5173",
    "https://finance-management-system-frontend-capstone.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],    # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],    # Allow all headers
)


@app.post("/loan/optimize-payments", response_model=List[LoanSuggestion])
async def optimize_payments(loans: List[Loan]):
    """
    Analyze the last 6 months of loan data and provide payment optimization suggestions.
    """
    suggestions = generate_payment_optimization(loans)
    return suggestions

# New income diversification suggestion endpoint


@app.post("/income/suggestions/", response_model=IncomeSuggestions)
async def get_income_suggestions(incomes: list[Income]):
    try:
        suggestions = IncomeService.get_income_suggestions(incomes)
        return suggestions
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/expense/suggestions/", response_model=ExpenseSuggestions)
async def get_expense_suggestions(expenses: List[Expense]):
    try:
        suggestions = ExpenseService.get_expense_suggestions(expenses)
        return suggestions
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/savings/suggestions/")
async def get_suggestions(goals: List[SavingsGoal]):
    suggestions = []
    monthly_savings = predict_monthly_savings(goals)
    if monthly_savings:
        suggestions.extend(monthly_savings)
    expense_cuts = suggest_expense_cuts(goals)
    if expense_cuts:
        suggestions.extend(expense_cuts)
    automated_savings = forecast_savings_growth(goals)
    if automated_savings:
        suggestions.extend(automated_savings)
    if not suggestions:
        raise HTTPException(status_code=404, detail="No suggestions available")
    return {"suggestions": suggestions}


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
