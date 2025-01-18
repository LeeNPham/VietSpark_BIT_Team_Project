
"""


@app.post("/login", tags=['Authentication'])
async def sign_in(user_info: UserInfo):
   return await loginOnFirebase(user_info[email], user_info[password])
async def sign_in(email: str, password: str):
   return await loginOnFirebase(email, password)


async def all_recipes():
    try:
        recipes = recipe_collection.stream()
        #return str(recipes.id)
        recipes_list = []
        for recipe in recipes:
            recipes_list.append(recipe.id)

    except Exception as e:
        return f"Error retrieving recipes from Firestore: {str(e)}"
    
    finally:
        if recipes_list:
            return recipes_list
        else:
            return "No Recipes"
    

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


@app.get("/user/{user_id}", tags=['Users'])
async def get_user(user_id: str):
    return await get_document(user_collection.document(user_id), details=True)


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





"""