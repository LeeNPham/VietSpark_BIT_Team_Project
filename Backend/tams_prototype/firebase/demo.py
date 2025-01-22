import os
import firebase_admin.auth
import pyrebase
import firebase_admin
from fastapi import FastAPI, HTTPException, status
from google.cloud import firestore
from dotenv import load_dotenv
from firebase_admin import credentials, auth
from pydantic import BaseModel
from typing import Optional
from models import *
from additionalFucntions import *
import json
import base64

load_dotenv()
# Load Firebase configuration
apiKey = os.getenv("APIKEY")
authDomain = os.getenv("AUTHDOMAIN")
databaseURL = os.getenv("DATABASEURL")
projectId = os.getenv("PROJECTID")
storageBucket = os.getenv("STORAGEBUCKET")
messagingSenderId = os.getenv("MESSAGINGSENDERID")
appId = os.getenv("APPID")
measurementId = os.getenv("MEASUREMENTID")
encoded_service_account = os.getenv("SERVICE_ACCOUNT_KEY")
import tempfile

serviceAccountKey = json.loads(
    base64.b64decode(encoded_service_account).decode("utf-8")
)
with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
    json.dump(serviceAccountKey, temp_file)
    temp_file.flush()  # Ensure all data is written
    service_account_path = temp_file.name  # Path to the temporary file
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)
db = firestore.Client.from_service_account_json(service_account_path)
os.remove(service_account_path)
# do not touch 24-37


firebaseConfig = {
    "apiKey": apiKey,
    "authDomain": authDomain,
    "databaseURL": databaseURL,
    "projectId": projectId,
    "storageBucket": storageBucket,
    "messagingSenderId": messagingSenderId,
    "appId": appId,
    "measurementId": measurementId,
}



# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
mainAuth = firebase.auth()

ingredient_collection = db.collection("ingredient")
user_auth_collection = db.collection("user_auth")
user_data_collection = db.collection("user_data")
recipe_collection = db.collection("recipe")

print("Firebase initialized successfully!")


# Signup function
async def signupOnFirebase(email, password, username):
    try:
        # user = mainAuth.create_user_with_email_and_password(email, password)
        user = auth.create_user(
            email=email,
            password=password,
            display_name=username,
            photo_url=None,
            disabled=False,
        )
        l = []
        l.append(user.uid)
        l.append(f"You successfully signed up: {user.email}")
        # return f"You successfully signed up: {user}"
        return l
    except Exception as e:
        return f"Failed Signup: {str(e)}"


async def add_user_auth_data(userID, userEmail, username, phoneNumber):
    try:
        user_auth = {
            "uid": userID,
            "userEmail": userEmail,
            "userName": username,
            "phoneNumber": phoneNumber or "",
            "disabled": False
        }
        user_auth_collection.document(userID).set(user_auth)
        response = {"auth_reponse": f"User auth {userID} added to Firestore!"}
    except Exception as e:
        response = {"auth_reponse": f"Error adding user to Firestore: {str(e)}"}
    try:
        user_data = {
            "userEmail": userEmail,
            "userName": username,
            "phoneNumber": phoneNumber or "",
            "profileImageURL": "",
            "description": "",
            "recipes": [],
            "allergies": []
        }
        user_data_collection.document(userID).set(user_data)
        response.update({"data_response": f"User data {userEmail} added to Firestore!"}) 
    except Exception as e:
        response.update({"data_response": f"Error adding user to Firestore: {str(e)}"})
    
    return response


# Login function
async def loginOnFirebase(email, password):
    try:
        login = mainAuth.sign_in_with_email_and_password(email, password)
        return login
    except Exception as e:
        error_message = str(e)
        return {"error": "UNKNOWN_ERROR", "message": error_message}


async def get_document(document, details):
    try:
        item = document.get()
        print(1)
        if item.exists:
            if details == False:
                return item.id
            else:
                return item.to_dict()
        else:
            return f"item not found"
    except Exception as e:
        return f"Error retrieving user from Firestore: {str(e)}"


