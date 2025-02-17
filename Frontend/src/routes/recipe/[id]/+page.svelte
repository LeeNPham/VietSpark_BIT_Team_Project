<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import type { RecipeDetailDTO } from '$lib/types';
	import { recipeHandler, recipeStore} from '$lib/stores/recipeStore';
	import { Button } from 'flowbite-svelte';


	let recipe: RecipeDetailDTO | null = null;
	let recipeId : string;
	$: recipeId = $page.params.id;

	async function fetchRecipe() {
		try {
			await recipeHandler.getRecipe(recipeId);
			recipe = $recipeStore.currentRecipe;
		} catch (e) {
			alert((e as Error).message);
		}
	}
	
	onMount(fetchRecipe);

	async function handleAddFavorite() {
		const recipesLS = localStorage.getItem('recipes')
			if (recipesLS?.includes(recipeId)) {return alert('Recipe already already favorited')}
		try {
			await recipeHandler.favoriteRecipe(recipeId)
			let userRecipes = recipesLS +"," + recipeId
			localStorage.setItem('recipes', userRecipes)
            alert('Recipe added to favorites');
        } catch (e) {
            alert((e as Error).message);
        }
	}

</script>
<div class="py-4 flex rounded-full justify-end flex-wrap">

	<div>
		<a href="/" class="text-teal-600 font-semibold">Home</a> |
		<a href="/user" class="text-teal-600 font-semibold">User</a>
	</div>
</div>
{#if recipe}
	<div class="p-6">
		<h1 class="text-2xl font-bold text-teal-600">{recipe.name}</h1>
		<img src={recipe.img_url} class="mt-4 w-full rounded-lg object-cover" alt={recipe.name} />

		<h2 class="mt-6 text-lg font-semibold text-blue-500">Description</h2>
		<div class="flex items-center justify-center">
			<div class="rounded-full bg-teal-300 p-2 mx-2">Time {recipe.time}</div>
			<div class="rounded-full bg-yellow-300 p-2 mx-2">Calories: {recipe.calories ? recipe.calories : "Unknown"}</div>
			<div class="rounded-full bg-green-300 p-2 mx-2">Servings: {recipe.servings}</div>
		</div>
		<h2 class="mt-6 text-lg font-semibold text-blue-500">Ingredients</h2>
		<ul class="list-disc pl-6">
			{#each recipe.ingredients as ingredient}
				<li>{ingredient.ingredientName} {ingredient.ingredientAmount}</li>
			{/each}
		</ul>

		<h2 class="mt-6 text-lg font-semibold text-blue-500">Instructions</h2>
		<ol>
			{#each recipe.instructions as instruction, i}
				<li>{i + 1}. {instruction}</li>
			{/each}
		</ol>
	</div>
	<Button
		class="mb-3 py-2 font-sans text-lg font-semibold text-white rounded-full bg-secondary-forest hover:bg-secondary-blue hover:text-black hover:outline hover:outline-secondary-forest whitespace-nowrap"
		onclick={handleAddFavorite}>
		Add to favorite
	</Button>

{:else}
	<p>Recipe not found. <a href="/" class="text-teal-600">Go back to home</a></p>
{/if}
