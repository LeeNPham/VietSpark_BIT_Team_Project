export interface Recipe {
    id: string,
    name: string,
    img_url: string,
    time: string,
    calories: string,
    ingredients: { quantity: string, name: string }[];
    instructions: string[],
    createdBy: string,
}

export interface User {
    uid: string, 
    userEmail: string,
    userName: string,
    phoneNumber: string,
    profileImageURL: string,
    description: string;
    recipes: string[],
    allergies: string[],
}