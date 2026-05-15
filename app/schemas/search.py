from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    limit: int = 5

class SearchResult(BaseModel):
    content: str
    document_id: int
    score: float # Similarity score. Чем выше, тем релевантнее результат
