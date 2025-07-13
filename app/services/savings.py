import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime

def predict_monthly_savings(goals):
    suggestions = []
    current_date = datetime(2025, 7, 13, 14, 36)  # Updated to current date and time: 02:36 PM +06
    for goal in goals:
        if not goal.end_date or goal.status != "In Progress":
            continue
        remaining = goal.target_amount - goal.current_amount
        try:
            end_date = np.datetime64(goal.end_date)
            days_left = (end_date - np.datetime64(current_date)).astype('timedelta64[D]').astype(int)
            if days_left <= 0:
                continue
            X = np.array([[days_left]]).reshape(-1, 1)
            y = np.array([remaining])
            model = LinearRegression().fit(X, y)
            monthly_savings = model.predict([[30]])[0] / 30
            if monthly_savings > 0:
                suggestions.append(f"Increase monthly savings for {goal.title} by {monthly_savings:.2f} BDT")
        except ValueError:
            continue
    return suggestions

def suggest_expense_cuts(goals):
    # Mock expense data with numeric amounts and categories
    expenses = np.array([[700.0, "Leisure"], [3000.25, "Household"]], dtype=object)
    kmeans = KMeans(n_clusters=2, random_state=0).fit(expenses[:, 0].reshape(-1, 1).astype(float))
    labels = kmeans.labels_
    suggestions = []
    for i in range(len(labels)):
        if labels[i] == 1:
            amount = float(expenses[i][0])  # Ensure amount is treated as float
            category = expenses[i][1]
            suggestions.append(f"Cut {category} by {amount * 0.2:.2f} BDT")
    return suggestions

def forecast_savings_growth(goals):
    suggestions = []
    for goal in goals:
        if goal.status != "In Progress":
            continue
        history = [goal.current_amount - sum(e.amount for e in goal.goal_entries)]
        try:
            model = ARIMA(history, order=(1, 1, 1))
            model_fit = model.fit()
            automated_savings = model_fit.forecast(steps=1)[0] + 1000
            if automated_savings > goal.current_amount:
                suggestions.append(f"Automate {automated_savings - goal.current_amount:.2f} BDT monthly savings/side income for {goal.title}")
        except Exception:
            continue
    return suggestions