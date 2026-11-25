from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Request
from pydantic import BaseModel, StringConstraints

from app.services.chat import Answer, RAGService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.agent = RAGService()
    yield
    # app.state.rag.close()


app = FastAPI(title="Clause APIs", lifespan=lifespan)


class AskQuestion(BaseModel):
    question: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)
    ]


@app.get(path="/")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(path="/ask", response_model=Answer)
def ask_query(body: AskQuestion, req: Request):
    return req.app.state.rag_service.ask(body.question)
