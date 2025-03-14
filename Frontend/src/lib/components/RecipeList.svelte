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
	let shownDescriptions = {};

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

	function toggleDescription(recipeId: string) {
		shownDescriptions[recipeId] = !shownDescriptions[recipeId];
		shownDescriptions = { ...shownDescriptions };
	}
</script>

<!-- <input
	type="text"
	class="w-full rounded-lg border border-gray-300 p-2"
	placeholder="Search for recipes"
	bind:value={searchTerm}
/> -->

<div
	class="mb-4 grid grid-cols-1 place-content-center gap-4 sm:grid-cols-2 md:p-5 lg:grid-cols-2 xl:grid-cols-2"
>
	{#if myRecipesData}
		{#each myRecipesData as item (item.recipe_id)}
			<div class="space-y-4">
				<Card
					img={item.img_url}
					class="m-3 mx-auto flex-shrink-0 rounded-lg bg-cover bg-center bg-no-repeat shadow-lg"
					href={`/recipe/${item.recipe_id}`}
					horizontal
					size="md"
				>
					{#if shownDescriptions[item.recipe_id]}
						<p class="text-md"><strong>⏰ Time:</strong> {item.time} mins</p>
						<p class="text-md"><strong>🔥 Calories:</strong> {item.calories} kcal</p>
						<p class="text-md"><strong>🥘 Servings:</strong> {item.servings}</p>
						<div class="mt-10 flex items-end justify-between">
							<button
								class="text-primary-600 hover:text-primary-800 dark:text-primary-400 dark:hover:text-primary-300 mt-auto flex w-fit items-center"
								onclick={(event) => {
									event.preventDefault();
									toggleDescription(item.recipe_id);
								}}
								aria-label="Hide description"
							>
								<span class="mr-2">Back</span>
								<svg class="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M15 19l-7-7 7-7"
									/>
								</svg>
							</button>
						</div>
					{:else}
						<h5
							class="mb-3 line-clamp-2 text-xl font-bold tracking-tight text-gray-900 dark:text-white"
						>
							{item.name}
						</h5>
						<div class="mt-10 flex items-end justify-between">
							<div></div>
							<button
								class="text-primary-600 hover:text-primary-800 dark:text-primary-400 dark:hover:text-primary-300 mt-auto flex w-fit items-center"
								onclick={(event) => {
									event.preventDefault();
									toggleDescription(item.recipe_id);
								}}
							>
								<span class="mr-2">Summary</span>
								<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M9 5l7 7-7 7"
									/>
								</svg>
							</button>
						</div>
					{/if}
				</Card>
			</div>
		{/each}
	{:else}
		<div class="flex h-full w-full items-center justify-center">
			<p class="text-center text-teal-600">No recipes found. Please try again later.</p>
		</div>
	{/if}
</div>
