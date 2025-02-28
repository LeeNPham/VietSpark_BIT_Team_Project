import os
import firebase_admin.auth
import pyrebase
import firebase_admin
import json
import base64
import requests
import io
import time
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
# do not touch 34-48


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




async def get_document(document, details = Optional):
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
        return str(e)


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
    if signup_data.phoneNumber == "string":
        signup_data.phoneNumber = None
    try:
        # user = mainAuth.create_user_with_email_and_password(email, password)
        user = auth.create_user(
            email=signup_data.email,
            password=signup_data.password,
            display_name=signup_data.userName,
            phone_number=signup_data.phoneNumber,
            photo_url=None,
            disabled=False,
        )
        l = []
        l.append(user.uid)
        l.append(f"You successfully signed up: {user.email}")
        return l
    except Exception as e:
        return str(e)


async def add_user_data(user_id, signup_data):
    try:
        user_data = {
            "userEmail": signup_data.email,
            "userName": signup_data.userName,
            "phoneNumber": signup_data.phoneNumber or "",
            "profileImageURL": "https://storage.googleapis.com/chat-app-react-and-firebase.appspot.com/profileImages/default_avatar.jpg",
            "description": "",
            "recipes": [],
            "allergies": []
        }
        user_collection.document(user_id).set(user_data)
        return {"data_response": f"User {signup_data.email} added to Firestore!"} 
    except Exception as e:
        return str(e)


# Login function
async def loginOnFirebase(email, password):
    try:
        login = mainAuth.sign_in_with_email_and_password(email, password)
        # user_data = await user_collection.document(login["localId"])
        uid = str(login['localId'])
        user_data = await get_document(user_collection.document(uid), details=True)
        login.update(user_data)
        return login
    except Exception as e:
        e = json.loads(e.args[1])['error']['message']
        return {"error": e}


async def verify_id_token(id_token):
    try:
        data = auth.verify_id_token(id_token)
        return data
    except (auth.ExpiredIdTokenError, auth.RevokedIdTokenError, auth.InvalidIdTokenError) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def refresh_id_token(refresh_token):
    url = f"https://securetoken.googleapis.com/v1/token?key={apiKey}" 
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


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
            "userName": user_data.userName,
            "phoneNumber": user_data.phoneNumber,
            "profileImageURL": user_data.profileImageURL,
            "description": user_data.description
        }
        for key, value in update_data.items():
            if value is None:
                user_data[key] = user.get(key, value)
        
        user_collection.document(user_data.user_id).update(update_data)
        return user
    except Exception as e:
        return f"Error retrieving user from Firestore: {str(e)}"


async def update_user_r_a(user_id, recipes: Optional[List[str]] = None, allergies: Optional[List[str]] = None):
    try:
        if recipes:
            user_collection.document(user_id).update({'recipes': firestore.ArrayUnion(recipes)})
        if allergies:
            user_collection.document(user_id).update({'allergies': firestore.ArrayUnion(allergies)})
        return {"message": "User data updated successfully."}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


async def update_all_u_d(user_data):
    try:
        # Update auth provider only if fields are provided
        auth_kwargs = {}
        if user_data.userEmail is not None:
            auth_kwargs["email"] = user_data.userEmail
        if user_data.userName is not None:
            auth_kwargs["display_name"] = user_data.userName
        if auth_kwargs:
            auth.update_user(user_data.user_id, **auth_kwargs)

        # Update Firestore only with provided fields
        update_data = {}
        if user_data.userEmail is not None:
            update_data["userEmail"] = user_data.userEmail
        if user_data.userName is not None:
            update_data["userName"] = user_data.userName
        if user_data.phoneNumber is not None:
            update_data["phoneNumber"] = user_data.phoneNumber
        if user_data.profileImageURL is not None:
            update_data["profileImageURL"] = user_data.profileImageURL
        if user_data.description is not None:
            update_data["description"] = user_data.description
        if user_data.recipes is not None:
            update_data["recipes"] = user_data.recipes
        if user_data.allergies is not None:
            update_data["allergies"] = user_data.allergies

        print("Firestore update data:", update_data)

        user_ref = user_collection.document(user_data.user_id)
        if update_data:
            user_ref.update(update_data)

        # Fetch and return the full updated document
        updated_doc = user_ref.get()
        if not updated_doc.exists:
            raise HTTPException(status_code=404, detail="User not found in Firestore")
        
        updated_data = updated_doc.to_dict()
        updated_data["user_id"] = user_data.user_id
        return updated_data

    except auth.AuthError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))




