from pydantic import BaseModel


class SearchResult(BaseModel):
    source: str
    title: str
    content: str
    score: float