async def delete_user_from_firestore(user_id):
    try:
        user_data_collection.document(user_id).delete()
        user_auth_collection.document(user_id).delete()
        auth.delete_user(user_id)
        return f"deleted user: {user_id}"
    except Exception as e:
        return f"Error retrieving user from Firestore: {str(e)}"


async def update_user_data(user_id, user_email, username, phone_number, profile_image_url, description):
    try:
        user = user_data_collection.document(user_id).get()
        user = user.to_dict()
        if not user:
            return f"{user_id} not found"
        user_data = {
            "userId": user_id,
            "userEmail": user_email,
            "userName": username,
            "phoneNumber": phone_number,
            "profileImageURL": profile_image_url,
            "description": description
        }
        for key, value in user_data.items():
            if value is None:
                user_data[key] = user.get(key, value)

        user_data_collection.document(user_id).update(user_data)
        return user_data
    except Exception as e:
        return f"Error retrieving user from Firestore: {str(e)}"


async def update_user_r_a(user_id, recipes, allergies):
    try:
        if recipes:
            print("add recipes")
            user_data_collection.document(user_id).update({'recipes': firestore.ArrayUnion(recipes)})
        if allergies:
            print("add allergies")
            user_data_collection.document(user_id).update({'allergies': firestore.ArrayUnion(allergies)})
        return {"message": "User data updated successfully."}
    
    except auth.AuthError as e:
        print(f"Authentication error: {str(e)}")
        raise HTTPException(status_code=404, detail="User not found.")
    except firestore.FirebaseError as e:
        print(f"Firestore error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating user data in Firestore.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


async def new_recipe(recipe, recipe_id):
    for ingredient in recipe.ingredients:
        await check_ingredient_index(ingredient.name, recipe_id)
    ingredient_data = [ingredient.dict() for ingredient in recipe.ingredients]
    recipe_data = {
        "id": recipe_id,
        "name": recipe.name,
        "ingredients": ingredient_data,
        "instructions": recipe.instructions,
        "time": recipe.time,
        "img_url": recipe.img_url,
        "servings": recipe.servings,
    }
    recipe_collection.document(str(recipe_id)).set(recipe_data)
    return {"message": "Recipe added successfully"}


async def check_ingredient_index(ingredient, recipe_id):
    ingredient_index = await get_collection(ingredient_collection.stream(), details=False)
    if ingredient in ingredient_index:
        ingredient_collection.document(ingredient).update({'recipe_id': firestore.ArrayUnion([recipe_id])})
        return f"new recipe added to {ingredient}"
    else:
        ingredient_data = {'recipe_id': [recipe_id]}
        ingredient_collection.document(ingredient).set(ingredient_data)
        return f"new ingredient '{ingredient}' added to index"


async def get_collection(collection, details):
    try:
        collection_list = []
        if details == False:
            for item in collection:
                collection_list.append(item.id)
        else:
            for item in collection:
                collection_list.append({item.id: item.to_dict()})
        if collection_list:
            return collection_list
        else:
            return "No collection"
    except Exception as e:
        return f"Error retrieving {collection} from Firestore: {str(e)}"


async def check_recipe(recipe_name):
    collection = recipe_collection.where("name", "in", [recipe_name]).stream()
    for doc in collection:
        print(f"{doc.id} => {doc.to_dict()}")


async def i_to_r(ingredients):
    if len(ingredients) == 1:
        document = await get_document(ingredient_collection.document(ingredients[0]), details=True)
        id_list = document['recipe_id']
    else:
        id_list = []
        for ingredient in ingredients:
            document = await get_document(ingredient_collection.document(ingredient), details=True)
            if document == "item not found":
                return "no match"
            if not id_list:
                id_list.extend(document["recipe_id"])
            else:
                id_list = list(set(id_list) & set(document["recipe_id"]))
                if not id_list:
                    return "no match"

    recipe_list = []
    for recipe_id in id_list:
        recipe = await get_document(recipe_collection.document(str(recipe_id)), details=True)
        recipe_list.append(recipe)
    return recipe_list

    
