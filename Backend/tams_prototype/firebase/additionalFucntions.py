from unidecode import unidecode
from PIL import Image
from io import BytesIO




def check_missing_index(t):
    if t == "No collection":
        return 1
    else:
        t = sorted(t, key=int)
        last_id = int(t[-1])
        if last_id > len(t):
            while str(last_id - 1) in t:
                last_id -= 1
            return last_id - 1
        else:
            return last_id + 1


def img_compression(img):
    img = Image.open(BytesIO(img))
    img = img.convert("RGB")
    byte_io = BytesIO()
    img.save(byte_io, format="JPEG", quality=75)
    byte_io.seek(0)
    return byte_io


def clean_words(input):
    char = '1234567890qwertyuiopasdfghjklzxcvbnm'
    if type(input) == str:
        if input[0] not in char:
            input = input[1:]
        if input[-1] not in char:
            input = input[:-1]
        return input
    
    elif type(input) == list:
        new_list = []
        for i in input:
            if i[0] not in char:
                i = i[1:]
            if i[-1] not in char:
                i = i[:-1]
            new_list.append(i)
        return new_list


def remove_accents(input):
    if type(input) == str:
        return unidecode(input)
    
    elif type(input) == list:
        new_list = []
        for i in input:
            new_list.append(unidecode(i))
        return new_list


def data_fill(data):
    new_data = {}
    for key, value in data.model_fields.item():
        if data[key] == "string":
            new_data[key] = ""
        elif data[key] == int:
            new_data[key] = 0
    return new_data


def format_recipe(recipe, length = None):
    recipe.pop("searchable_ingredient", None)
    recipe.pop("searchable_recipe_name", None)
    if length == "short":
        recipe.pop("instructions", None)
        recipe["numIngredients"] = len(recipe['ingredients'])
        recipe.pop("ingredients", None)
    return recipe


def combined_nutrition(nutritions, recipe_name):
    recipe_name = remove_accents(recipe_name)
    combined = {
        "calories": 0,
        "serving_size_g": 0,
        "fat_total_g": 0,
        "fat_saturated_g": 0,
        "protein_g": 0,
        "sodium_mg": 0,
        "potassium_mg": 0,
        "cholesterol_mg": 0,
        "carbohydrates_total_g": 0,
        "fiber_g": 0,
        "sugar_g": 0
    }

# for item in nutritions["items"]:
#     combined["calories"] += item["calories"]
#     combined["serving_size_g"] += item["serving_size_g"]
#     combined["fat_total_g"] += item["fat_total_g"]
#     combined["fat_saturated_g"] += item["fat_saturated_g"]
#     combined["protein_g"] += item["protein_g"]
#     combined["sodium_mg"] += item["sodium_mg"]
#     combined["potassium_mg"] += item["potassium_mg"]
#     combined["cholesterol_mg"] += item["cholesterol_mg"]
#     combined["carbohydrates_total_g"] += item["carbohydrates_total_g"]
#     combined["fiber_g"] += item["fiber_g"]
#     combined["sugar_g"] += item["sugar_g"]

    for item in nutritions["items"]:
        for key in combined:
            if key != "name":
                combined[key] += item.get(key, 0)

    formated_nutritions = {}
    for key in combined:
        if key != "calories":
            string = str(key)
            idx = string.rfind("_")
            unit = string[idx + 1:]
            new_key = string[:idx]
            formated_nutritions[new_key] = f"{round(combined[key], 2)} {unit}"
        else:
            formated_nutritions[key] = f"{round(combined[key], 2)}"
    return formated_nutritions





















































