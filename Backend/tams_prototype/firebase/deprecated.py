
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


@app.get("/user/{user_email}", tags=['Users'])
async def get_user(user_email: str):
    try:
        user_id = auth.get_user_by_email(user_email).uid
        return await get_document(user_data_collection.document(user_id), details=True)
    except Exception as e:
        return f"Error retrieving user: {str(e)}"


async def delete_user_from_firestore(user_email):
    authUser = auth.get_user_by_email(user_email)
    # userEmail = user.to_dict().get('userEmail')
    try:
        if authUser:
            user_id = authUser.uid
            user_data_collection.document(user_id).delete()
            user_auth_collection.document(user_id).delete()
            auth.delete_user(user_id)
            return f"deleted user: {user_email}"
        else:
            return "User not found"
    except Exception as e:
        return f"Error retrieving user from Firestore: {str(e)}"


async def update_user_data(user_email, new_email, username, phone_number, profile_image_url, description):
    try:
        authUser = auth.get_user_by_email(user_email)
        user_id = authUser.uid
        user = user_data_collection.document(user_id).get()
        user = user.to_dict()
        if not user:
            return f"{user_id} not found"
        user_data = {
            "userId": user_id,
            "userEmail": new_email,
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





"""