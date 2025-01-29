from pydantic import BaseModel
from typing import List, Optional, Dict

class publicProfile(BaseModel):
    user_id: Optional[str] = (None,)
    user_email: Optional[str] = (None,)
    user_name: Optional[str] = (None,)  # Adjust if you collect the user's name
    recipes: Optional[list[str]] = (None,)  # Initialize empty lists
    allergies: Optional[List[str]] = None


class UserLoginModel(BaseModel):
  email: str
  password: str

class UserSignUpModel(BaseModel):
  email: str
  username: str
  password: str
  phone_number: str

class UserUpdateModel(BaseModel):
  user_id: str
  email: str
  username: str
  password: str
  phone_number: str
  profile_image_url: str
  description: str

class UserUpdateRecipeAllergiesModel(BaseModel):
  user_id: str
  recipes: List[str]
  allergies: List[str]

class authProfile(BaseModel):
   uid: str
   email:str
   username: str
   profile_image: Optional[str]
   phone_number: Optional[str]
  #  disabled: False


class IngredientModel(BaseModel):
  ingredientName: str
  ingredientAmount: str

class SearchIngredientsModel(BaseModel):
   ingredients: List[str]

class AddIngredientModel(BaseModel):
   ingredient: str
   recipe_id: str

class RecipeModel (BaseModel):
  name: str
  ingredients: List[IngredientModel]
  instructions: List[str]
  time: str
  img_url: str = ""
  servings: int
  calories: int
  author: str






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






