from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    industry = Column(String(100), nullable=False)
    region = Column(String(50), nullable=False)
    plan_type = Column(String(50), nullable=False)
    signup_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)

    subscriptions = relationship("Subscription", back_populates="customer")
    cancellations = relationship("Cancellation", back_populates="customer")
    support_tickets = relationship("SupportTicket", back_populates="customer")
    product_usage = relationship("ProductUsage", back_populates="customer")