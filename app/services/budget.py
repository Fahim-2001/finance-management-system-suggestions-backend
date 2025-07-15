from typing import List
from app.models.budget import Budget, BudgetSuggestion

class BudgetService:
    @staticmethod
    def analyze_budgeting_behavior(budgets: List[Budget]) -> List[BudgetSuggestion]:
        suggestions = []
        annual_end_date_issue = any(b.end_date == "1970-01-01 06:00:00" for b in budgets if b.type == "Annually")
        if annual_end_date_issue:
            suggestions.append(BudgetSuggestion(
                title="Adjust Annual Budget End Dates",
                description="Set realistic end dates for annual budgets to better track progress.",
                priority="High"
            ))

        savings_utilization = [b for b in budgets if "Savings" in b.title and b.remaining > b.total_amount * 0.5]
        if savings_utilization:
            suggestions.append(BudgetSuggestion(
                title="Increase Monthly Savings",
                description="Boost monthly savings contributions to meet targets like the emergency fund more effectively.",
                priority="Medium"
            ))

        recurring_expenses = [b for b in budgets if b.type == "Monthly" and b.remaining / b.total_amount < 0.5]
        if recurring_expenses:
            suggestions.append(BudgetSuggestion(
                title="Create Monthly Expense Reserve",
                description="Establish a reserve for recurring expenses to avoid overspending.",
                priority="Medium"
            ))

        return suggestions[:3]  # Limit to 3 suggestions

    @staticmethod
    def get_budget_suggestions(budgets: List[Budget]) -> List[BudgetSuggestion]:
        return BudgetService.analyze_budgeting_behavior(budgets)