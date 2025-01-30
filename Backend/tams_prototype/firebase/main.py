from fastapi import Depends, Query, FastAPI, HTTPException, status
# from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
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
    "http://localhost:5173", "https://vietspark-v1.vercel.app/" # Add your frontend URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins from the list above
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.post("/authentication", tags=['Authentication'])
async def signup(signup_data: UserSignUpModel):
    try:
        signup_response = await signupOnFirebase(signup_data)
        user_id = signup_response[0]
        if "successfully signed up" in signup_response[1]:
            response = await add_user_data(user_id, signup_data)
            return response
        else:
            raise HTTPException(status_code=400, detail=signup_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login", tags=['Authentication'])
async def sign_in(user_info: UserLoginModel):
    # print(user_info)
    # user_info = user_info.model_dump()  # Convert the Pydantic model to a dictionary
    # print(user_info)
    try:
        # Call the login function and check for successful login
        # response = await loginOnFirebase(user_info["email"], user_info["password"])
        response = await loginOnFirebase(user_info.email, user_info.password)
        if 'error' in response:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response['error'])
        return JSONResponse(content=response)  # Directly return the response from Firebase
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")




@app.get("/get_user/{user_id}", tags=['Users'])
async def get_user(user_id: str):
    try:
        return await get_document(user_collection.document(user_id.strip()), details=True)
    except Exception as e:
        return f"Error retrieving user: {str(e)}"


@app.get("/get_all_users", tags=['Users'])
async def get_all_users():
    try:
        return await get_collection(user_collection.stream(), details=True)
    except Exception as e:
        return f"Error retrieving user: {str(e)}"


@app.delete("/delete_user/{user_id}", tags=['Users'])
async def delete_user(user_id: str):
    return await delete_user_from_firestore(user_id)


@app.put("/update_user/{user_id}", tags=['Users'])
# async def update_user(user_id: str, user_email: str = None, username: str = None, phone_number: str = None, profile_image_url: str = None, description: str = None):
async def update_user(user_data: UserUpdateModel):
    print(user_data)
    return await update_user_data(user_data)


@app.put("/update_user_recipes_allergies/{user_id}", tags=['Users'])
# async def update_user_recipes_allergies(user_id: Optional[str], recipes: Optional[list[str]] = None, allergies: Optional[list[str]] = None):
async def update_user_recipes_allergies(user_data: UserUpdateRecipeAllergiesModel):
    try:
        if not user_data.recipes and not user_data.allergies:
            raise HTTPException(status_code=400, detail="At least one of 'recipes' or 'allergies' must be provided.")
        return await update_user_r_a(user_data.user_id, user_data.recipes, user_data.allergies)
    
    except HTTPException as e:
        print(f"HTTP exception: {str(e.detail)}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")




@app.get("/get_all_recipes", tags=['Recipes'])
async def get_all_recipes():
    collection = await get_collection(recipe_collection.stream(), details=True)
    for recipe in collection:
        recipe.pop("instructions", None)
        recipe.pop("searchable_ingredient", None)
        recipe.pop("searchable_recipe_name", None)
        recipe["ingredients"] = len(recipe['ingredients'])
    # p_c = json.dumps(collection, indent=4)
    return collection


@app.get("/get_recipe_by_name/{recipe_name}", tags=['Recipes'])
async def get_recipe_by_name(recipe_name: str):
    
    return await check_recipe(recipe_name.strip())


@app.post("/add_new_recipe", tags=['Recipes'])
async def add_recipe(recipe: RecipeModel):
    check = await check_recipe(recipe.name)
    if check == "Recipe not in database":
        return await new_recipe(recipe)
    return check


@app.get("/get_recipe_by_id/{recipe_id}", tags=['Recipes'])
async def get_recipe_by_id(recipe_id: str):
    recipe = await get_document(recipe_collection.document(recipe_id.strip()), details=True)
    recipe.pop("searchable_ingredient", None)
    recipe.pop("searchable_recipe_name", None)
    return recipe




@app.get("/ingredients_to_recipes", tags=['Ingredients'])
async def ingredients_to_recipes(ingredients: str):
    return await i_to_r(ingredients)




@app.post("/GPT_to_recipe", tags=['GPT'])
async def send_ingredients_to_GPT(ingredient: str):
    response_list =  await GPT_response_to_ingredientS(ingredient)
    check = await check_recipe(response_list[0])
    if check == "Recipe not in database":
        return await new_recipe(response_list[1])
    return check
    # return await GPT_response_to_ingredientS(ingredient)




# @app.get("/get_image", tags=['Experimental'])
# async def get_image():
#     image_path = Path(r"C:\Users\t\Desktop\1683115847268.jpg")
#     if not image_path.is_file():
#         return {"error": "Image not found on the server"}
#     return FileResponse(image_path)


# @app.post("/upload-image/", tags=['Experimental'])
# async def upload_image(file: UploadFile = File(...)):
#     return await image_to_storage(file)







