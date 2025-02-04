import os
import firebase_admin.auth
import pyrebase
import firebase_admin
import json
import base64
import io
import requests
from io import BytesIO
from openai import OpenAI
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from google.cloud import firestore
from dotenv import load_dotenv
from firebase_admin import credentials, auth, storage
from pydantic import BaseModel
from typing import Optional
from models import *
from additionalFucntions import *

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
# firebase_admin.initialize_app(cred)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'chat-app-react-and-firebase.appspot.com'  # Replace with your actual Firebase Storage bucket name
})
db = firestore.Client.from_service_account_json(service_account_path)
os.remove(service_account_path)
# do not touch 31-45


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
            user_collection.document(user_id).update({'recipes': firestore.ArrayUnion(recipes)})
        if allergies:
            user_collection.document(user_id).update({'allergies': firestore.ArrayUnion(allergies)})
        return {"message": "User data updated successfully."}
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


async def search_recipe_by_id(id: str):
    if id.strip():
        recipe = await get_document(recipe_collection.document(id.strip()), details=True)
        recipe.pop("searchable_ingredient", None)
        recipe.pop("searchable_recipe_name", None)
        return recipe
    else:
        raise HTTPException(status_code=422, detail="Recipe ID is required!")


async def recipe_database_search(name: Optional[str] = None):
    if name and name.strip():
        return await search_recipe_by(name.strip(), "searchable_recipe_name")
    else:
        collection = await get_collection(recipe_collection.stream(), details=True)
        for recipe in collection:
            recipe.pop("instructions", None)
            recipe.pop("searchable_ingredient", None)
            recipe.pop("searchable_recipe_name", None)
            recipe["numIngredients"] = len(recipe['ingredients'])
        # p_c = json.dumps(collection, indent=4)
        return collection


async def new_recipe(recipe, user_added):
    ingredient_data = []
    searchable_ingredient = [] 
    for ingredient in recipe.ingredients:
        ingredient_data.append(ingredient.dict())
        searchable_ingredient = list(set(searchable_ingredient + ingredient.ingredientName.split())) 
    
    lower_searchable_ingredient = [item.lower() for item in searchable_ingredient]
    lower_searchable_ingredient = clean_words(remove_accents(lower_searchable_ingredient))
    lower_searchable_name = [item.lower() for item in recipe.name.split()]
    lower_searchable_name = clean_words(remove_accents(lower_searchable_name))
    
    # if user_added == False:
    #     img_prompt = ", ".join(lower_searchable_name)
    #     GPT_img_url = await GPT_image(img_prompt, recipe.name)
    #     GPT_img_url = (GPT_img_url[GPT_img_url.find('http'):])
    #     url_list = [GPT_img_url, ""]
    # else:
    #     # img_url = await image_to_storage(user_added)
    #     # url_list = [img_url, '']
    #     url_list = ""

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

    recipe_doc = recipe_collection.document()
    recipe_doc.set(recipe_data)
    recipe_doc.update({"recipe_id": recipe_doc.id})
    return {"message": f"Recipe: {recipe.name} - ID: {recipe_doc.id} added successfully"}


async def search_recipe_by(data, search_type):
    data = data.lower().split()
    clean_data = clean_words(remove_accents(data))
    recipe_list = []
    for word in clean_data:
        collection = recipe_collection.where(f"{search_type}", "array_contains", word).stream()
        recipe_id = await get_collection(collection, details=False)

        if recipe_id == "No collection":
            return []  # Exit early if no match is found

        if recipe_list is None:
            recipe_list.extend(recipe_id)  # First valid set of IDs
        else:
            recipe_list = list(set(recipe_list) & set(recipe_id))  # Intersection to keep common IDs

        if not recipe_list:  # If no common IDs remain, exit early
            return []

    return list(recipe_list) if recipe_list else []
    
    # match_recipe = []
    # for recipe_id in recipe_list:
    #     recipe = await get_document(recipe_collection.document(str(recipe_id)), details=True)
    #     recipe.pop("searchable_ingredient", None)
    #     recipe.pop("searchable_recipe_name", None)
    #     match_recipe.append(recipe)
    # return match_recipe



