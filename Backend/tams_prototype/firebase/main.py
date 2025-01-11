from fastapi import Depends, Query, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from demo import *
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
import json


class publicProfile(BaseModel):
    user_id: Optional[str] = None,
    user_email: Optional[str] = None,
    user_name: Optional[str] = None,  # Adjust if you collect the user's name
    recipes: Optional[str] = None,  # Initialize empty lists
    allergies: Optional[str] = None

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

# @app.get("/")
# async def get_root():
#     return {"hello": "world"}

@app.post("/authentication", tags=['Authentication'])
async def signup(email: str, username: str, password: str):
    """
    Sign up a user and add them to the Firestore collection.
    """
    # Sign up user in Firebase Authentication
    try:
        signup_response = await signupOnFirebase(email, password)
        user_id = signup_response[0]
        if "successfully signed up" in signup_response[1]:
            # Extract user ID (you may need to adjust this based on actual response format)
            #for n in range(9999):

            #user_id = username  # Assuming email is the unique user ID
            # Add user to Firestore
            firestore_response = await add_user_to_firestore(
                user_id=user_id,
                user_email=email,
                username=username,  # Adjust if you collect the user's name
                recipes=[],  # Initialize empty lists
                allergies=[],
                test=["hello","world"]
            )
            return {"message": signup_response, "firestore": firestore_response}
        else:
            raise HTTPException(status_code=400, detail=signup_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class UserInfo(BaseModel):
    email: str
    password: str

#@app.post("/login", tags=['Authentication'])
#async def sign_in(user_info: UserInfo):
#    return await loginOnFirebase(user_info[email], user_info[password])
#async def sign_in(email: str, password: str):
#    return await loginOnFirebase(email, password)


class UserInfo(BaseModel):
    email: str
    password: str

@app.post("/login", tags=['Authentication'])
async def sign_in(user_info: UserInfo):
    print(user_info)
    user_info = user_info.model_dump()  # Convert the Pydantic model to a dictionary
    print(user_info)
    try:
        # Call the login function and check for successful login
        response = await loginOnFirebase(user_info["email"], user_info["password"])
        
        if 'error' in response:
            # Firebase login failed, raise an HTTPException with the proper error message
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response['error'])
        
        # If login is successful, return the response
        return JSONResponse(content=response)  # Directly return the response from Firebase
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")


@app.get("/user/{user_id}", tags=['Users'])
async def get_user(user_id: str):
    return await get_user_from_firestore(user_id)

@app.get("/user", tags=['Users'])
async def get_all_users():
    return await get_all_users_from_firestore()

@app.delete("/user/{user_id}", tags=['Users'])
async def delete_user(user_email: str):
    return await delete_user_from_firestore(user_email)

@app.put("/user/{user_id}", tags=['Users'])
async def update_user(user_id: str, user_email: Optional[str] = None, user_name: Optional[str] = None, recipes: Optional[str] = None, allergies: Optional[str] = None):
    return await update_user_from_firestore(user_id, user_email, user_name, recipes, allergies)



# I want you to connect to a collection, and add to it, the name of the collection is going to be users
# it will store data
# 
#  such as userEmail, userName, userId, recipes, allergies, 






















