from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    category = Column(String(100), nullable=False)
    priority = Column(String(50), nullable=False)
    sentiment = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)

    customer = relationship("Customer", back_populates="support_tickets")