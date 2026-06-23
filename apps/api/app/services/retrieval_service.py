from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from sqlalchemy.orm import Session


MODEL_NAME = "all-MiniLM-L6-v2"
_model = SentenceTransformer(MODEL_NAME)


def retrieve_relevant_context(
    query: str,
    db: Session,
    top_k: int = 3,
):
    query_embedding = _model.encode(query).tolist()

    results = db.execute(
        text("""
            SELECT
                id,
                doc_name,
                section_title,
                content,
                embedding <-> CAST(:query_embedding AS vector) AS distance
            FROM knowledge_documents
            ORDER BY embedding <-> CAST(:query_embedding AS vector)
            LIMIT :top_k
        """),
        {
            "query_embedding": str(query_embedding),
            "top_k": top_k,
        },
    ).mappings().all()

    return [
        {
            "id": row["id"],
            "doc_name": row["doc_name"],
            "section_title": row["section_title"],
            "content": row["content"],
            "score": float(row["distance"]),
        }
        for row in results
    ]