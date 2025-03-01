from fastapi import Header, Depends, Query, FastAPI, HTTPException, status, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict
from pydantic import BaseModel
from demo import *
from models import *
from additionalFucntions import *
from fastapi.responses import JSONResponse
from pathlib import Path
import time
import asyncio
import logging

#from fastapi.encoders import jsonable_encoder
#from fastapi.security import OAuth2PasswordRequestForm
#import json

app = FastAPI(
    title="Project VietSpark",
    version="1.0.13",
    openapi_version="3.1.0"
)

origins = [
    "http://localhost:5173",
    "https://vietspark-v1.vercel.app",
    "https://vietsparkv1.vercel.app"
    # "https://api.openai.com",
    # "https://chat.openai.com",
    # "https://platform.openai.com" # Add your frontend URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)



@app.post("/authentication", tags=['Authentication'])
async def signup(signup_data: UserSignUpModel):
    try:
        signup_response = await signupOnFirebase(signup_data)
        if "successfully signed up" in signup_response[1]:
            user_id = signup_response[0]
            response = await add_user_data(user_id, signup_data)
            return response
        else:
            raise HTTPException(status_code=400, detail=signup_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login", tags=['Authentication'])
async def sign_in(user_info: UserLoginModel):
    try:
        response = await loginOnFirebase(user_info.email, user_info.password)
        if "error" in response:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response['error'])
        return JSONResponse(content=response)  # Directly return the response from Firebase
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/refresh_token", tags=['Authentication'])
async def refresh_token(refresh_token: str):
    try:
        refreshed_token = refresh_id_token(refresh_token)
        return refreshed_token
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")




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


# @app.put("/users/{user_id}", tags=['Users'])
# async def update_user(user_data: UserUpdateModel):
#     return await update_user_data(user_data)


@app.put("/users/recipes_allergies/{user_id}", tags=['Users'])
async def update_user_recipes_allergies(user_data: UserUpdateRecipeAllergiesModel, id_token: str):
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


@app.put("/users/add_favorite/{id_token}", tags=["Users"])
async def add_favorite(id_token: str, recipe_id: str):
    user_verify = await verify_id_token(id_token)
    uid = user_verify['user_id']
    try:
        user_collection.document(uid).update({'recipes': firestore.ArrayUnion([recipe_id])})
        user_data = await get_document(user_collection.document(uid))
        return user_data["recipes"]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@app.put("/users/update_all", tags=['Users'])
async def update_all_user_data(user_data: allUserDataModel, id_token: str = Query(...)):
    await verify_id_token(id_token)
    return await update_all_u_d(user_data)


@app.put("/users/profile_image/", tags=["Users"])
async def user_profile_image(file: UploadFile = File(...), id_token: str = Query(...)):
    user_verify = await verify_id_token(id_token)
    uid = user_verify['user_id']
    # name = uid + str(int(time.time() * 1000))
    profile_image_url = await image_to_storage(file, uid)
    user_collection.document(uid).update({"profileImageURL": profile_image_url})
    return await get_document(user_collection.document(user_id.strip()), details=True)
    return profile_image_url




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


@app.post("/recipes/add_recipe", tags=['Recipes'])
async def user_added_recipe(recipe: RecipeModel, id_token: str = Query(...)):
<<<<<<< HEAD
<<<<<<< HEAD
    user_verify = await verify_id_token(id_token)
    recipe_id = await new_recipe(recipe, user_verify['uid'], user_verify['name'], user_added = True)
=======
=======
>>>>>>> a9d9892 (Add creation time to new recipes, enhance user profile image handling, and streamline token verification)
    await verify_id_token(id_token)
    recipe_id = await new_recipe(recipe, user_added = True)
>>>>>>> fd1430c (Add creation time to new recipes, enhance user profile image handling, and streamline token verification)
    await update_user_r_a(recipe.author, [recipe_id], None)
    return recipe_id



@app.get("/GPT_ingredients_to_recipe/", tags=['GPT'])
async def ingredients_to_GPT(background_tasks: BackgroundTasks, ingredients: str,  id_token: str = Query(...), allergies: str = Query(...)):
    user_verify = await verify_id_token(id_token)
    try:
        check_ingredients = await search_recipe_by(ingredients, "searchable_ingredient")
        if check_ingredients != []:
            return check_ingredients
        
        response_list = await GPT_to_recipe(ingredients, allergies)
        response = await new_recipe(response_list[1], user_verify['uid'], user_verify['name'], user_added = False)

        # if user_id:
        #     await update_user_r_a(user_id, [response["recipe_id"]], None)
        background_tasks.add_task(GPT_image, response_list[0], response['recipe_id'])

        return [response]

        # response_list_task = asyncio.create_task(GPT_to_recipe(ingredients))
        # img_url_task = asyncio.create_task(GPT_image(ingredients, img_name))
        # r_list, GPT_img_url = await asyncio.gather(response_list_task, img_url_task)
            
        # response = await new_recipe(r_list[1], GPT_img_url, user_added = False)
        # response["img_url"] = GPT_img_url
        # return [response]
    
    except Exception as e:
        print(f"Error in ingredients_to_GPT: {str(e)}")
        raise HTTPException(status_code=500, detail=f"{str(e)}")




@app.post("/upload-image/file", tags=['Images'])
async def upload_image(file: UploadFile = File(...), id_token: str = Query(...), save_path: str = Query(...)):
    user_verify = await verify_id_token(id_token)

    try:
        profile_image_url = await image_to_storage(file, save_path)
        return profile_image_url
    except Exception as e:
        print(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"{str(e)}")




@app.get("/get_image_url/{file_name}", tags=['Experimental'])
async def get_image(file_name: str):
    img_url = await get_image_from_firebase(file_name)
    return img_url


<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> a9d9892 (Add creation time to new recipes, enhance user profile image handling, and streamline token verification)
@app.put("/upload-image/file", tags=['Experimental'])
async def upload_image(file: UploadFile = File(...), id_token: str = Query(...)):
    user_verify = await verify_id_token(id_token)
    uid = user_verify['user_id']
    # name = uid + str(int(time.time() * 1000))
    profile_image_url = await image_to_storage(file, uid)
    print(profile_image_url)
    return profile_image_url

>>>>>>> fd1430c (Add creation time to new recipes, enhance user profile image handling, and streamline token verification)

@app.post("/upload-image/{url}", tags=['Experimental'])
async def upload_image_by_url(url: str):
    return await image_url_to_storage(url)


@app.get("/generate-image", tags=['Experimental'])
async def generate_image(item: str):
    start_time = time.time()
    a = await GPT_image(item, item)
    end_time = time.time()
    print(end_time - start_time)
    return a

    # image_data = requests.get(image_url).content
    # img_byte_arr = io.BytesIO(image_data)
    # StreamingResponse(img_byte_arr, media_type="image/png")@app.post("/upload-image/{url}", tags=['Experimental'])

