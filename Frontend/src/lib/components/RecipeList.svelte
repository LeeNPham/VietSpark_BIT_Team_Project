<script lang="ts">
	import type { RecipeDTO } from '$lib/types';
	import { recipeStore } from '$lib/stores/recipeStore';

	let recipes: RecipeDTO[] | [] = [];
	recipeStore.subscribe((store) => {
		recipes = store.recipes;
	});
</script>

<div class="mb-4 grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
	{#if recipes.length > 0}
		{#each recipes as item}
			<a
				class="mb-4 flex w-full items-center gap-4 rounded-lg p-4"
				href={`/recipe/${item.recipe_id}`}
			>
				<div class="flex w-full items-center gap-4">
					<img src={item.img_url} class="h-20 w-20 rounded-lg object-cover" alt={item.name} />
					<div class="flex-1">
						<p>{item.name}</p>
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
		<p class="text-center text-teal-600">No recipes found. Please try again later.</p>
	{/if}
</div>
