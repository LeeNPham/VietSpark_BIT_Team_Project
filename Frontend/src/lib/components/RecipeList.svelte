<script lang="ts">
	//@ts-nocheck
	import type { RecipeDTO } from '$lib/types';
	import { recipeHandler, recipeStore } from '$lib/stores/recipeStore';
	import { Card } from 'flowbite-svelte';

	export let userRecipes = [];
	export let limit: number = 10;

	let myRecipesData: RecipeDTO[] = [];
	let shownDescriptions = {};
	let page = 1;
	let totalRecipes = 0;

	$: {
		const allRecipes = $recipeStore.recipes || [];
		let filteredRecipes = userRecipes.length
			? allRecipes.filter((recipe) => userRecipes.includes(recipe.recipe_id))
			: allRecipes;

		// Sort by creation_time (assuming it’s in the data)
		filteredRecipes = filteredRecipes.sort(
			(a, b) => new Date(b.creation_time) - new Date(a.creation_time)
		);

		totalRecipes = filteredRecipes.length;
		myRecipesData = filteredRecipes.slice(0, limit * page);
	}

	function loadMore() {
		page += 1;
	}

	function toggleDescription(recipeId: string) {
		shownDescriptions[recipeId] = !shownDescriptions[recipeId];
		shownDescriptions = { ...shownDescriptions };
	}
</script>

<div
	class="mb-4 grid grid-cols-1 place-content-center gap-4 sm:grid-cols-2 md:p-5 lg:grid-cols-2 xl:grid-cols-2"
>
	{#if myRecipesData.length > 0}
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
								class="text-primary-600 hover:text-primary-800 dark:text-primary-400 dark:hover:text-primary-300 flex w-fit items-center"
								on:click|preventDefault={() => toggleDescription(item.recipe_id)}
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
								class="text-primary-600 hover:text-primary-800 dark:text-primary-400 dark:hover:text-primary-300 flex w-fit items-center"
								on:click|preventDefault={() => toggleDescription(item.recipe_id)}
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
		{#if myRecipesData.length < totalRecipes}
			<div class="col-span-full text-center">
				<button class="bg-primary-green outline-secondary-green rounded-2xl text-sm text-black outline p-2" on:click={loadMore}>
					Load More
				</button>
			</div>
		{/if}
	{:else}
		<div class="flex h-full w-full items-center justify-center">
			<p class="text-center text-teal-600">
				{$recipeStore.recipes ? 'No recipes found.' : 'Loading recipes...'}
			</p>
		</div>
	{/if}
</div>
