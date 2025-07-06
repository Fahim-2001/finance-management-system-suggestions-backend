from fastapi import HTTPException
from app.models.income import Income, IncomeSuggestionResponse


class IncomeService:
    @staticmethod
    def get_diversification_suggestion(incomes: list[Income]) -> dict[IncomeSuggestionResponse]:
        try:
            if not incomes:
                return {"suggestion": "No income data provided for analysis."}

            # Calculate total income
            total_income = sum(income.amount for income in incomes)

            if total_income == 0:
                return {"suggestion": "Total income is zero. No analysis possible."}

            # Group by source and calculate percentage
            source_distribution = {}
            for income in incomes:
                source_distribution[income.source] = source_distribution.get(
                    income.source, 0) + income.amount

            # Identify dominant source and check diversification threshold (e.g., 70%)
            threshold = 0.7
            for source, amount in source_distribution.items():
                percentage = amount / total_income
                if percentage > threshold:
                    alternative_sources = [
                        "Freelance",
                        "Side Business",
                        "Investments",
                        "Real Estate",
                    ]
                    # Filter out the dominant source from alternatives
                    alternative_sources = [
                        s for s in alternative_sources if s != source]
                    return IncomeSuggestionResponse(suggestion=f"Your income is heavily reliant ({percentage*100:.1f}%) on {source}. "
                                                    f"Consider diversifying by exploring {', '.join(alternative_sources)}.")

            # If no single source exceeds threshold
            return IncomeSuggestionResponse(suggestion="Your income is well-diversified. Maintain current strategy!")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_savings_allocation(incomes: list[Income]) -> dict[IncomeSuggestionResponse]:
        try:
            if not incomes:
                return {"suggestion": "No income data provided for analysis."}

            # Calculate total income
            total_income = sum(income.amount for income in incomes)

            if total_income == 0:
                return {"suggestion": "Total income is zero. No analysis possible."}

            # Suggested savings rate (20-30% based on income level)
            base_savings_rate = 0.20
            if total_income > 5000:
                savings_rate = 0.30  # Higher rate for higher income
            else:
                savings_rate = base_savings_rate

            savings_amount = total_income * savings_rate
            remaining_income = total_income - savings_amount

            # Suggest allocation options
            suggestion = (
                f"Based on your total income of ${total_income:.2f}, we recommend saving "
                f"${savings_amount:.2f} ({savings_rate*100:.0f}%). Consider allocating this to a "
                f"high-yield savings account or low-risk investment. You can use the remaining "
                f"${remaining_income:.2f} for expenses and discretionary spending."
            )

            return IncomeSuggestionResponse(suggestion=suggestion)

        except Exception as e:
            return IncomeSuggestionResponse(suggestion=f"Error analyzing savings: {str(e)}")

    @staticmethod
    def get_income_boost_recommendation(incomes: list[Income]) -> dict[IncomeSuggestionResponse]:
        try:
            if not incomes:
                return {"suggestion": "No income data provided for analysis."}

            # Group incomes by month and calculate monthly totals
            monthly_income = {}
            for income in incomes:
                month = income.date.split(" ")[0][:7]  # Extract YYYY-MM
                monthly_income[month] = monthly_income.get(
                    month, 0) + income.amount

            if not monthly_income:
                return {"suggestion": "No valid monthly income data available."}

            # Find the lowest income month
            min_month = min(monthly_income, key=monthly_income.get)
            min_amount = monthly_income[min_month]

            # Average income for comparison
            avg_income = sum(monthly_income.values()) / len(monthly_income)

            # Threshold for low income (50% of average)
            if min_amount < avg_income * 0.5:
                # Suggest income boost based on category
                categories = set(income.category for income in incomes)
                suggestions = []
                if "Employment" in categories:
                    suggestions.append("Negotiate a raise with your employer.")
                if "Self-Employment" in categories:
                    suggestions.append(
                        "Take on additional freelance projects or upskill in a high-demand area like AI/ML.")
                suggestions.append(
                    "Explore side gigs such as tutoring or online content creation.")

                return IncomeSuggestionResponse(suggestion=f"Your income in {min_month} was low at ${min_amount:.2f}. "
                                                f"Consider {', '.join(suggestions[:-1])} or {suggestions[-1]} to boost earnings.")

            return IncomeSuggestionResponse(suggestion="Your income is stable across months. No immediate boost needed!")

        except Exception as e:
            return {"suggestion": f"Error analyzing income boost: {str(e)}"}
