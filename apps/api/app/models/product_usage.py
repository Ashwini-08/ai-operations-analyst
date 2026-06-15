from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class ProductUsage(Base):
    __tablename__ = "product_usage"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    usage_month = Column(Date, nullable=False)
    feature_name = Column(String(100), nullable=False)
    usage_count = Column(Integer, nullable=False)
    active_users = Column(Integer, nullable=False)
    health_score = Column(Integer, nullable=False)

    customer = relationship("Customer", back_populates="product_usage")