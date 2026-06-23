from pathlib import Path

from sentence_transformers import SentenceTransformer

from app.database import SessionLocal
from app.models.knowledge_document import KnowledgeDocument


KNOWLEDGE_DIR = Path(__file__).resolve().parents[3] / "data" / "knowledge"
MODEL_NAME = "all-MiniLM-L6-v2"


def chunk_text(text: str, max_chars: int = 800):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) <= max_chars:
            current_chunk += "\n\n" + paragraph if current_chunk else paragraph
        else:
            chunks.append(current_chunk)
            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def get_section_title(chunk: str):
    for line in chunk.splitlines():
        if line.startswith("#"):
            return line.replace("#", "").strip()
    return None


def ingest_knowledge_docs():
    db = SessionLocal()
    model = SentenceTransformer(MODEL_NAME)

    try:
        print(f"Reading docs from: {KNOWLEDGE_DIR}")

        docs = list(KNOWLEDGE_DIR.glob("*.md"))

        if not docs:
            print("No markdown docs found.")
            return

        print("Clearing existing knowledge documents...")
        db.query(KnowledgeDocument).delete()
        db.commit()

        total_chunks = 0

        for doc_path in docs:
            content = doc_path.read_text(encoding="utf-8")
            chunks = chunk_text(content)

            print(f"Ingesting {doc_path.name}: {len(chunks)} chunks")

            for chunk in chunks:
                embedding = model.encode(chunk).tolist()

                record = KnowledgeDocument(
                    doc_name=doc_path.name,
                    section_title=get_section_title(chunk),
                    content=chunk,
                    embedding=embedding,
                )

                db.add(record)
                total_chunks += 1

        db.commit()
        print(f"Inserted {total_chunks} knowledge chunks successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    ingest_knowledge_docs()