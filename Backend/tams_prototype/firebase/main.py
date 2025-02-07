from fastapi import Depends, Query, FastAPI, HTTPException, status, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from demo import *
from models import *
from additionalFucntions import *
from fastapi.responses import JSONResponse
from pathlib import Path
from pathlib import Path
#from fastapi.encoders import jsonable_encoder
#from fastapi.security import OAuth2PasswordRequestForm
#import json


app = FastAPI(
    title="Project VietSpark",
    version="1.0.13",
    openapi_version="3.1.0"
)

origins = [
    "http://localhost:5173", "https://vietspark-v1.vercel.app", "https://vietsparkv1.vercel.app" # Add your frontend URL here
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




@app.get("/users/{user_id}", tags=['Users'])
async def get_user(user_id: str):
    try:
        return await get_document(user_collection.document(user_id.strip()), details=True)
    except Exception as e:
        return f"Error retrieving user: {str(e)}"


@app.get("/users", tags=['Users'])
async def get_all_users():
    try:
        return await get_collection(user_collection.stream(), details=True)
    except Exception as e:
        return f"Error retrieving user: {str(e)}"


@app.delete("/users/{user_id}", tags=['Users'])
async def delete_user(user_id: str):
    return await delete_user_from_firestore(user_id)


@app.put("/users/{user_id}", tags=['Users'])
# async def update_user(user_id: str, user_email: str = None, username: str = None, phone_number: str = None, profile_image_url: str = None, description: str = None):
async def update_user(user_data: UserUpdateModel):
    return await update_user_data(user_data)


@app.put("/users/recipes_allergies/{user_id}", tags=['Users'])
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



#GET cannot pass a body, only parameters
@app.get("/recipes", tags=['Recipes'])
async def get_recipes(
    name: Optional[str] = None, 
    author: Optional[str] = None, 
    calories: Optional[int] = None, 
    time: Optional[int] = None
    ):

    return await recipe_database_search(name, author, calories, time)


@app.get("/recipes/{recipe_id}", tags=["Recipes"])
async def get_recipe_by_id(recipe_id: str):
    return await search_recipe_by_id(recipe_id)


@app.post("/recipes", tags=['Recipes'])
async def user_added_recipe(recipe: RecipeModel):
    return await new_recipe(recipe, None)




#Need a string of ingredients
@app.get("/GPT_ingredients_to_recipe", tags=['GPT'])
async def ingredients_to_GPT(ingredients: str, user_id: Optional[str] = None):
    try:
        check_ingredients = await search_recipe_by(ingredients, "searchable_ingredient")
        if check_ingredients != []:
            return check_ingredients
        response_list = await GPT_to_recipe(ingredients)

        # check_name = await search_recipe_by(response_list[0], "searchable_recipe_name")
        # if check_name != "no match":
        #     return check_name
        response = await new_recipe(response_list[1], user_added = False)
        return [response]
    
    except Exception as e:
        print(f"Error in ingredients_to_GPT: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating recipe: {str(e)}")




@app.get("/get_image_url/{file_name}", tags=['Experimental'])
async def get_image(file_name: str):
# async def get_image():
    img_url = await get_image_from_firebase(file_name)
    return img_url
    # return StreamingResponse(img, media_type="image/jpeg", filename=file_name)
    
    # image_path = Path(r"C:\Users\t\Desktop\1683115847268.jpg")
    # if not image_path.is_file():
    #     return {"error": "Image not found on the server"}
    # return FileResponse(image_path)


@app.post("/upload-image/file", tags=['Experimental'])
async def upload_image(file: UploadFile = File(...)):
    return await image_to_storage(file)


@app.post("/upload-image/{url}", tags=['Experimental'])
async def upload_image_by_url(url: str):
    return await image_url_to_storage(url)


@app.get("/generate-image", tags=['Experimental'])
async def generate_image(item: str):
    return await GPT_image(item, item)

    # image_data = requests.get(image_url).content
    # img_byte_arr = io.BytesIO(image_data)
    # StreamingResponse(img_byte_arr, media_type="image/png")@app.post("/upload-image/{url}", tags=['Experimental'])
async def upload_image_by_url(url: str):
    return await image_url_to_storage(url)


@app.get("/generate-image/", tags=['Experimental'])
async def generate_image(item: str):
    return await GPT_image(item, item)

    # image_data = requests.get(image_url).content
    # img_byte_arr = io.BytesIO(image_data)
    # StreamingResponse(img_byte_arr, media_type="image/png")




