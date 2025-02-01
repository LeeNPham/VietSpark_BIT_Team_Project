<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import type { Recipe } from '../../types';

	const API_URL = import.meta.env.VITE_API_URL;

	let recipe: Recipe | null = null;
	$: recipeId = $page.params.id;

	async function fetchRecipe() {
		try {
			const res = await fetch(`${API_URL}/check_recipe/${recipeId}`);
			if (!res.ok) throw new Error('Failed to get recipe detail');

			recipe = await res.json();
		} catch (e) {
			alert((e as Error).message);
		}
	}
	onMount(async () => {
		try {
			const res = await fetch(`${API_URL}/check_recipe/${recipeId}`);
			if (!res.ok) throw new Error('Failed to fetch recipe details');
			const recipeData = await res.json();
			console.log('recipe detail', recipeData); // Log the data
			recipe = recipeData;
		} catch (e) {
			alert((e as Error).message);
		}
	});
</script>
<div class="py-4 flex rounded-full justify-end flex-wrap">
	
	<div>
		<a href="/hong-prototype/home" class="text-teal-600 font-semibold">Home</a> |
		<a href="/hong-prototype/user" class="text-teal-600 font-semibold">User</a>
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
		</div>
		<h2 class="mt-6 text-lg font-semibold text-blue-500">Ingredients</h2>
		<ul class="list-disc pl-6">
			{#each recipe.ingredients as ingredient}
				<li>{ingredient.quantity} {ingredient.name}</li>
			{/each}
		</ul>

		<h2 class="mt-6 text-lg font-semibold text-blue-500">Instructions</h2>
		<ol>
			{#each recipe.instructions as instruction, i}
				<li>{i + 1}. {instruction}</li>
			{/each}
		</ol>
	</div>
{:else}
	<p>Recipe not found. <a href="/" class="text-teal-600">Go back to home</a></p>
{/if}
