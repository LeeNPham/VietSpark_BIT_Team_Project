<script lang="ts">
	//@ts-nocheck
	import type { RecipeDTO } from '$lib/types';
	import { recipeHandler, recipeStore } from '$lib/stores/recipeStore';
	import { onMount } from 'svelte';
	import RecipeItem from './RecipeItem.svelte';

	export let userRecipes = [];

	let myRecipesData: RecipeDTO[] = [];
	onMount(async () => {
		myRecipesData = await recipeHandler.getRecipeList(userRecipes);
	});

</script>

<div
	class="mb-4 grid grid-cols-1 place-content-center gap-4 sm:grid-cols-2 md:p-5 lg:grid-cols-2 xl:grid-cols-2"
>
	{#if myRecipesData.length > 0}
		{#each myRecipesData as item (item.recipe_id)}
			<RecipeItem item={item} />
		{/each}
	{:else}
		<div class="flex h-full w-full items-center justify-center">
			<p class="text-center text-teal-600">
				You have not liked any recipe.
			</p>
		</div>
	{/if}
</div>
