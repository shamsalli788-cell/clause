from langchain.tools import tool
from langchain_qdrant import QdrantVectorStore

from app.schemas.retrieval import Source


def file_search(store: QdrantVectorStore, top_k: int):
    @tool(response_format="content_and_artifact")
    def search_handbook(query: str) -> tuple[str, list[Source]]:
        """Search the Clause shop handbook: refunds, delivery times and fees,
        payments, cash on delivery, warranty, exchanges, tracking, loyalty, support hours.
        Use a short query like "refund window electronics"."""

        results = store.similarity_search_with_score(
            query=query,
            k=top_k,
        )
        if not results:
            return "Nothing found.", []

        text = "\n\n---\n\n".join(doc.page_content for doc, _ in results)
        sources = [
            Source(
                source=doc.metadata.get("source", "unknown"),
                page=doc.metadata.get("page"),
                score=round(score, 4),
            )
            for doc, score in results
        ]
        # content -> goes to the LLM; artifact (sources) -> stays with us
        return text, sources

    return search_handbook
