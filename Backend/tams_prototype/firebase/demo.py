
import os
import firebase_admin.auth
import pyrebase
import firebase_admin
from google.cloud import firestore
from dotenv import load_dotenv
from firebase_admin import credentials, auth
from pydantic import BaseModel
from typing import Optional

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
serviceAccountKey = os.getenv("SERVICE_ACCOUNT_KEY")  # Path to service account JSON file

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

class publicProfile(BaseModel):
    user_id: Optional[str] = None,
    user_email: Optional[str] = None,
    user_name: Optional[str] = None,  # Adjust if you collect the user's name
    recipes: Optional[str] = None,  # Initialize empty lists
    allergies: Optional[str] = None


cred = credentials.Certificate(serviceAccountKey)
firebase_admin.initialize_app(cred)

# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
mainAuth = firebase.auth()

# Initialize Firestore with the service account
db = firestore.Client.from_service_account_json(serviceAccountKey)
user_collection = db.collection("users")

print("Firebase initialized successfully!")

# Login function
async def loginOnFirebase(email, password):
    print("Log in...")
    try:
        login = mainAuth.sign_in_with_email_and_password(email, password)
        print("login")
        return login
        #if login:
            #return "Successfully logged in!"
    except Exception as e:
        return f"Invalid email or password: {str(e)}"
    return


# Signup function
async def signupOnFirebase(email, password):
    try:
        #user = mainAuth.create_user_with_email_and_password(email, password)
        user = auth.create_user(
            email = email,
            password = password,
            display_name = None,
            photo_url = None,
            disabled = False
        )
        l = []
        l.append(user.uid)
        l.append(f"You successfully signed up: {user.email}")
        #return f"You successfully signed up: {user}"
        return l
    except Exception as e: 
        return f"Failed Signup: {str(e)}"

'''
# Add user to Firestore
async def add_user_to_firestore(user_id, user_data):
    try:
        user_collection.document(user_id).set(user_data)
        return f"User {user_id} added to Firestore!"
    except Exception as e:
        return f"Error adding user to Firestore: {str(e)}"
'''


async def add_user_to_firestore(user_id, user_email, username, recipes=None, allergies=None):
    """
    Adds a user to the Firestore 'users' collection.
    
    Parameters:
        user_id (str): Unique identifier for the user.
        user_email (str): User's email address.
        user_name (str): User's name.
        recipes (list, optional): List of recipes.
        allergies (list, optional): List of allergies.
    
    Returns:
        str: Confirmation message or error message.
    """
    try:
        user_data = {
            "userId": user_id,
            "userEmail": user_email,
            "userName": username,
            "recipes": recipes or [],
            "allergies": allergies or []
        }
        user_collection.document(user_id).set(user_data)
        return f"User {user_id} added to Firestore!"
    except Exception as e:
        return f"Error adding user to Firestore: {str(e)}"    
    

# Get user from Firestore
async def get_user_from_firestore(user_id):
    try:
        #user_ref = user_collection.document(user_id)
        #user = user_ref.get()
        user = user_collection.document(user_id).get()
        if user.exists:
            return user.to_dict()
        else:
            return "User not found"
    except Exception as e:
        return f"Error retrieving user from Firestore: {str(e)}"
    

async def get_all_users_from_firestore():
    try:
        users = user_collection.stream()
        users_list = []
        for user in users:
            users_list.append({user.id: user.to_dict()})
        
        if users_list:
            return users_list
        else:
            return "No users in Firestore"
    except Exception as e:
        return f"Error retrieving users from Firestore: {str(e)}"
    

async def get_user_from_firestore2(user_id):
    user = user_collection.document(user_id).get()
    return user.to_dict()


async def delete_user_from_firestore(user_email):
    authUser = auth.get_user_by_email(user_email)
    #userEmail = user.to_dict().get('userEmail')
    try:
        if authUser:
            user_id = authUser.uid
            user_collection.document(user_id).delete()
            auth.delete_user(user_id)
            return f'deleted user: {user_email}'
        else:
            return "User not found"
    except Exception as e:
        return f"Error retrieving user from Firestore: {str(e)}"
    

async def update_user_from_firestore(user_id, user_email, user_name, recipes, allergies):
    try:
        user = user_collection.document(user_id).get()
        user = user.to_dict()
        if not user:
            return f'{user_id} not found'
        user_data = {
            "userId": user_id,
            "userEmail": user_email,
            "userName": user_name,
            "recipes": recipes,
            "allergies": allergies
        }
        for key, value in user_data.items():
            if value is None:
                user_data[key] = user.get(key, value)

        user_collection.document(user_id).update(user_data)
        return user_data
    except Exception as e:
        return f"Error retrieving user from Firestore: {str(e)}"


# Example usage
if __name__ == "__main__":
    import asyncio

    email = "test@example.com"
    password = "testpassword"

    # Sign up
    print(asyncio.run(signupOnFirebase(email, password)))

    # Log in
    print(asyncio.run(loginOnFirebase(email, password)))

    # Add user to Firestore
    user_data = {"name": "John Doe", "age": 30}
    print(asyncio.run(add_user_to_firestore("user123", user_data)))

    # Get user from Firestore
    print(asyncio.run(get_user_from_firestore("user123")))
