export interface Recipe {
    id: string,
    name: string,
    img_url: string,
    time: string,
    calories: string,
    ingredients: { quantity: string, name: string }[];
    instructions: string[],
}