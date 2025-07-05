from app.models.loan import Loan, LoanSuggestion, Suggestion, LoanPayment, PaymentFrequency
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta

def generate_payment_optimization(loans: List[Loan]) -> List[LoanSuggestion]:
    now = datetime.now().replace(tzinfo=None)  # Naive local time
    six_months_ago = now.replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta(months=6)
    recent_loans = [loan for loan in loans if datetime.fromisoformat(loan.start_date.replace("Z", "").replace("+00:00", "")).replace(hour=0, minute=0, second=0, microsecond=0) >= six_months_ago]

    loan_suggestions = []

    for loan in recent_loans:
        suggestions = []
        remaining_principal = loan.due if loan.due else (loan.principal_amount - (loan.total_paid or 0.0))
        if loan.payments:
            last_payment = max(loan.payments, key=lambda p: datetime.fromisoformat(p.payment_date.replace("Z", "").replace("+00:00", "")))
            remaining_principal = last_payment.remaining_balance

        payments_per_year = 52 if loan.payment_frequency == PaymentFrequency.WEEKLY else 26 if loan.payment_frequency == PaymentFrequency.BIWEEKLY else 12
        current_payment = remaining_principal / loan.remaining_payments
        monthly_interest = (loan.interest_rate / 100) * remaining_principal / 12
        high_interest_threshold = 10.0

        # Suggestion 1: Increase Payment for High-Interest Loans
        if loan.interest_rate > high_interest_threshold:
            increased_payment = current_payment * 1.2
            new_term = remaining_principal / increased_payment * (12 / payments_per_year)
            interest_saved = (loan.remaining_payments - new_term) * (monthly_interest / (payments_per_year / 12))
            suggestions.append(
                Suggestion(
                    text=f"Increase {loan.payment_frequency.value.lower()} payment for {loan.lender_name} loan by 20% to {increased_payment:.2f} BDT. "
                         f"This could save approximately {interest_saved:.2f} BDT in interest and reduce the term by "
                         f"{int(loan.remaining_payments - new_term)} {loan.payment_frequency.value.lower()} periods.",
                    type="increase"
                )
            )

        # Suggestion 2: Switch to Monthly Payments (if BiWeekly or Weekly)
        if loan.payment_frequency in [PaymentFrequency.BIWEEKLY, PaymentFrequency.WEEKLY] and remaining_principal > 0:
            monthly_payment = remaining_principal / (loan.remaining_payments * (payments_per_year / 12))
            new_term_monthly = remaining_principal / monthly_payment
            interest_saved_monthly = (loan.remaining_payments - new_term_monthly) * (monthly_interest / (payments_per_year / 12))
            if interest_saved_monthly > 0:
                suggestions.append(
                    Suggestion(
                        text=f"Switch {loan.lender_name} loan to monthly payments of {monthly_payment:.2f} BDT. "
                             f"This could save {interest_saved_monthly:.2f} BDT in interest and reduce the term by "
                             f"{int(loan.remaining_payments - new_term_monthly)} months.",
                        type="frequency"
                    )
                )

        # Suggestion 3: Early Payment if Few Remaining Payments
        if loan.remaining_payments <= 3 and remaining_principal > 0:
            total_to_pay = remaining_principal + (monthly_interest * loan.remaining_payments / (payments_per_year / 12))
            suggestions.append(
                Suggestion(
                    text=f"Pay off {loan.lender_name} loan early with {total_to_pay:.2f} BDT to clear the remaining {loan.remaining_payments} {loan.payment_frequency.value.lower()} payments.",
                    type="early"
                )
            )

        # Add loan suggestion if there are any suggestions
        if suggestions:
            loan_suggestions.append(
                LoanSuggestion(
                    loan_id=loan.id,
                    lender_name=loan.lender_name,
                    loan_type=loan.loan_type,
                    start_date=loan.start_date,
                    end_date=loan.end_date,
                    suggestions=suggestions
                )
            )

    return loan_suggestions