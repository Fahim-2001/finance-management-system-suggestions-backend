from fastapi import FastAPI
from app.models.income import Income, IncomeSuggestionResponse, IncomeSuggestions
from app.models.loan import Loan, LoanSuggestion
from app.services.income import IncomeService
from app.services.loan import generate_payment_optimization
from datetime import datetime
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Loan Management API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
async def income_suggestions(incomes: list[Income]):
    diversification = IncomeService.get_diversification_suggestion(incomes)
    optimal_savings = IncomeService.get_savings_allocation(incomes)
    income_boost = IncomeService.get_income_boost_recommendation(incomes)
    suggestions = []
    suggestions.append(diversification)
    suggestions.append(optimal_savings)
    suggestions.append(income_boost)
    print(suggestions)
    return suggestions


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
