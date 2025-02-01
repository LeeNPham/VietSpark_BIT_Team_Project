import { writable } from "svelte/store";
import type { RecipeAddDTO } from "../types";
const API_URL = import.meta.env.VITE_API_URL;


export const recipeStore = writable({
    isLoading: true,
    recipes: [],
    currentRecipe: null
});


export const recipeHandler = {
    addRecipe: async (recipeData: RecipeAddDTO) => {
        try {
            const res = await fetch(`${API_URL}/add_new_recipe`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(recipeData),
            });

            if (!res.ok) throw new Error("Failed to add recipe");

            const newRecipe = await res.json();
            return newRecipe.id;
        } catch (error) {
            console.error("Error creating new recipe", error);
            throw error
        }
    },
    getRecipe: async (recipeId: string) => {
        try {
            const res = await fetch(`${API_URL}/get_recipe_by_id/${recipeId}`);
            if (!res.ok) throw new Error(`Failed to fetch recipe ${recipeId}`);
            const recipe = await res.json();
            recipeStore.update((state) => ({
                ...state,
                isLoading: false,
                currentRecipe: recipe
            }));

        } catch (error) {
            console.error("Error finding recipe", recipeId);
            throw error;
        }
    },
    getRecipes: async () => {
        try {
            const res = await fetch(`${API_URL}/get_all_recipes`);
            if (!res.ok) throw new Error('Failed to fetch recipes');
            const recipes = await res.json();
            recipeStore.set({ isLoading: false, recipes, currentRecipe: null });
        } catch (e) {
            console.error((e as Error).message);
            throw e;
        }
    },
    updateRecipe: () => {},
    deleteRecipe: () => {},

}