<script lang="ts">
	//@ts-nocheck
	import type { RecipeDTO } from '$lib/types';
	import { recipeHandler, recipeStore } from '$lib/stores/recipeStore';
	import { Card } from 'flowbite-svelte';

	export let myRecipes = []; // passed down option property in the case that a user has favorited recipes
	export let showFavorites = false;
	let searchTerm = '';
	let myRecipesData = [];
	let recipes: RecipeDTO[] | [] = [];

	recipeStore.subscribe((store) => {
		recipes = store.recipes;
	});

	// make sure to organize the recipes based on how recent it was created. this means we will need a createdAt attribute that uses new Date().toISOString()
	$: if (myRecipes.length > 0 || showFavorites) {
		myRecipesData = recipes.filter((recipe) => myRecipes.includes(recipe.recipe_id));
	} else {
		myRecipesData = recipes;
	}

	// look into fuze.js for better search functionality, this includes details on how to implement a fuzzy
	// $: if (searchTerm !== '') {
	// 	myRecipesData = myRecipesData.filter((recipe) =>
	// 		recipe.name.toLowerCase().includes(searchTerm.toLowerCase())
	// 	);
	// } else {
	// 	myRecipesData = recipes;
	// }
</script>

<!-- <input
	type="text"
	class="w-full rounded-lg border border-gray-300 p-2"
	placeholder="Search for recipes"
	bind:value={searchTerm}
/> -->

<div class="mb-4 grid grid-cols-1 gap-4 md:p-5 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-2 place-content-center">
	{#if myRecipesData}
		{#each myRecipesData as item (item.recipe_id)}
			<div class="space-y-4">
				<Card
					img={item.img_url}
					class="m-3 flex-shrink-0 rounded-lg bg-cover bg-center bg-no-repeat shadow-lg mx-auto"
					href={`/recipe/${item.recipe_id}`}
					horizontal
					size="md"
				>
					<h5
						class="mb-3 line-clamp-2 text-xl font-bold tracking-tight text-gray-900 dark:text-white"
					>
						{item.name}
					</h5>
					<p class="mb-3 font-normal text-gray-700 dark:text-gray-400 leading-relaxed">{item.time} minutes</p>
				</Card>
			</div>
		{/each}
	{:else}
		<div class="flex h-full w-full items-center justify-center">
			<p class="text-center text-teal-600">No recipes found. Please try again later.</p>
		</div>
	{/if}
</div>
