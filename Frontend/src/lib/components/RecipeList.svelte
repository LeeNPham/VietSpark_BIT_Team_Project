<script lang="ts">
	//@ts-nocheck
	import type { RecipeDTO } from '$lib/types';
	import { recipeHandler, recipeStore } from '$lib/stores/recipeStore';
	import { Card, Pagination, PaginationItem } from 'flowbite-svelte';
	import { ArrowLeftOutline, ArrowRightOutline } from 'flowbite-svelte-icons';
	import RecipeItem from './RecipeItem.svelte';
	import { showToast } from '$lib/stores/alertStore';

	let myRecipesData: RecipeDTO[] = [];
	let currentPage = 1;
	let limit = 10;
	let offset = 0;
	let totalPages = 0;
	let total = 0;

	const fetchRecipes = async () => {
		try {
			await recipeHandler.getRecipes(null, limit, offset);
		} catch (e) {
			showToast('error', 'Error fetching recipes: ' + e.message);
		}
	};

	function nextPage() {
		if (currentPage < totalPages) {
			currentPage += 1;
			offset = (currentPage - 1) * limit;
			fetchRecipes();
		}
	}
	function prevPage() {
		if (currentPage > 1) {
			currentPage -= 1;
			offset = (currentPage - 1) * limit;
			if (offset < 0) {
				offset = 0;
			}
			fetchRecipes();
		}
	}

	recipeStore.subscribe((store) => {
		const newRecipes = store.recipes || [];
		total = store.total || 0;
		totalPages = store.totalPages || 0;
		currentPage = store.page || 1;

		if (newRecipes.length > 0) {
			myRecipesData = newRecipes;
		}
	});
</script>

<div class="mb-4 gap-4">
	{#if myRecipesData.length > 0}
		<div
			class="grid grid-cols-1 place-content-center sm:grid-cols-2 md:p-5 lg:grid-cols-2 xl:grid-cols-2"
		>
			{#each myRecipesData as item (item.recipe_id)}
				<RecipeItem {item} />
			{/each}
		</div>
		<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 md:p-5 lg:grid-cols-2 xl:grid-cols-2">
			<div class="flex justify-start">
				{#if currentPage > 1}
					<PaginationItem
						large
						class="bg-secondary-forest hover:bg-secondary-forest-light hover:text-white flex items-center rounded-lg px-4 py-2 text-white transition-colors duration-200 disabled:bg-gray-400 disabled:text-gray-600 disabled:hover:bg-gray-400"
						on:click={prevPage}
						disabled={currentPage === 1}
					>
						<ArrowLeftOutline class="me-2 h-5 w-5" />
						Previous
					</PaginationItem>
				{/if}
			</div>
			<div class="flex justify-end">
				{#if currentPage < totalPages}
					<PaginationItem
						large
						class="bg-primary-green hover:bg-primary-green-dark flex items-center rounded-lg px-4 py-2 text-black transition-colors duration-200 disabled:bg-gray-200 disabled:text-gray-600 disabled:hover:bg-gray-200"
						on:click={nextPage}
						disabled={currentPage >= totalPages}
					>
						Next
						<ArrowRightOutline class="ms-2 h-5 w-5" />
					</PaginationItem>
				{/if}
			</div>
		</div>
	{:else}
		<div class="flex h-full w-full items-center justify-center">
			<p class="text-center text-teal-600">
				{$recipeStore.recipes ? 'No recipes found.' : 'Loading recipes...'}
			</p>
		</div>
	{/if}
</div>
