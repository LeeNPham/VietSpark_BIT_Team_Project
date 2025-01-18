from pydantic import BaseModel
from typing import List, Optional, Dict


class UserInfo(BaseModel):
  email: str
  password: str


class Ingredient(BaseModel):
  name: str
  amount: str
  recipe_index: List[int] = []


class Recipe (BaseModel):
  name: str
  ingredients: List[Ingredient]
  instructions: List[str]
  duration: int
  img_url: str
  serving: int







{
  "id": "000001",
  "name": "scramble egg",
  "ingredients": [
    {
      "name": "egg",
      "amount": "1",
      "recipe_index": [
        "000001"
      ]
    }
  ],
  "instructions": [
    "oil up the pan",
    "break egg to pan",
    "scramble"
  ],
  "duration": 15,
  "img_url": "img"
}










