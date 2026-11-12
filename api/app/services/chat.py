from langchain.chat_models import init_chat_model
from langchain_qdrant import QdrantVectorStore
from pydantic import BaseModel 

from core.config import get_settings, get_embeddings, get_qdrant_client

NO_ANSWER = ""

class source():
    source:str
    page: int | None=None
    score: float

class Answer(BaseModel):
    answer: str
    sources: list[source]

class RAGService:
    def __init__(self) -> None:
          self.settings = get_settings()
          self.client = get_qdrant_client(settings=self.settings):

          if not self.client.collection_exists(collection_name=self.settings.qdrant_collection):
              raise ValueError(f"Collection {self.settings.qdrant_collection} does not exist. Please run the ingestion process first.")
          self.store = QdrantVectorStore(
              client=self.client,
              collection_name=self.settings.collection_name,
              embedding=get_embeddings(settings=self.settings)
          )
          self.llm = init_chat_model(
               model=self.settings.chat_model,
               provider=self.settings.chat_provider,
               temperature=self.settings.temperature)

    def ask(self, question: str) -> None:
         question = question.strip()

         if not question:
                raise ValueError("Question cannot be empty.")
         results = self.store.similarity_search_with_score(
                query=question,
                k=self.settings.top_k
         )

         if not results:
                return Answer(answer="NO_ANSWER", sources=[])
         context = "/n/n".join(doc.page_content for doc, _ in results)

         message = [
                {"role": "system", "content": self.settings.system},
                {"role": "user", "content": f"Context: {context}"},
                {"role": "user", "content": f"Question: {question}"}
         ]

         return Answer(
              answer= self.llm.invoke(input=messages).text,
                sources=[
                     source(
                          source=doc.metadata.get("source", "unknown"),
                          page=doc.metadata.get("page"),
                          score=round(number=store, ndigits=4)
                  )
                   for doc, store in results
                   ]
         )
         

    def close(self) -> None:
            self.client.close()
              