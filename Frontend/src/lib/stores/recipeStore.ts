import { writable } from "svelte/store";
import type { RecipeAddDTO } from "../types";

const API_URL = import.meta.env.VITE_API_URL;


export const recipeStore = writable({
    isLoading: true,
    recipes: [],
    currentRecipe: null,
    currentIndex: -1,
});


export const recipeHandler = {
    addRecipe: async (recipeData: RecipeAddDTO) => {
        try {
            console.log("Adding new recipe");
            const res = await fetch(`${API_URL}/recipes`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(recipeData),
            });

            if (!res.ok) throw new Error("Failed to add recipe");

            const newRecipe = await res.json();
            recipeStore.update((state) => ({
                ...state,
                currentRecipe: newRecipe,
                currentIndex: -1
            }))
            return newRecipe.id;
        } catch (error) {
            console.error("Error creating new recipe", error);
            throw error
        }
    },
    getRecipe: async (recipeId: string) => {
        try {

            const url = `${API_URL}/recipes/${recipeId}`;
            const res = await fetch(url);
            if (!res.ok) throw new Error(`Failed to fetch recipe ${recipeId}`);
            const foundRecipe = await res.json();
            recipeStore.update((state) => ({
                ...state,
                isLoading: false,
                currentRecipe: foundRecipe,
                currentIndex: -1
            }));
            return foundRecipe;
        } catch (error) {
            console.error("Error finding recipe", recipeId);
            throw error;
        }
    },
    getRecipes: async (recipeName: string | null) => {
        try {
            const queryParams = new URLSearchParams();
            if (recipeName?.trim()) queryParams.append("name", recipeName.trim());
            const paramStr = queryParams.toString() ? '?' + queryParams.toString() : '';

            const res = await fetch(`${API_URL}/recipes${paramStr}`);

            if (!res.ok) throw new Error('Failed to fetch recipes');
            const recipes = await res.json();
            console.log("Fetched recipes", recipes);
            recipeStore.set({ isLoading: false, recipes, currentRecipe: null, currentIndex: -1 });
        } catch (e) {
            console.error((e as Error).message);
            throw e;
        }
    },
    updateRecipe: () => { },
    deleteRecipe: () => { },

    searchRecipesGPT: async (ingredients: string, user_id: string | null) => {
        if (!ingredients.trim()) throw new Error("There is no ingredients");

        try {
            const queryParams = new URLSearchParams();
            if (ingredients) queryParams.append("ingredients", ingredients);
            if (user_id) queryParams.append("user_id", user_id);
            const paramStr = queryParams.toString ? '?' + queryParams.toString() : '';
            const res = await fetch(`${API_URL}/GPT_ingredients_to_recipe${paramStr}`);

            if (!res.ok) throw new Error("Failed to search for recipes with ingredients " + ingredients);

            const recipes = await res.json();
            if (recipes) {
                recipeStore.update((state) => ({
                    ...state,
                    recipes,
                    isLoading: false,
                    currentRecipe: recipes[0].id,
                    currentIndex: 0
                }))
            } else throw new Error(`No recipes with ingredients ${ingredients} found`)
            
        } catch (e) {
            console.error((e as Error));
            throw e;
        }
    }
}