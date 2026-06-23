from sqlalchemy import Column, Integer, String, Text
from pgvector.sqlalchemy import Vector

from app.database import Base


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id = Column(Integer, primary_key=True, index=True)
    doc_name = Column(String(255), nullable=False)
    section_title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384), nullable=False)