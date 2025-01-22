// import { writable } from "svelte/store";
// import { db } from "$lib/firebase/firebase.client";
// import { addDoc, deleteDoc, updateDoc, getDoc, getDocs, collection, doc } from "firebase/firestore";


// export const ingredients = writable([]);
// export const recipeStore = writable({
//     isLoading: true,
//     recipes: [],
//     currentRecipe: null
// });

// export const categories = writable([
//     "Chicken", "Beef", "Fish", "Pork", "Cauliflower", "Fruit", "Bakery", "Dessert", "Broccoli", "Carrot"
// ])
// export const ingredientHandler = {
//     /**
//      * @param {string} newIngredient
//      */
//     addIngredient: (newIngredient) => {
//         if (newIngredient) {
//             ingredients.update((current) => [...current, newIngredient]);
//         }
//     },

//     /**
//      * @param {number} index
//      */
//     removeIngredient: (index) => {
//         ingredients.update((current) => current.filter((_, i) => i !== index));
//     }
// }

// export const recipeHandler = {
//     addRecipe: async (recipeData) => {
//         try {
//             const recipeRef = collection(db, "recipes");
//             const newRecipeRef = await addDoc(recipeRef, { ...recipeData });
//             return newRecipeRef.id;
//         } catch (error) {
//             console.error("Error creating new recipe", error);
//             throw error
//         }
//     },
//     getRecipe: async (recipeId) => {
//         try {
//             const recipeRef = doc(db, "recipes", recipeId);
//             const recipeDoc = await getDoc(recipeRef);
//             if (recipeDoc.exists()) {
//                 recipeStore.update(state => ({
//                     ...state,
//                     isLoading: false,
//                     currentRecipe: { id: recipeDoc.id, ...recipeDoc.data() },
//                 }));
//             } else {
//                 console.warn(`Recipe ${recipeId} does not exist`);
//                 recipeStore.update(state => ({
//                     ...state,
//                     isLoading: false,
//                     currentRecipe: null,
//                 }))
//             }

//         } catch (error) {
//             console.error("Error finding recipe", recipeId);
//             throw error;
//         }
//     },
//     getRecipes: async () => {
//         const recipeRef = collection(db, 'recipes');
//         const snapshot = await getDocs(recipeRef);
//         const recipes = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
//         recipeStore.set({ isLoading: false, recipes });
//     },
//     updateRecipe: () => { },
//     deleteRecipe: async (recipeId) => {
//         const confirmation = window.confirm('Are you sure you want to delete this recipe?');
//         if (confirmation) {
//             try {
//                 const recipeRef = doc(db, 'recipes', recipeId);
//                 await deleteDoc(recipeRef);
//                 alert('Recipe successfully deleted');
//             } catch (error) {
//                 console.error(`Error deleting recipe ${recipeId}`, error);
//             }
//         }
//     },

// }