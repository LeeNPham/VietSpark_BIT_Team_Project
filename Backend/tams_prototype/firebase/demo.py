import os
import firebase_admin.auth
import pyrebase
import firebase_admin
from openai import OpenAI
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
user_collection = db.collection("user")
recipe_collection = db.collection("recipe")

print("Firebase initialized successfully!")


# Signup function
async def signupOnFirebase(signup_data):
    if signup_data.phone_number == "string":
        signup_data.phone_number = None
    try:
        # user = mainAuth.create_user_with_email_and_password(email, password)
        user = auth.create_user(
            email=signup_data.email,
            password=signup_data.password,
            display_name=signup_data.username,
            phone_number=signup_data.phone_number,
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


async def add_user_data(user_id, signup_data):
    try:
        user_data = {
            "userEmail": signup_data.email,
            "userName": signup_data.username,
            "phoneNumber": signup_data.phone_number or "",
            "profileImageURL": "",
            "description": "",
            "recipes": [],
            "allergies": []
        }
        user_collection.document(user_id).set(user_data)
        response = {"data_response": f"User {signup_data.email} added to Firestore!"} 
    except Exception as e:
        response = {"data_response": f"Error adding user to Firestore: {str(e)}"}
    
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
        user_collection.document(user_id).delete()
        auth.delete_user(user_id)
        return f"deleted user: {user_id}"
    except Exception as e:
        return f"Error retrieving user from Firestore: {str(e)}"


async def update_user_data(user_data):
    try:
        user = user_collection.document(user_data.user_id).get()
        user = user.to_dict()
        if not user:
            return f"{user_data.user_id} not found"
        update_data = {
            "userEmail": user_data.email,
            "userName": user_data.username,
            "phoneNumber": user_data.phone_number,
            "profileImageURL": user_data.profile_image_url,
            "description": user_data.description
        }
        for key, value in update_data.items():
            if value is None:
                user_data[key] = user.get(key, value)
        
        user_collection.document(user_data.user_id).update(update_data)
        return user
    except Exception as e:
        return f"Error retrieving user from Firestore: {str(e)}"


async def update_user_r_a(user_id, recipes, allergies):
    try:
        if recipes:
            print(1)
            user_collection.document(user_id).update({'recipes': firestore.ArrayUnion(recipes)})
        if allergies:
            print(2)
            user_collection.document(user_id).update({'allergies': firestore.ArrayUnion(allergies)})
        return {"message": "User data updated successfully."}
    
    # except auth.AuthError as e:
    #     print(f"Authentication error: {str(e)}")
    #     raise HTTPException(status_code=404, detail="User not found.")
    # except firestore.FirebaseError as e:
    #     print(f"Firestore error: {str(e)}")
    #     raise HTTPException(status_code=500, detail="Error updating user data in Firestore.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


async def new_recipe(recipe):
    ingredient_data = []
    searchable_ingredient = [] 
    for ingredient in recipe.ingredients:
        ingredient_data.append(ingredient.dict())
        searchable_ingredient = list(set(searchable_ingredient + ingredient.ingredientName.split())) 
    lower_searchable_ingredient = [item.lower() for item in searchable_ingredient]
    lower_searchable_name = [item.lower() for item in recipe.name.split()]
    recipe_data = {
        "name": recipe.name,
        "ingredients": ingredient_data,
        "instructions": recipe.instructions,
        "time": recipe.time,
        "img_url": recipe.img_url,
        "servings": recipe.servings,
        "calories": recipe.calories,
        "searchable_recipe_name": lower_searchable_name,
        "searchable_ingredient": lower_searchable_ingredient,
    }
    if recipe.author != 'string':
        recipe_data['user_id'] = recipe.author
        recipe_data["searchable_recipe_name"].append(recipe.author)
    recipe_collection.document().set(recipe_data)
    return {"message": f"Recipe: {recipe.name} added successfully"}


async def get_collection(collection, details):
    try:
        collection_list = []
        if details == False:
            for item in collection:
                collection_list.append(item.id)
        else:
            for item in collection:
                collection_list.append(item.to_dict())
        if collection_list:
            return collection_list
        else:
            return "No collection"
    except Exception as e:
        return f"Error retrieving {collection} from Firestore: {str(e)}"


async def check_recipe(recipe_name):
    # recipe_name = recipe_name.split()
    # print(recipe_name)
    try:
        collection = recipe_collection.where("name", "in", [recipe_name]).stream()
        # collection = ingredient_collection.where("searchable_recipe_name", "array_contains_any", recipe_name).stream()
        for doc in collection:
            return doc.to_dict()
        return "Recipe not in database"

    except Exception as e:
        return f"An unexpected error occurred: {e}"
    

async def i_to_r(ingredients):
    ingredients = ingredients.split()
    # if len(ingredients) == 1:
    #     search = str(ingredients[0])
    #     collection = recipe_collection.where("searchable_ingredient", "array_contains", search).stream()
    #     return await get_collection(collection, details=True)

    # else:
    recipe_list = []
    for ingredient in ingredients:
        collection = recipe_collection.where("searchable_ingredient", "array_contains", ingredient).stream()
        recipe_id = await get_collection(collection, details=False)
        if recipe_id == "No collection":
            return recipe_id
        if not recipe_list:
            recipe_list.extend(recipe_id)
        else:
            recipe_list = list(set(recipe_list) & set(recipe_id))
            if not recipe_list:
                return "no match"
        print(recipe_list)
    match_recipe = []
    for recipe_id in recipe_list:
        recipe = await get_document(recipe_collection.document(str(recipe_id)), details=True)
        match_recipe.append(recipe)
    return match_recipe

    


async def GPT_response_to_ingredientS(ingredient):
    OAI_api_key = os.getenv("OAI_API_KEY")

    client = OpenAI(
        api_key=OAI_api_key
    )
    prompt = f"""
    You are a Vietnamese recipe expert. You are only allowed to respond in the form of a JSON. Time should be in minutes. The JSON should always take the following shape:
    {{
        "name": " ",
        "ingredients": [{{"ingredientName": "ingredientName", "ingredientAmount": "ingredient amount with unit"}}],
        "calories": int,
        "time": " ",
        "servings": int,
        "instructions": ["step 1", "step 2"]
    }}
    I will provide you a list of ingredients, and you will always respond with your best recommendation for a Vietnamese recipe. Here are the ingredients I have:
    {{ingredients}}

    Respond only with the JSON format as described above.
    """

    # Initialize a message history list with the system prompt
    # This structure is required for the OpenAI chat model to maintain context.
    messages = [{"role": "system", "content": prompt}]

    # Define a function to handle user input and generate a response using OpenAI's API
    messages.append({"role": "user", "content": ingredient})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,  # Specify the model to use
        messages = messages       # Pass the conversation history
    )
    ChatGPT_reply = response.choices[0].message.content
    recipe_json = json.loads(ChatGPT_reply)
    recipe_json["author"] = "string"
    print(recipe_json["author"])
    recipe_name = recipe_json['name']
    recipe = RecipeModel.model_validate(recipe_json)
    # recipe["user_id"] = "string"
    # print(recipe.user_id)
    # Add the assistant's reply to the message history to maintain context
    messages.append({"role": "assistant", "content": response})
    response_list = [recipe_name, recipe]

    return response_list




