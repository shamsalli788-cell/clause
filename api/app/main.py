from services.ingestion import ingest 
from services.chat import RAGService


def main() ->None:
    
print(f"Ingested {ingest()}chunks!")
