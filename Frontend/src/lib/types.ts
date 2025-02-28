export interface RecipeDTO {
    recipe_id: string,
    name: string,
    img_url: string,
    time: number,
    calories: number,
    servings: number,
    numIngredients: number,
    
};

export interface RecipeDetailDTO {
    id: string,
    name: string,
    img_url: string,
    time: number,
    calories: number,
    servings: number,
    ingredients: { ingredientAmount: string, ingredientName: string }[];
    instructions: string[],
    author_id: string,
    author_name: string,
}
export interface RecipeAddDTO {
    name: string,
    img_url: string,
    time: number,
    calories: number,
    ingredients: { ingredientAmount: string, ingredientName: string }[];
    instructions: string[],
    author: string,
    servings: number,
};


// User
export interface UserDTO {
    user_id: string, 
    userEmail: string,
    userName: string,
    phoneNumber: string,
    profileImageURL: string,
    description: string;
    recipes: string[],
    allergies: string[],
}

export interface UserLoginDTO {
    email: string,
    password: string,
}

export interface UserSignUpDTO {
    email: string, 
    userName: string,
    password: string,
    phoneNumber: string,
}

