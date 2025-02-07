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
    img.save(byte_io, format="JPEG", quality=65)
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
    for key in data.items():
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

























































