<script lang="ts">
	import { Button, Input, Spinner } from 'flowbite-svelte';
	import { recipeHandler, recipeStore } from '$lib/stores/recipeStore';
	import { derived } from 'svelte/store';

	// For searching
	let searchType = 'ingredients'; // default: search by name, other: by ingredients
	let searchQuery = '';

	const isLoading = derived(recipeStore, ($recipeStore) => $recipeStore.isLoading);

	async function handleSearchSubmit() {
		recipeStore.update((state) => ({ ...state, isLoading: true }));
		if (!searchQuery.trim()) {
			try {
				await recipeHandler.getRecipes(null);
				return;
			} catch (e) {
				console.error((e as Error).message)
			}
		}

		try {
			if (searchType === 'name') {
				await recipeHandler.getRecipes(searchQuery.trim());
			} else if (searchType === 'ingredients') {
				//regex to remove all commas and special characters
				searchQuery = searchQuery.replace(/[^a-zA-Z0-9 ]/g, '');
				console.log('searchQuery',searchQuery);
				await recipeHandler.searchRecipesGPT(searchQuery.trim());

				await new Promise((resolve) => setTimeout(resolve, 13000));

				// After the delay, call getRecipes
				await recipeHandler.getRecipes(null);
			}
		} catch (e) {
			console.error(e);
		}

		// Reset search query
		searchQuery = '';
	}
</script>

<div class="flex flex-col justify-normal p-2 sm:p-2 md:p-5 lg:p-9">
	<h1 class="mb-4 text-lg sm:text-xl md:text-2xl lg:text-3xl">What do you want to cook today?</h1>

	<!-- Search Mode Selector -->
	<div class="mb-4 flex space-x-4">
		<label class="flex cursor-pointer items-center space-x-2">
			<input type="radio" bind:group={searchType} value="ingredients" />
			<span> AI Generated Recipe </span>
		</label>
		<label class="flex cursor-pointer items-center space-x-2">
			<input type="radio" bind:group={searchType} value="name" />
			<span>Search by name</span>
		</label>
	</div>

	<!-- Search bar -->
	<div class="flex gap-3">
		<Input
			aria-label="ingredients-input-box"
			type="text"
			bind:value={searchQuery}
			on:keydown={(event) => {
				if (event.key === 'Enter') handleSearchSubmit();
			}}
			placeholder={searchType === 'name'
				? 'Enter recipe name'
				: 'Enter 5 ingredients to generate a recipe'}
			class="outline-secondary-green rounded-2xl text-lg outline"
		/>
		<Button
			on:click={handleSearchSubmit}
			class="bg-primary-orange  outline-secondary-green rounded-2xl text-lg text-black outline"
			>Search</Button
		>
	</div>

	{#if $isLoading}
		<div class="mt-4 flex justify-center">
			<Spinner size={10} color="green" />
		</div>
	{/if}
</div>
