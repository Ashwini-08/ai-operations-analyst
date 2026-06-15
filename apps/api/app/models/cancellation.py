from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Cancellation(Base):
    __tablename__ = "cancellations"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    cancellation_date = Column(Date, nullable=False)
    cancellation_reason = Column(String(255), nullable=False)
    churn_risk_segment = Column(String(50), nullable=False)
    notes = Column(String(500), nullable=True)

    customer = relationship("Customer", back_populates="cancellations")