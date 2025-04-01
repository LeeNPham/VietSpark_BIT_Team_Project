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
import requests

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




# --- STYLING ---
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")




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

@app.delete("/users/favorite/{id_token}", tags=["Users"])
async def remove_favorite(id_token: str, recipe_id: str = Query(...)):
    user_verify = await verify_id_token(id_token)
    uid = user_verify['user_id']
    try:
        user_collection.document(uid).update({'recipes': firestore.ArrayRemove([recipe_id])})
        user_data = await get_document(user_collection.document(uid))
        return user_data["recipes"]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.put("/users/update_all", tags=['Users'])
async def update_all_user_data(user_data: allUserDataModel, id_token: str = Query(...)):
    await verify_id_token(id_token)
    return await update_all_u_d(user_data)


import math

#GET cannot pass a body, only parameters
@app.get("/recipes", tags=['Recipes'], response_model=None)
async def get_recipes(
    name: Optional[str] = None, 
    author: Optional[str] = None, 
    calories: Optional[int] = None, 
    time: Optional[int] = None,
    limit: Optional[int] = Query(10, ge=1),
    offset: Optional[int] = Query(0, ge=0),
    ):
    recipes, total_recipes = await recipe_database_search(name, author, calories, time, limit, offset)
    if limit is not None and offset is not None:
        if len(recipes) > limit * offset:
            recipes = recipes[offset * limit:offset * limit + limit]
        else:
            recipes = []
        page = (offset // limit) + 1 if total_recipes > 0 else 1
        page_size = min(limit, len(recipes))
        total_pages = math.ceil(total_recipes / limit) if limit > 0 else 1
        
        return {
            "recipes": recipes,
            "pagination": {
                "page": page,
                "pageSize": page_size,,
                "total": total_recipes,
                "totalPages": total_pages
            }
        }
    else:
        return {
            "recipes": recipes,
            "pagination": {
                "page": 1,
                "pageSize": len(recipes),
                "total": len(recipes),
                "totalPages": 1
            }
        }


@app.get("/recipes/{recipe_id}", tags=["Recipes"])
async def get_recipe_by_id(recipe_id: str):
    return await search_recipe_by_id(recipe_id)

@app.get("/recipes_batch", tags=["Recipes"])
async def get_recipes_batch(recipeIds: str):
    recipeIds = recipeIds.split(',')
    return await search_recipe_by_id_batch(recipeIds)


@app.post("/recipes/add_recipe", tags=['Recipes'])
async def user_added_recipe(recipe: RecipeModel, id_token: str = Query(...)):
    user_verify = await verify_id_token(id_token)
    recipe_id = await new_recipe(recipe, user_verify['uid'], user_verify['name'], user_added = True)
    await update_user_r_a(recipe.author, [recipe_id], None)
    return recipe_id

from typing import Dict, Any

@app.get("/search_recipe_database", tags=['Recipes'])
async def search_by_ingredients(
    ingredients: str = Query(...),
    limit: Optional[int] = Query(10, ge=1), 
    offset: Optional[int] = Query(0, ge=0)
) -> Dict[str, Any]:
    """
    Search recipes by ingredients with pagination.
    Returns {"recipes": [...], "pagination": {...}} format.
    """
    try:
        # Fetch all matching recipes
        check_ingredients = await search_recipe_by(ingredients, "searchable_ingredient")
        
        # Handle empty or invalid results
        if not check_ingredients or check_ingredients == 'item not found':
            return {
                "recipes": [],
                "pagination": {
                    "page": 1,
                    "pageSize": 0,
                    "total": 0,
                    "totalPages": 0
                }
            }
        
        # Calculate total number of recipes
        total_recipes = len(check_ingredients)
        
        # Check if offset exceeds total results
        if offset >= total_recipes:
            return {
                "recipes": [],
                "pagination": {
                    "page": (offset // limit) + 1,
                    "pageSize": 0,
                    "total": total_recipes,
                    "totalPages": math.ceil(total_recipes / limit)
                }
            }
        
        # Apply pagination
        recipes = check_ingredients[offset:offset + limit]
        
        # Return paginated results with metadata
        return {
            "recipes": recipes,
            "pagination": {
                "page": (offset // limit) + 1,
                "pageSize": len(recipes),
                "total": total_recipes,
                "totalPages": math.ceil(total_recipes / limit)
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching recipes: {str(e)}")


@app.get("/GPT_ingredients_to_recipe/", tags=['GPT'])
async def ingredients_to_GPT(background_tasks: BackgroundTasks, ingredients: str,  id_token: str = Query(...), allergies: str = Query(...)):
    user_verify = await verify_id_token(id_token)
    try:
        response_list = await GPT_to_recipe(ingredients, allergies)
        response = await new_recipe(response_list[1], user_verify['uid'], user_verify['name'], user_added = False)
        background_tasks.add_task(GPT_image, response_list[0], response['recipe_id'])
        return [response]
    except Exception as e:
        print(f"Error in ingredients_to_GPT: {str(e)}")
        raise HTTPException(status_code=500, detail=f"{str(e)}")




@app.post("/upload-image/file", tags=['Media'])
async def upload_image(file: UploadFile = File(...), id_token: str = Query(...), save_path: str = Query(...)):
    user_verify = await verify_id_token(id_token)
    try:
        profile_image_url = await image_to_storage(file, save_path)
        return profile_image_url
    except Exception as e:
        print(f"Error uploading image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"{str(e)}")

@app.post("/upload-video/file", tags=['Media'])
async def upload_video(file: UploadFile = File(...), id_token: str = Query(...), save_path: str = Query(...)):
    user_verify = await verify_id_token(id_token)
    try:
        video_url = await video_to_storage(file, save_path)
        return video_url
    except Exception as e:
        print(f"Error uploading media: {str(e)}")
        raise HTTPException(status_code=500, detail=f"{str(e)}")

@app.delete("/media", tags=['Media'])
async def delete_media(url: str, id_token: str = Query(...)):
    user_verify = await verify_id_token(id_token)
    try:
        await delete_media_from_firebase(url)
        return {"message": "Media deleted successfully"}
    except Exception as e:
        print(f"Error deleting media: {str(e)}")
        raise HTTPException(status_code=500, detail=f"{str(e)}")

@app.get("/get_image_url/{file_name}", tags=['Experimental'])
async def get_image(file_name: str):
    img_url = await get_image_from_firebase(file_name)
    return img_url


@app.put("/upload-image/file", tags=['Experimental'])
async def upload_image(file: UploadFile = File(...), id_token: str = Query(...)):
    user_verify = await verify_id_token(id_token)
    uid = user_verify['user_id']
    # name = uid + str(int(time.time() * 1000))
    profile_image_url = await image_to_storage(file, uid)
    return profile_image_url


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

@app.get('/index', tags=['Experimental'])
async def index_of():
    return await return_index()


@app.get("/Nutritions", tags=["Recipes"])
async def get_nutritions(ingredients: str):
    return await request_nutritions(ingredients)


# Authorization with Firebase Authentication
from fastapi import FastAPI, HTTPException, Depends
from firebase_admin import firestore, auth
from typing import List
async def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.split("Bearer ")[1]
        decoded_token = auth.verify_id_token(token)
        return decoded_token['uid']
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Review
@app.get("/reviews/{recipe_id}", tags=['Reviews'])
async def get_reviews(
    recipe_id: str,
    review_id: Optional[str] = Query(None, description="Filter by review ID"),
    rating: Optional[int] = Query(None, description="Filter by rating 1 - 5", ge=1, le=5), 
    has_image: Optional[bool] = Query(None, description="Filter by has image or not"),
    ):
    reviews = []
    try:
        reviews = await search_reviews(recipe_id, review_id, rating, has_image)
        return reviews
    except Exception as e:
        print(f"Error in get_reviews: {str(e)}")
        raise HTTPException(status_code=500, detail=f"{str(e)}")

    
@app.post("/reviews", tags=['Reviews'])
async def add_review(review: ReviewAdd, id_token: str = Query(...)):
    user_data = await verify_id_token(id_token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    review_id = await create_review(review, user_data['user_id'], user_data['name'])
    return review_id

 
# for route in app.routes:
#     print(f"Path: {route.path}")