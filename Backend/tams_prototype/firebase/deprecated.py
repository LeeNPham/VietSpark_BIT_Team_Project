
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



@app.get("/ingredients_to_recipes", tags=['Ingredients'])
async def ingredients_to_recipes(ingredients: str):
    return await search_by_ingredients(ingredients)


    

@app.get("/recipes", tags=['Recipes'])
async def get_all_recipes():
    collection = await get_collection(recipe_collection.stream(), details=True)
    for recipe in collection:
        recipe.pop("instructions", None)
        recipe.pop("searchable_ingredient", None)
        recipe.pop("searchable_recipe_name", None)
        recipe["ingredients"] = len(recipe['ingredients'])
    # p_c = json.dumps(collection, indent=4)
    return collection


@app.get("/recipes/name/{recipe_name}", tags=['Recipes'])
async def get_recipe_by_name(recipe_name: str):
    return await check_recipe(recipe_name.strip())


@app.get("/recipes/id/{recipe_id}", tags=['Recipes'])
async def get_recipe_by_id(recipe_id: str):
    recipe = await get_document(recipe_collection.document(recipe_id.strip()), details=True)
    recipe.pop("searchable_ingredient", None)
    recipe.pop("searchable_recipe_name", None)
    return recipe

    
async def check_recipe(recipe_name):
    recipe_name = recipe_name.split()
    print(recipe_name)
    try:
        collection = recipe_collection.where("name", "in", [recipe_name]).stream()
        # collection = ingredient_collection.where("searchable_recipe_name", "array_contains_any", recipe_name).stream()
        for doc in collection:
            return doc.to_dict()
        return "Recipe not in database"

    except Exception as e:
        return f"An unexpected error occurred: {e}"


        
async def search_by_ingredients(ingredients):
    ingredients = ingredients.split()
    recipe_list = []
    for ingredient in ingredients:
        collection = recipe_collection.where("searchable_ingredient", "array_contains", ingredient).stream()
        recipe_id = await get_collection(collection, details=False)
        if recipe_id == "No collection":
            recipe_id = "no match"
            return recipe_id
        if not recipe_list:
            recipe_list.extend(recipe_id)
        else:
            recipe_list = list(set(recipe_list) & set(recipe_id))
            if not recipe_list:
                return "no match"
    
    match_recipe = []
    for recipe_id in recipe_list:
        recipe = await get_document(recipe_collection.document(str(recipe_id)), details=True)
        match_recipe.append(recipe)
    return match_recipe


@app.post("/recipes", tags=['Recipes'])
async def user_added_recipe(recipe: RecipeModel):
    check = await search_recipe_by(recipe.name, "searchable_recipe_name")
    if check == "no match":
        return await new_recipe(recipe, None)
    return check


    response_list_task = asyncio.create_task(GPT_to_recipe(ingredients))
    img_url_task = asyncio.create_task(GPT_image(ingredients, img_name))
    r_list, GPT_img_url = await asyncio.gather(response_list_task, img_url_task)
        
    response = await new_recipe(r_list[1], GPT_img_url, user_added = False)
    response["img_url"] = GPT_img_url

    

    # uid = user_verify['user_id']
    # name = uid + str(int(time.time() * 1000))

    # url = blob.generate_signed_url(version='v4', expiration=3600, method='GET')
    # Make the file publicly accessible (optional)



@app.put("/users/profile_image/", tags=["Users"])
async def user_profile_image(file: UploadFile = File(...), id_token: str = Query(...)):
    user_verify = await verify_id_token(id_token)
    uid = user_verify['user_id']
    # name = uid + str(int(time.time() * 1000))
    profile_image_url = await image_to_storage(file, uid)
    user_collection.document(uid).update({"profileImageURL": profile_image_url})
    return await get_document(user_collection.document(user_id.strip()), details=True)
    return profile_image_url



        response_list_task = asyncio.create_task(GPT_to_recipe(ingredients))
        img_url_task = asyncio.create_task(GPT_image(ingredients, img_name))
        r_list, GPT_img_url = await asyncio.gather(response_list_task, img_url_task)
            
        response = await new_recipe(r_list[1], GPT_img_url, user_added = False)
        response["img_url"] = GPT_img_url
        return [response]
    























































































"""