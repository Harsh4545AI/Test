from pydantic import BaseModel
from typing import List

class Ingredients(BaseModel):
    name: str
    type: str
    confidence: float
    details: str = ""



class ImageAgentResponse(BaseModel):
    description: str
    ingredients: List[Ingredients] = []
