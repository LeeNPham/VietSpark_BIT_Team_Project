import { writable } from "svelte/store";
import { getLSUserData } from "$lib/stores/userStore";
import type { RecipeAddDTO } from "../types";

const API_URL = import.meta.env.VITE_API_URL;


export const recipeStore = writable({
    isLoading: true,
    recipes: [],
    page: 1,
    totalPages: 1,
    total: 0,
    currentRecipe: null,
});


export const recipeHandler = {
    addRecipe: async (recipeData: RecipeAddDTO) => {
        const idToken = localStorage.getItem("idToken")
        try {
            const res = await fetch(`${API_URL}/recipes/add_recipe?id_token=${idToken}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(recipeData),
            });

            const newRecipe = await res.json();
            if (!res.ok) throw new Error(newRecipe.detail || "Failed to create new recipe");

            recipeStore.update((state) => ({
                ...state,
                currentRecipe: newRecipe,
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
            const foundRecipe = await res.json();
            
            if (!res.ok) throw new Error(foundRecipe.detail || "Failed to fetch recipe");
            
            if (!foundRecipe || Array.isArray(foundRecipe) && foundRecipe.length === 0 || foundRecipe === "item not found") {
                throw new Error(`Recipe is not found`);
            }
            recipeStore.update((state) => ({
                ...state,
                isLoading: false,
                currentRecipe: foundRecipe,
            }));
            return foundRecipe;
        } catch (error) {
            recipeStore.update((state) => ({
                ...state,
                isLoading: false,
                currentRecipe: null,
            }))
            throw error;
        }
    },
    getRecipes: async (recipeName: string | null, limit: number = 10, offset: number = 0) => {
        try {
            const queryParams = new URLSearchParams();
            if (recipeName?.trim()) queryParams.append("name", recipeName.trim());
            queryParams.append("offset", offset.toString());
            queryParams.append("limit", limit.toString());

            const paramStr = queryParams.toString() ? '?' + queryParams.toString() : '';

            const res = await fetch(`${API_URL}/recipes${paramStr}`);
            const resData = await res.json();

            if (!res.ok) throw new Error(resData.detail || 'Failed to fetch recipes');
            recipeStore.update((state) => ({
                ...state,
                isLoading: false,
                recipes: resData.recipes,
                page: resData.pagination.page,
                totalPages: resData.pagination.totalPages,
                total: resData.pagination.total,
            }));
        } catch (e) {
            recipeStore.update((state) => ({
                ...state,
                isLoading: false,
                recipes: [],
                page: 1,
                totalPages: 1,
                total: 0,
            }))
            throw e;
        }
    },

    getRecipeList: async (recipeIds: string[]) => {
        const queryParams = new URLSearchParams();
        queryParams.append("recipeIds", recipeIds.join(','));
        const paramStr = queryParams.toString() ? '?' + queryParams.toString() : '';

        try {
            const res = await fetch(`${API_URL}/recipes_batch${paramStr}`);
            const recipes = await res.json();
            if (!res.ok) throw new Error(recipes.detail || 'Failed to fetch recipes');
            return recipes;
        } catch (e) {
            throw e;
        }

    },
    updateRecipe: () => { },
    deleteRecipe: () => { },

    searchRecipesGPT: async (ingredients: string) => {
        

        if (!ingredients.trim()) throw new Error("There is no ingredients");

        try {
            // Step 1: Search with ingredients only
            const queryParams = new URLSearchParams();
            if (ingredients) queryParams.append("ingredients", ingredients);
            else return recipeHandler.getRecipes(null, 10, 0);

            const paramStr = queryParams.toString ? '?' + queryParams.toString() : '';

            const resIngredients = await fetch(`${API_URL}/search_recipe_database${paramStr}`);
            const resData = await resIngredients.json();
            if (resIngredients.ok && resData !== "item not found") {
                recipeStore.update((state) => ({
                    ...state,
                    recipes: resData.recipes,
                    isLoading: false,
                    page: resData.pagination.page,
                    totalPages: resData.pagination.totalPages,
                    total: resData.pagination.total,

                }));
                return resData.recipes;
            }


            const userLS = getLSUserData();
            if (!userLS.idToken) { 
                recipeStore.update((state) => ({
                    ...state,
                    recipes: [],
                    isLoading: false,
                    page: 0,
                    totalPages: 0,
                    total: 0,

                }));
                return [];
             }
            // Step 2: Search with GPT
            const res = await fetch(`${API_URL}/GPT_ingredients_to_recipe${paramStr}&id_token=${userLS.idToken}&allergies=${userLS.allergies}`);

            if (!res.ok) throw new Error(res.statusText || "Failed to search for recipes with ingredients " + ingredients);

            const recipes = await res.json();
            if (recipes.length > 0) {
                recipeStore.update((state) => ({
                    ...state,
                    recipes,
                    isLoading: false,
                    page: 1,
                    totalPages: 1,
                    total: recipes.length,
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
}