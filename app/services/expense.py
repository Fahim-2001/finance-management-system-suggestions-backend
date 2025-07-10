from app.models.expense import Expense, ExpenseSuggestions, ExpenseSuggestionResponse
from fastapi import HTTPException
from typing import List
from datetime import datetime

class ExpenseService:
    @staticmethod
    def get_expense_suggestions(expenses: List[Expense]) -> ExpenseSuggestions:
        """
        Generate personalized expense suggestions based on user expense data.
        """
        try:
            if not expenses:
                return ExpenseSuggestions(suggestions=[ExpenseSuggestionResponse(suggestion="No expense data provided for analysis.")])

            total_expenses = sum(expense.amount for expense in expenses)
            if total_expenses == 0:
                return ExpenseSuggestions(suggestions=[ExpenseSuggestionResponse(suggestion="Total expenses are zero. No analysis possible.")])

            suggestions = []

            # 1. Expense Optimization Suggestion
            recent_expenses = [e for e in expenses if datetime.strptime(e.date, "%Y-%m-%d %H:%M:%S") >= datetime(2025, 6, 1)]
            if recent_expenses:
                high_expense = max(recent_expenses, key=lambda x: x.amount)
                if high_expense.amount > 500:
                    suggestions.append(ExpenseSuggestionResponse(
                        suggestion=f"Your highest recent expense was ${high_expense.amount:.2f} on {high_expense.title} "
                        f"in the {high_expense.category} category. Consider reducing discretionary spending in this area "
                        f"to save approximately ${high_expense.amount * 0.2:.2f} monthly."
                    ))

            # 2. Category Spending Review
            category_totals = {}
            for expense in expenses:
                category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
            dominant_category = max(category_totals.items(), key=lambda x: x[1])[0]
            if category_totals[dominant_category] / total_expenses > 0.3:  # 30% threshold
                suggestions.append(ExpenseSuggestionResponse(
                    suggestion=f"Your spending is heavily weighted toward {dominant_category} ({(category_totals[dominant_category] / total_expenses * 100):.1f}%). "
                    f"Review and adjust your budget to balance spending across categories."
                ))

            # 3. Savings Opportunity Suggestion
            utilities_total = sum(e.amount for e in expenses if e.category == "Utilities")
            if utilities_total > 4000 and len(expenses) > 10:
                potential_savings = utilities_total * 0.15  # 15% savings potential
                suggestions.append(ExpenseSuggestionResponse(
                    suggestion=f"Your utility expenses total ${utilities_total:.2f}. Consider energy-saving measures "
                    f"to save up to ${potential_savings:.2f} by optimizing electricity and water usage."
                ))

            # Add a default suggestion if no specific advice applies
            if not suggestions:
                suggestions.append(ExpenseSuggestionResponse(
                    suggestion="Your expense patterns are stable. Continue monitoring to maintain financial health."
                ))

            return ExpenseSuggestions(suggestions=suggestions)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating expense suggestions: {str(e)}")