<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
	import type { Recipe } from '../../types'; 

    const API_URL = import.meta.env.VITE_API_URL;
	
    let recipe: Recipe | null = null;
    $: recipeId = $page.params.id;

	async function fetchRecipe() {
		try {
			const res = await fetch(`${API_URL}/recipes/${recipeId}`);
			if (!res.ok) throw new Error("Failed to get recipe detail");

			recipe = await res.json();
			
		} catch (e) {
			alert((e as Error).message);
		}
	}
    onMount(async () => {
        try {
			const res = await fetch(`${API_URL}/recipes/${recipeId}`);
			if (!res.ok) throw new Error('Failed to fetch recipe details');
			console.log("recipe detail", res.json());
			recipe = await res.json();
		} catch (e) {
			alert((e as Error).message);
		}
    });
</script>

{#if recipe}
	<div class="p-6">
		<h1 class="text-2xl font-bold">{recipe.name}</h1>
		<img src={recipe.img_url} class="mt-4 w-full rounded-lg object-cover" alt={recipe.name} />

		<h2 class="mt-6 text-lg font-semibold">Description</h2>
		<div class="flex items-center justify-between">
			<p>Time {recipe.time}</p>
			<p>Calories {recipe.calories}</p>
		</div>
		<h2 class="mt-6 text-lg font-semibold">Ingredients</h2>
		<ul class="list-disc pl-6">
			{#each recipe.ingredients as ingredient}
				<li>{ingredient.quantity} {ingredient.name}</li>
			{/each}
		</ul>

		<h2 class="mt-6 text-lg font-semibold">Instructions</h2>
		<ol>
			{#each recipe.instructions as instruction}
				<li>{instruction}</li>
			{/each}
		</ol>
	</div>
{:else}
	<p>Recipe not found. <a href="/" class="text-teal-600">Go back to home</a></p>
{/if}
