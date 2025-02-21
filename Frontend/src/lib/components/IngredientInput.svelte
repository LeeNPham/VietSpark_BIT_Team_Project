<script lang="ts">
	import { Button, Input, Spinner, Tooltip } from 'flowbite-svelte';
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

<div class="flex flex-col justify-normal p-2 sm:p-2 md:p-5 lg:p-7">
	<h1 class="mb-6 sm:mb-6 md:mb-8 lg:mb-10 text-xl sm:text-xl md:text-3xl lg:text-4xl text-secondary-forest">What would you like to cook? </h1>
	<Tooltip>Select from an AI-Generated Recipe or choose from our collection of curated recipes.</Tooltip>

	<!-- Search Mode Selector -->
	<div class="mb-4 flex space-x-4">
		<label class="flex cursor-pointer items-center space-x-2 text-sm sm:text-sm md:text-xl lg:text-2xl">
			<input type="radio" bind:group={searchType} value="ingredients" />
			<span> AI Generated Recipe </span>
		</label>
		<label class="flex cursor-pointer items-center space-x-2 text-sm sm:text-sm md:text-xl lg:text-2xl">
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
			class="outline-secondary-green rounded-2xl text-sm sm: text-sm md:text-lg lg:text-xl outline"
		/>
		<Button
			on:click={handleSearchSubmit}
			class="bg-primary-green outline-secondary-green rounded-2xl text-sm text-black outline p-2"
			>Search</Button
		>
	</div>

	{#if $isLoading}
		<div class="mt-4 flex justify-center">
			<Spinner size={10} color="green" />
		</div>
	{/if}
</div>