async def new_recipe(recipe, uid, author, user_added):
    ingredient_data = []
    searchable_ingredient = [] 
    for ingredient in recipe.ingredients:
        ingredient_data.append(ingredient.dict())
        searchable_ingredient = list(set(searchable_ingredient + ingredient.ingredientName.split())) 
    
    lower_searchable_ingredient = [item.lower() for item in searchable_ingredient]
    lower_searchable_ingredient = clean_words(remove_accents(lower_searchable_ingredient))
    lower_searchable_name = [item.lower() for item in recipe.name.split()]
    lower_searchable_name = clean_words(remove_accents(lower_searchable_name))
    
    if user_added == False:
        # img_prompt = " ".join(lower_searchable_name)
        # GPT_img_url = await GPT_image(img_prompt, recipe.name)
        # img_url = (GPT_img_url[GPT_img_url.find('http'):])
        img_url = "https://s3.gifyu.com/images/b2PWA.gif"
    else:
        img_url = ""
    creation_time = int(time.time() * 1000)

    recipe_data = {
        "name": recipe.name,
        "ingredients": ingredient_data,
        "instructions": recipe.instructions,
        "time": recipe.time,
        "img_url": img_url,
        "servings": recipe.servings,
        "calories": recipe.calories,
        "searchable_recipe_name": lower_searchable_name,
        "searchable_ingredient": lower_searchable_ingredient,
        "creation_time": creation_time,
    }
    if user_added == True:
        recipe_data['author_id'] = uid
        recipe_data['author_name'] = author
    else:
        recipe_data['author_id'] = "VSChef"
        recipe_data['author_name'] = "VS Chef"
        # recipe_data["searchable_recipe_name"].append(recipe.author)

    recipe_doc = recipe_collection.document()
    recipe_doc.set(recipe_data)
    recipe_doc.update({"recipe_id": recipe_doc.id})

    if user_added == False:
        recipe_data["recipe_id"] = recipe_doc.id
        return recipe_data
    return recipe_doc.id


async def recipe_database_search(name, author, calories, time):
    if name:
        return await search_recipe_by(name, "searchable_recipe_name")
    elif author:
        collection = recipe_collection.where("author", "==", author).stream()
    elif calories:
        collection = recipe_collection.where("calories", "==", calories).stream()
    elif time:
        collection = recipe_collection.where("time", "==", time).stream()
    else:
        latest_sort = recipe_collection.order_by('creation_time', direction=firestore.Query.DESCENDING).stream()
        collection =  await get_collection(latest_sort, details=True)
        for recipe in collection:
            recipe = format_recipe(recipe, "short")
        return collection

    collection = await get_collection(collection, details=True)
    for recipe in collection:
        recipe = format_recipe(recipe, "short")
    return collection


async def search_recipe_by_id(id: str):
    if id.strip():
        recipe = await get_document(recipe_collection.document(id.strip()), details=True)
        # recipe = format_recipe(recipe)
        return recipe
    else:
        raise HTTPException(status_code=422, detail="Recipe ID is required!")


async def search_recipe_by(data, search_type):
    data = data.lower().split()
    clean_data = clean_words(remove_accents(data))
    recipe_list = []
    for word in clean_data:
        collection = recipe_collection.where(f"{search_type}", "array_contains", word).stream()
        recipe_id = await get_collection(collection, details=False)
        if recipe_id == "No collection":
            return []
        if not recipe_list:
            recipe_list.extend(recipe_id)
        else:
            recipe_list = list(set(recipe_list) & set(recipe_id))
            if not recipe_list:
                return []
    match_recipe = []
    for recipe_id in recipe_list:
        recipe = await get_document(recipe_collection.document(str(recipe_id)), details=True)
        recipe.pop("searchable_ingredient", None)
        recipe.pop("searchable_recipe_name", None)
        match_recipe.append(recipe)
    return match_recipe
    

async def GPT_to_recipe(ingredients, allergies):
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
    {{Ingredients}}
    I will also provide you a list of allergies, and you will not including them in the recipe. It is very critical to not include any of them.
    {{Allergies}}

    Respond only with the JSON format as described above.
    """

    messages = [{"role": "system", "content": prompt}]
    # Define a function to handle user input and generate a response using OpenAI's API
    messages.append({"role": "user", "content": f"Ingredients: {ingredients}\n Allgeries: {allergies}"})
    # response = client.chat.completions.create(
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
    # messages.append({"role": "assistant", "content": response})
    response_list = [recipe_name, recipe]
    return response_list


async def GPT_image(item, recipe_id):
    print("GPT imaging...")
    OAI_api_key = os.getenv("OAI_API_KEY")
    client = OpenAI(api_key=OAI_api_key)

    prompt = f"""Generate a image of a presented dish of food: {{item}}"""
    messages = [{"role": "system", "content": prompt}]
    messages.append({"role": "user", "content": item})
    response = client.images.generate(
        prompt=item,
        n=1,
        # size="256x256"
        size="512x512"
        # size="1024x1024"
    )

    image_url = response.data[0].url
    image_data = requests.get(image_url).content
    img_byte_arr = io.BytesIO(image_data)

    return await image_url_to_storage(image_url, recipe_id)
    # return StreamingResponse(img_byte_arr, media_type="image/png")




async def image_url_to_storage(url, recipe_id):
    recipe_name = recipe_id +'_1'
    # name = (url[url.rfind('/') + 1:]) # select name after the last '/'
    response = requests.get(url)
    if response.status_code == 200:
        image_data = img_compression(response.content)
        bucket = storage.bucket()
        blob = bucket.blob(f"images/{recipe_name}")
        blob.upload_from_file(image_data, content_type='image/jpeg')
        blob.make_public()
        image_url = blob.public_url
        recipe_collection.document(recipe_id).update({"img_url": image_url})
        return image_url

    return f"Failed to fetch image from URL: {response.status_code}"


async def image_to_storage(file, path):
    image_data = await file.read()
    image_data = img_compression(image_data)
    try:
        bucket = storage.bucket()
        blob = bucket.blob(f"{path}")
        blob.upload_from_file(image_data, content_type='image/jpeg')
        blob.make_public()
        image_url = blob.public_url
        print(image_url)
        return image_url

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


async def get_image_from_firebase(file_name):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(file_name)
        img_url = blob.public_url
        return img_url
        
    except Exception as e:
        print(f"Error downloading file: {e}")














































