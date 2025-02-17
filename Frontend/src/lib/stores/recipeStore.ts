import { writable } from "svelte/store";
import { getLSUserData } from "$lib/stores/userStore";
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
            recipeStore.update((state) => ({
                ...state,
                isLoading: false,
            }))
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
            recipeStore.update((state) => ({
                ...state,
                isLoading: false,
                recipes
            }));
        } catch (e) {
            recipeStore.update((state) => ({
                ...state,
                isLoading: false,
                recipes: []
            }))
            throw e;
        }
    },
    updateRecipe: () => { },
    deleteRecipe: () => { },

    searchRecipesGPT: async (ingredients: string) => {
        const userLS = getLSUserData();
        console.log(userLS)
        if (!userLS.idToken) {throw new Error("User is not signed in");}

        if (!ingredients.trim()) throw new Error("There is no ingredients");

        try {
            const queryParams = new URLSearchParams();
            if (ingredients) queryParams.append("ingredients", ingredients);
            else return recipeHandler.getRecipes(null);

            const paramStr = queryParams.toString ? '?' + queryParams.toString() : '';
            const res = await fetch(`${API_URL}/GPT_ingredients_to_recipe${paramStr}&id_token=${userLS.idToken}&allergies=${userLS.allergies}`);

            if (!res.ok) throw new Error("Failed to search for recipes with ingredients " + ingredients);

            const recipes = await res.json();
            console.log("Found recipes from GPT", recipes)
            if (recipes.length > 0) {
                recipeStore.update((state) => ({
                    ...state,
                    recipes,
                    isLoading: false,
                    currentRecipe: recipes[0].recipe_id,
                    currentIndex: 0
                }))
            } else throw new Error(`No recipes with ingredients ${ingredients} found`)
            
        } catch (e) {
            recipeStore.update((state) => ({
                ...state,
                isLoading: false,
                recipes: []
            }))
            throw e;
        }
    },

    favoriteRecipe: async (recipeId: string) => {
        const userLS = getLSUserData()
        if (!userLS.idToken) {throw new Error("User is not signed in");}

        try {
            const url = `${API_URL}/users/add_favorite/${userLS.idToken}?recipe_id=${recipeId}`

            const res = await fetch(url,{
                method: 'PUT',
                headers:{
                    'Content-Type': 'application/json'
                }
            });

            if (!res.ok) throw new Error('Failed to add favorite recipe')

            const userRecipes = await res.json()
            return userRecipes
        } catch (error) {
            console.error("Error adding favorite recipe", error);
            throw error
        }
    },
}