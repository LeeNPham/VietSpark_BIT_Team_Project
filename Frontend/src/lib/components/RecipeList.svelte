<script lang="ts">
	//@ts-nocheck
	import type { RecipeDTO } from '$lib/types';
	import { recipeHandler, recipeStore } from '$lib/stores/recipeStore';

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

<div class="mb-4 grid grid-cols-1 gap-2 sm:grid-cols-2 md:p-5 lg:grid-cols-3 xl:grid-cols-4">
	{#if myRecipesData}
		{#each myRecipesData as item (item.recipe_id)}
			<a
				class="mb-4 flex w-full items-center gap-4 rounded-lg p-4"
				href={`/recipe/${item.recipe_id}`}
			>
				<div class="flex w-full items-center gap-4">
					<img src={item.img_url} class="h-20 w-20 rounded-lg object-cover" alt={item.name} />
					<div class="flex-1">
						<p class="line-clamp-1">{item.name}</p>
						<div class="text-secondary-forest space-x-2 text-sm font-medium">
							<span>{item.time} minutes</span>
							<span>*</span>
							<span>{item.numIngredients} ingredients</span>
						</div>
					</div>
				</div>
			</a>
		{/each}
	{:else}
		<div class="flex h-full w-full items-center justify-center">
			<p class="text-center text-teal-600">No recipes found. Please try again later.</p>
		</div>
	{/if}
</div>