async def GPT_to_recipe(ingredient):
    print("GPT working...")
    OAI_api_key = os.getenv("OAI_API_KEY")
    client = OpenAI(api_key=OAI_api_key)
    if not OAI_api_key:
        raise ValueError("API Key is missing!")

    prompt = f"""
    You are a Vietnamese recipe expert. You are only allowed to respond in the form of a JSON. Time should be in minutes. The JSON should always take the following shape:
    {{
        "name": " ",
        "ingredients": [{{"ingredientName": "ingredientName", "ingredientAmount": "ingredient amount with unit"}}],
        "calories": int,
        "time": int, # minutes
        "servings": int,
        "instructions": ["step 1", "step 2"]
    }}
    I will provide you a list of ingredients, and you will always respond with your best recommendation for a Vietnamese recipe. Here are the ingredients I have:
    {{ingredients}}

    Respond only with the JSON format as described above.
    """

    messages = [{"role": "system", "content": prompt}]
    # Define a function to handle user input and generate a response using OpenAI's API
    messages.append({"role": "user", "content": ingredient})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,  # Specify the model to use
        messages = messages       # Pass the conversation history
    )

    if not response.choices or not response.choices[0].message.content:
        raise ValueError("Received empty or invalid response from OpenAI.")
    
    ChatGPT_reply = response.choices[0].message.content
    ChatGPT_reply = ChatGPT_reply.replace('```', '')
    ChatGPT_reply = ChatGPT_reply.replace('json', '')
    try:
        recipe_json = json.loads(ChatGPT_reply)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON from the response: {e}")
    
    recipe_json["author"] = "string"
    recipe_name = recipe_json['name']
    recipe = RecipeModel.model_validate(recipe_json)
    messages.append({"role": "assistant", "content": response})
    response_list = [recipe_name, recipe]

    return response_list


async def GPT_image(item, recipe_name):
    OAI_api_key = os.getenv("OAI_API_KEY")
    client = OpenAI(api_key=OAI_api_key)

    prompt = f"""Generate a image of a presented dish of food: {{item}}"""
    messages = [{"role": "system", "content": prompt}]
    messages.append({"role": "user", "content": item})
    response = client.images.generate(
        prompt=item,
        n=1,
        # size="256x256"
        # size="512x512"
        size="1024x1024"
    )

    image_url = response.data[0].url
    image_data = requests.get(image_url).content
    img_byte_arr = io.BytesIO(image_data)

    return await image_url_to_storage(image_url, recipe_name)
    # return StreamingResponse(img_byte_arr, media_type="image/png")




async def image_url_to_storage(url, recipe_name):
    recipe_name = remove_accents(recipe_name)
    recipe_name = recipe_name +'_1'
    # name = (url[url.rfind('/') + 1:]) # select name after the last '/'
    response = requests.get(url)
    if response.status_code == 200:
        image_data = img_compression(response.content)
        bucket = storage.bucket()
        blob = bucket.blob(f"images/{recipe_name}")
        blob.upload_from_file(image_data, content_type='image/jpeg')
        blob.make_public()
        image_url = blob.public_url
        return image_url

    return f"Failed to fetch image from URL: {response.status_code}"
    

async def image_to_storage(file):
    # temp_file_path = f"temp_{file.filename}"
    # with open(temp_file_path, "wb") as temp_file:
    #     temp_file.write(await file.read())
    image_data = await file.read()
    image_data = img_compression(image_data)
    try:
        bucket = storage.bucket()
        # Upload the image to Firebase Storage
        blob = bucket.blob(f"images/{file.filename}")
        blob.upload_from_file(image_data, content_type='image/jpeg')
        # Make the file publicly accessible (optional)
        blob.make_public()
        # Get the public URL of the uploaded image
        image_url = blob.public_url
        # Clean up the temporary file
        # os.remove(temp_file_path)

        return image_url

    # except Exception as e:
    #     os.remove(temp_file_path)
    #     return JSONResponse(content={"error": str(e)}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


async def get_image_from_firebase(file_name):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(file_name)
        img_url = blob.public_url
        return(img_url)
        
    except Exception as e:
        print(f"Error downloading file: {e}")











