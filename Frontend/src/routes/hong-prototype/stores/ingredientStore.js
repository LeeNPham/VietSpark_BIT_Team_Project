import { writable } from "svelte/store";
export const ingredients = writable([]);

export const categories = writable([
    "Chicken", "Beef", "Fish", "Pork", "Cauliflower", "Fruit", "Bakery", "Dessert", "Broccoli", "Carrot"
])
export const ingredientHandler = {
    /**
     * @param {string} newIngredient
     */
    addIngredient: (newIngredient) => {
        if (newIngredient) {
            ingredients.update((current) => [...current, newIngredient]);
        }
    },

    /**
     * @param {number} index
     */
    removeIngredient: (index) => {
        ingredients.update((current) => current.filter((_, i) => i !== index));
    }
}
