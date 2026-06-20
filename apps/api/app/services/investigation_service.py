from sqlalchemy.orm import Session

from app.services.analytics_service import (
    get_churn_summary_data,
    get_regional_churn_data,
    get_revenue_impact_data,
    get_top_cancellation_reason_data,
)


def investigate_churn(db: Session):
    churn_summary = get_churn_summary_data(db)
    revenue_impact = get_revenue_impact_data(db)
    regional_churn = get_regional_churn_data(db)
    top_reason = get_top_cancellation_reason_data(db)

    top_region = regional_churn["regional_churn"][0]

    findings = [
        f"Overall churn rate is {churn_summary['churn_rate_percent']}% across {churn_summary['total_customers']} customers.",
        f"{churn_summary['churned_customers']} customers have churned.",
        f"The highest churn region is {top_region['region']} with {top_region['churned_customers']} cancellations.",
        f"The leading cancellation reason is '{top_reason['cancellation_reason']}' with {top_reason['reason_count']} cases.",
        f"Estimated lost monthly revenue is ${revenue_impact['lost_monthly_revenue']:,.2f}.",
        f"Estimated lost annual revenue is ${revenue_impact['lost_annual_revenue']:,.2f}.",
    ]

    recommendations = [
        "Prioritize retention campaigns in the highest-churn region.",
        "Investigate the leading cancellation reason and create a targeted mitigation plan.",
        "Review support and billing workflows for churned customers.",
        "Create a customer success playbook for accounts showing low engagement or negative support sentiment.",
    ]

    return {
        "problem": "Customer churn investigation",
        "summary": (
            f"Customer churn is currently {churn_summary['churn_rate_percent']}%, "
            f"representing {churn_summary['churned_customers']} lost customers."
        ),
        "findings": findings,
        "recommendations": recommendations,
        "metrics": {
            "total_customers": churn_summary["total_customers"],
            "churned_customers": churn_summary["churned_customers"],
            "churn_rate_percent": churn_summary["churn_rate_percent"],
            "lost_monthly_revenue": revenue_impact["lost_monthly_revenue"],
            "lost_annual_revenue": revenue_impact["lost_annual_revenue"],
            "top_region": top_region["region"],
            "top_cancellation_reason": top_reason["cancellation_reason"],
        },
    }