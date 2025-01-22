from fastapi import Depends, Query, FastAPI, HTTPException, status
from typing import List, Optional, Dict
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from demo import *
from models import *
from additionalFucntions import *
from fastapi.responses import JSONResponse
#from fastapi.encoders import jsonable_encoder
#from fastapi.security import OAuth2PasswordRequestForm
#import json


app = FastAPI()

origins = [
    "http://localhost:5173",  # Add your frontend URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins from the list above
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.post("/authentication", tags=['Authentication'])
async def signup(email: str, username: str, password: str, phone_number: str = None):
    try:
        signup_response = await signupOnFirebase(email, password, username)
        user_id = signup_response[0]
        if "successfully signed up" in signup_response[1]:
            response = await add_user_auth_data(
                userID=user_id,
                userEmail=email,
                username=username,
                phoneNumber=phone_number
            )
            return response
        else:
            raise HTTPException(status_code=400, detail=signup_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login", tags=['Authentication'])
async def sign_in(user_info: UserInfo):
    print(user_info)
    user_info = user_info.model_dump()  # Convert the Pydantic model to a dictionary
    print(user_info)
    try:
        # Call the login function and check for successful login
        response = await loginOnFirebase(user_info["email"], user_info["password"])
        if 'error' in response:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response['error'])
        return JSONResponse(content=response)  # Directly return the response from Firebase
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")




@app.get("/user/{user_id}", tags=['Users'])
async def get_user(user_id: str):
    try:
        return await get_document(user_data_collection.document(user_id), details=True)
    except Exception as e:
        return f"Error retrieving user: {str(e)}"


@app.get("/user", tags=['Users'])
async def get_all_users():
    return await get_collection(user_auth_collection.stream(), details=True)


@app.delete("/user/{user_id}", tags=['Users'])
async def delete_user(user_id: str):
    return await delete_user_from_firestore(user_id)


@app.put("/users/{user_id}", tags=['Users'])
async def update_user(user_id: str, user_email: str = None, username: str = None, phone_number: str = None, profile_image_url: str = None, description: str = None):
    return await update_user_data(user_id, user_email, username, phone_number, profile_image_url, description)


@app.put("/user/{user_email}", tags=['Users'])
async def update_user_recipes_allergies(user_email: str, recipes: Optional[list[str]] = None, allergies: Optional[list[str]] = None):
    try:
        if not recipes and not allergies:
            raise HTTPException(status_code=400, detail="At least one of 'recipes' or 'allergies' must be provided.")
        return await update_user_r_a(user_email, recipes, allergies)
    
    except HTTPException as e:
        print(f"HTTP exception: {str(e.detail)}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")




@app.get("/recipes", tags=['Recipes'])
async def get_all_recipes():
    return await get_collection(recipe_collection.stream(), details=True)


@app.get("/check_recipe/{recipe_name}", tags=['Recipes'])
async def check_recipes(recipe_name: str):
    return await check_recipe(recipe_name)


@app.post("/add_recipe", tags=['Recipes'])
async def add_recipe(recipe: Recipe):
    t = await get_collection(recipe_collection.stream(), details=False)
    recipe_id = check_missing_index(t)
    return await new_recipe(recipe, recipe_id)

@app.get("/check_recipe/{recipe_id}", tags=['Recipes'])
async def get_recipe_id(recipe_id: str):
    return await get_document(recipe_collection.document(recipe_id), details=True)



@app.post("/ingredients", tags=['Ingredients'])
async def add_ingredients(ingredient: str, recipe_id: str):
    return await check_ingredient_index(ingredient, recipe_id)


@app.post("/ingredients/search", tags=['Ingredients'])
async def ingredients_to_recipes(ingredients: List[str]):
    return await i_to_r(ingredients)

