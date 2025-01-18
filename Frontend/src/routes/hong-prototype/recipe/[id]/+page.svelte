<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { recipeStore } from '../../../stores/recipeStore';

    let recipe;
    $: recipeId = $page.params.id;

    onMount(() => {
        recipeStore.subscribe((store) => {
            recipe = store.recipes.find((r) => r.id === recipeId);
        });
    });
</script>

{#if recipe}
	<div class="p-6">
		<h1 class="text-2xl font-bold">{recipe.name}</h1>
		<img src={recipe.image} class="mt-4 w-full rounded-lg object-cover" alt="Recipe image">
	
		<h2 class="mt-6 text-lg font-semibold">Description</h2>
		<div class="flex items-center justify-between">
			<p>Duration {recipe.duration}</p>
			<p>Duration {recipe.calories}</p>
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
{/if}
{:else}
	<p>Recipe not found. <a href="/" class="text-indigo-600">Go back to home</a></p>
{/if}