import { writable } from "svelte/store";
export const ingredients = writable<string[]>([]);

export const categories = writable([
    "Chicken", "Beef", "Fish", "Pork", "Cauliflower"
])
export const ingredientHandler = {
    /**
     * @param {string} newIngredient
     */
    addIngredient: (newIngredient: string) => {
        if (newIngredient) {
            ingredients.update((current) => [...current, newIngredient]);
        }
    },

    /**
     * @param {number} index
     */
    removeIngredient: (index: number) => {
        ingredients.update((current) => current.filter((_, i) => i !== index));
    }
}
