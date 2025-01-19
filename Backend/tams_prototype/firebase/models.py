from pydantic import BaseModel
from typing import List, Optional, Dict

class publicProfile(BaseModel):
    user_id: Optional[str] = (None,)
    user_email: Optional[str] = (None,)
    user_name: Optional[str] = (None,)  # Adjust if you collect the user's name
    recipes: Optional[list[str]] = (None,)  # Initialize empty lists
    allergies: Optional[List[str]] = None

class UserInfo(BaseModel):
  email: str
  password: str


class Ingredient(BaseModel):
  name: str
  amount: str
  # recipe_index: List[str] = []


class Recipe (BaseModel):
  name: str
  ingredients: List[Ingredient]
  instructions: List[str]
  time: str
  img_url: str = ""
  servings: str
  calories: str






{
  "id": "000001",
  "name": "scramble egg",
  "ingredients": [
    {
      "name": "egg",
      "amount": "1",
      "recipe_index": []
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



{
  "recipe": {
    "name": "string",
    "ingredients": [
      {
        "name": "string1",
        "amount": "1",
        "recipe_index": []
      },
      {
        "name": "string2",
        "amount": "2",
        "recipe_index": []
      },
      {
        "name": "string3",
        "amount": "3",
        "recipe_index": []
      },
    ],
    "instructions": [
      "string"
    ],
    "time": 0,
    "img_url": "",
    "servings": 0,
    "calories": 0
  },
  "ingredient": {
    "name": "string",
    "amount": "string",
    "recipe_index": []
  }
}






