from pydantic import BaseModel
from typing import List

class QueryModel(BaseModel):
    keyword: str

class MultiSearchQuery(BaseModel):
    keywords: List[str]
