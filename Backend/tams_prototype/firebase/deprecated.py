
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
    


async def check_ingredient_index(ingredientName, recipe_id):
    ingredient_index = await get_collection(ingredient_collection.stream(), details=False)
    if ingredientName in ingredient_index:
        ingredient_collection.document(ingredientName).update({'recipe_id': firestore.ArrayUnion([recipe_id])})
        return f"new recipe added to {ingredientName}"
    else:
        ingredient_data = {'recipe_id': [recipe_id]}
        ingredient_collection.document(ingredientName).set(ingredient_data)
        return f"new ingredient '{ingredientName}' added to index"


@app.post("/add_ingredients", tags=['Ingredients'])
async def add_ingredients(ingredient: AddIngredientModel):
    return await check_ingredient_index(ingredient)


try:
    user_auth = {
        "uid": user_id,
        "userEmail": signup_data.email,
        "userName": signup_data.username,
        "phoneNumber": signup_data.phone_number or "",
        "disabled": False
    }
    user_auth_collection.document(user_id).set(user_auth)
    response = {"auth_reponse": f"User auth {user_id} added to Firestore!"}
except Exception as e:
    response = {"auth_reponse": f"Error adding user to Firestore: {str(e)}"}














































































































"""