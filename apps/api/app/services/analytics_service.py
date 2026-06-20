from sqlalchemy import text
from sqlalchemy.orm import Session


def get_churn_summary_data(db: Session):
    total_customers = db.execute(
        text("SELECT COUNT(*) FROM customers")
    ).scalar()

    churned_customers = db.execute(
        text("SELECT COUNT(*) FROM customers WHERE status = 'churned'")
    ).scalar()

    churn_rate = round((churned_customers / total_customers) * 100, 2)

    return {
        "total_customers": total_customers,
        "churned_customers": churned_customers,
        "churn_rate_percent": churn_rate,
    }


def get_revenue_impact_data(db: Session):
    result = db.execute(
        text("""
            SELECT
                COUNT(ca.id) AS churned_customers,
                COALESCE(SUM(s.monthly_recurring_revenue), 0) AS lost_monthly_revenue,
                COALESCE(SUM(s.monthly_recurring_revenue) * 12, 0) AS lost_annual_revenue
            FROM cancellations ca
            JOIN subscriptions s
                ON ca.customer_id = s.customer_id
        """)
    ).mappings().first()

    return {
        "churned_customers": result["churned_customers"],
        "lost_monthly_revenue": float(result["lost_monthly_revenue"]),
        "lost_annual_revenue": float(result["lost_annual_revenue"]),
    }


def get_support_analysis_data(db: Session):
    results = db.execute(
        text("""
            SELECT
                st.category,
                st.sentiment,
                COUNT(*) AS ticket_count
            FROM support_tickets st
            GROUP BY st.category, st.sentiment
            ORDER BY ticket_count DESC
        """)
    ).mappings().all()

    return {
        "support_ticket_breakdown": [
            {
                "category": row["category"],
                "sentiment": row["sentiment"],
                "ticket_count": row["ticket_count"],
            }
            for row in results
        ]
    }


def get_regional_churn_data(db: Session):
    results = db.execute(
        text("""
            SELECT
                c.region,
                COUNT(ca.id) AS churned_customers
            FROM cancellations ca
            JOIN customers c
                ON ca.customer_id = c.id
            GROUP BY c.region
            ORDER BY churned_customers DESC
        """)
    ).mappings().all()

    return {
        "regional_churn": [
            {
                "region": row["region"],
                "churned_customers": row["churned_customers"],
            }
            for row in results
        ]
    }


def get_top_cancellation_reason_data(db: Session):
    result = db.execute(
        text("""
            SELECT
                cancellation_reason,
                COUNT(*) AS reason_count
            FROM cancellations
            GROUP BY cancellation_reason
            ORDER BY reason_count DESC
            LIMIT 1
        """)
    ).mappings().first()

    return {
        "cancellation_reason": result["cancellation_reason"],
        "reason_count": result["reason_count"],
    }