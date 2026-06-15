from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    billing_cycle = Column(String(50), nullable=False)
    monthly_recurring_revenue = Column(Numeric(10, 2), nullable=False)
    start_date = Column(Date, nullable=False)
    renewal_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)

    customer = relationship("Customer", back_populates="subscriptions")