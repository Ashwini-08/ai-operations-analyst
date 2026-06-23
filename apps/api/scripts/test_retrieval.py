from app.database import SessionLocal
from app.services.retrieval_service import retrieve_relevant_context


def main():
    db = SessionLocal()

    try:
        query = "How should we respond to billing-related churn?"
        results = retrieve_relevant_context(query=query, db=db, top_k=3)

        print(f"Query: {query}")
        print("-" * 80)

        for result in results:
            print(f"Doc: {result['doc_name']}")
            print(f"Score: {result['score']}")
            print(result["content"][:500])
            print("-" * 80)

    finally:
        db.close()


if __name__ == "__main__":
    main()