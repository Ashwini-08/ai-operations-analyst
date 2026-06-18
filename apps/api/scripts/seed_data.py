import random
from datetime import date, datetime, timedelta

from faker import Faker

from app.database import SessionLocal
from app.models.customer import Customer
from app.models.subscription import Subscription
from app.models.cancellation import Cancellation
from app.models.support_ticket import SupportTicket
from app.models.product_usage import ProductUsage


fake = Faker()

REGIONS = ["North America", "Europe", "Asia Pacific", "Latin America"]
INDUSTRIES = ["Healthcare", "Finance", "Retail", "Education", "Technology"]
PLAN_TYPES = ["Basic", "Pro", "Enterprise"]
BILLING_CYCLES = ["Monthly", "Annual"]

CANCELLATION_REASONS = [
    "Billing issues",
    "Low product adoption",
    "Missing features",
    "Poor support experience",
    "Switched to competitor",
]

SUPPORT_CATEGORIES = [
    "Billing",
    "Technical Issue",
    "Feature Request",
    "Onboarding",
    "Account Management",
]

FEATURES = [
    "Dashboard",
    "Reporting",
    "Integrations",
    "Automation",
    "Forecasting",
]


def random_date_within_last_year():
    return date.today() - timedelta(days=random.randint(1, 365))


def create_customers(db, count=1000):
    customers = []

    for _ in range(count):
        customer = Customer(
            customer_name=fake.company(),
            industry=random.choice(INDUSTRIES),
            region=random.choice(REGIONS),
            plan_type=random.choice(PLAN_TYPES),
            signup_date=random_date_within_last_year(),
            status="active",
        )
        db.add(customer)
        customers.append(customer)

    db.commit()

    for customer in customers:
        db.refresh(customer)

    return customers


def create_subscriptions(db, customers):
    for customer in customers:
        mrr = {
            "Basic": random.randint(49, 199),
            "Pro": random.randint(200, 999),
            "Enterprise": random.randint(1000, 5000),
        }[customer.plan_type]

        start_date = customer.signup_date
        renewal_date = start_date + timedelta(days=365)

        subscription = Subscription(
            customer_id=customer.id,
            billing_cycle=random.choice(BILLING_CYCLES),
            monthly_recurring_revenue=mrr,
            start_date=start_date,
            renewal_date=renewal_date,
            status="active",
        )
        db.add(subscription)

    db.commit()


def create_support_tickets(db, customers):
    for customer in customers:
        ticket_count = random.randint(0, 6)

        if customer.region == "North America":
            ticket_count += random.randint(0, 3)

        for _ in range(ticket_count):
            category = random.choice(SUPPORT_CATEGORIES)

            ticket = SupportTicket(
                customer_id=customer.id,
                created_at=datetime.now() - timedelta(days=random.randint(1, 180)),
                category=category,
                priority=random.choice(["Low", "Medium", "High"]),
                sentiment=random.choice(["Positive", "Neutral", "Negative"]),
                status=random.choice(["Open", "Resolved", "Escalated"]),
                description=fake.sentence(nb_words=12),
            )
            db.add(ticket)

    db.commit()


def create_product_usage(db, customers):
    for customer in customers:
        for feature in FEATURES:
            usage_count = random.randint(0, 100)

            if customer.plan_type == "Enterprise":
                usage_count += random.randint(20, 80)

            usage = ProductUsage(
                customer_id=customer.id,
                usage_month=date.today().replace(day=1),
                feature_name=feature,
                usage_count=usage_count,
                active_users=random.randint(1, 50),
                health_score=random.randint(20, 100),
            )
            db.add(usage)

    db.commit()


def create_cancellations(db, customers):
    churn_candidates = random.sample(customers, int(len(customers) * 0.18))

    for customer in churn_candidates:
        reason = random.choice(CANCELLATION_REASONS)

        if customer.region == "North America":
            reason = random.choice(["Billing issues", "Poor support experience"])

        customer.status = "churned"

        cancellation = Cancellation(
            customer_id=customer.id,
            cancellation_date=random_date_within_last_year(),
            cancellation_reason=reason,
            churn_risk_segment=random.choice(["Low", "Medium", "High"]),
            notes=fake.sentence(nb_words=15),
        )
        db.add(cancellation)

    db.commit()


def seed_database():
    db = SessionLocal()

    try:
        print("Seeding customers...")
        customers = create_customers(db)

        print("Seeding subscriptions...")
        create_subscriptions(db, customers)

        print("Seeding support tickets...")
        create_support_tickets(db, customers)

        print("Seeding product usage...")
        create_product_usage(db, customers)

        print("Seeding cancellations...")
        create_cancellations(db, customers)

        print("Seed data inserted successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()