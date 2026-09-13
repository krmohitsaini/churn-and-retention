from backend.app.kpis.churn_kpis import gross_churn_rate
from backend.app.kpis.portfolio_kpis import active_customer_count, average_tenure_months
from backend.app.kpis.revenue_kpis import revenue_at_risk


def test_active_customer_count():
    customers = [{"current_status": "Active"}, {"current_status": "Churned"}, {"current_status": "Active"}]
    assert active_customer_count(customers) == 2


def test_average_tenure_months():
    customers = [
        {"current_status": "Active", "tenure_months": 10},
        {"current_status": "Active", "tenure_months": 20},
    ]
    assert average_tenure_months(customers) == 15


def test_gross_churn_rate():
    assert gross_churn_rate([{}, {}], 10) == 0.2


def test_revenue_at_risk():
    customers = [
        {"estimated_annual_value": 1000, "churn_probability": 0.5},
        {"estimated_annual_value": 500, "churn_probability": 0.2},
    ]
    assert revenue_at_risk(customers) == 600

