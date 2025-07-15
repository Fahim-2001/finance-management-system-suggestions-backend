from fastapi import HTTPException
from app.models.income import Income, IncomeSuggestionResponse, IncomeSuggestions
from typing import List

class IncomeService:
    @staticmethod
    def get_income_suggestions(incomes: List[Income]) -> IncomeSuggestions:
        """
        Generate personalized financial suggestions based on income data.
        Returns a list of suggestions wrapped in IncomeSuggestions model.
        """
        try:
            if not incomes:
                return IncomeSuggestions(suggestions=[IncomeSuggestionResponse(suggestion="No income data provided for analysis.")])

            # Calculate total income
            total_income = sum(income.amount for income in incomes)
            if total_income == 0:
                return IncomeSuggestions(suggestions=[IncomeSuggestionResponse(suggestion="Total income is zero. No analysis possible.")])

            # Initialize list to hold all suggestions
            suggestions = []

            # 1. Diversification Suggestion
            source_distribution = {}
            for income in incomes:
                source_distribution[income.source] = source_distribution.get(income.source, 0) + income.amount

            threshold = 0.7  # 70% threshold for diversification
            for source, amount in source_distribution.items():
                percentage = amount / total_income
                if percentage > threshold:
                    alternative_sources = ["Freelance", "Side Business", "Investments", "Real Estate"]
                    alternative_sources = [s for s in alternative_sources if s != source]
                    suggestions.append(IncomeSuggestionResponse(
                        suggestion=f"Your income is heavily reliant ({percentage*100:.1f}%) on {source}. "
                        f"Consider diversifying by exploring {', '.join(alternative_sources)}."
                    ))
                    break  # Only provide one diversification suggestion if threshold is exceeded
            if not suggestions:
                suggestions.append(IncomeSuggestionResponse(suggestion="Your income is well-diversified. Maintain current strategy!"))

            # 2. Savings Allocation Suggestion
            base_savings_rate = 0.20
            savings_rate = 0.30 if total_income > 5000 else base_savings_rate
            savings_amount = total_income * savings_rate
            remaining_income = total_income - savings_amount
            suggestions.append(IncomeSuggestionResponse(
                suggestion=f"Based on your total income of BDT{total_income:.2f}, we recommend saving "
                f"BDT{savings_amount:.2f} ({savings_rate*100:.0f}%). Consider allocating this to a "
                f"high-yield savings account or low-risk investment. You can use the remaining "
                f"BDT{remaining_income:.2f} for expenses and discretionary spending."
            ))

            # 3. Income Boost Recommendation
            monthly_income = {}
            for income in incomes:
                month = income.date.split(" ")[0][:7]  # Extract YYYY-MM
                monthly_income[month] = monthly_income.get(month, 0) + income.amount

            if monthly_income:
                min_month = min(monthly_income, key=monthly_income.get)
                min_amount = monthly_income[min_month]
                avg_income = sum(monthly_income.values()) / len(monthly_income)

                if min_amount < avg_income * 0.5:
                    categories = set(income.category for income in incomes)
                    suggestions_list = []
                    if "Employment" in categories:
                        suggestions_list.append("Negotiate a raise with your employer.")
                    if "Self-Employment" in categories:
                        suggestions_list.append("Take on additional freelance projects or upskill in a high-demand area like AI/ML.")
                    suggestions_list.append("Explore side gigs such as tutoring or online content creation.")
                    suggestions.append(IncomeSuggestionResponse(
                        suggestion=f"Your income in {min_month} was low at BDT{min_amount:.2f}. "
                        f"Consider {', '.join(suggestions_list[:-1])} or {suggestions_list[-1]} to boost earnings."
                    ))
                else:
                    suggestions.append(IncomeSuggestionResponse(suggestion="Your income is stable across months. No immediate boost needed!"))

            return IncomeSuggestions(suggestions=suggestions)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating income suggestions: {str(e)}")