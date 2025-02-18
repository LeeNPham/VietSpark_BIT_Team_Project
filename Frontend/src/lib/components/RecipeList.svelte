<script lang="ts">
	//@ts-nocheck
	import type { RecipeDTO } from '$lib/types';
    import { recipeStore } from '$lib/stores/recipeStore';

	export let myRecipes = [] // passed down option property in the case that a user has favorited recipes

	let myRecipesData = []
	let recipes: RecipeDTO[] | [] = [];

	recipeStore.subscribe((store) => {
		recipes = store.recipes;
	});

	$: if (myRecipes.length > 0) {
		myRecipesData = recipes.filter(recipe => myRecipes.includes(recipe.recipe_id));
	} else {
		myRecipesData = recipes
	}
</script>

<div class="mb-4 grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 md:p-5 w-full sm:w-3/4 md:w-1/2 lg:w-1/3 xl:w-1/4">
	{#if myRecipesData.length > 0}
		{#each myRecipesData as item}
			<a
				class="mb-4 flex w-full items-center gap-4 rounded-lg p-4"
				href={`/recipe/${item.recipe_id}`}
			>
				<div class="flex w-full items-center gap-4">
					<img src={item.img_url} class="h-20 w-20 rounded-lg object-cover" alt={item.name} />
					<div class="flex-1">
						<p class="line-clamp-1">{item.name}</p>
						<div class="space-x-2 text-sm font-medium text-teal-700">
							<span>{item.time} minutes</span>
							<span>*</span>
							<span>{item.numIngredients} ingredients</span>
						</div>
					</div>
				</div>
			</a>
		{/each}
	{:else}
		<div class="flex items-center justify-center h-full">
			<p class="text-center text-teal-600">No recipes found. Please try again later.</p>
		</div>
	{/if}
</div>