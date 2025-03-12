import type { idText } from "typescript";

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

export interface ReviewAddDTO {
    recipe_id: string,
    rating: number,
    description: string,
    content: string,
    images: string[],
    video: string | null,
}

export interface ReviewDTO {
    review_id: string,
    rating: number,
    description: string,
    content: string,
    images: string[],
    video: string | null,
    userName: string,
    userImage: string,
    user_id: string,
    recipe_id: string,
    created_at: string,
}