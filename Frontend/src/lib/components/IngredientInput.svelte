<script lang="ts">
	import { Button, Input, Spinner, Tooltip } from 'flowbite-svelte';
	import { recipeHandler, recipeStore } from '$lib/stores/recipeStore';
	import { userStore } from '$lib/stores/userStore';
	import { derived } from 'svelte/store';

	// For searching
	let authenticated: boolean = false;
	userStore.subscribe((state) => {
		authenticated = state.authenticated;
	});

	let searchType = (authenticated ? 'ingredients' : 'name'); // default: search by name, other: by ingredients
	let searchQuery = '';

	const isLoading = derived(recipeStore, ($recipeStore) => $recipeStore.isLoading);

	async function handleSearchSubmit() {
		recipeStore.update((state) => ({ ...state, isLoading: true }));
		if (!searchQuery.trim()) {
			try {
				await recipeHandler.getRecipes(null, 10, 0);
				return;
			} catch (e) {
				console.error((e as Error).message);
			}
		}

		try {
			if (searchType === 'name') {
				await recipeHandler.getRecipes(searchQuery.trim(), 10, 0);
			} else if (searchType === 'ingredients') {
				//regex to remove all commas and special characters
				searchQuery = searchQuery.replace(/[^a-zA-Z0-9 ]/g, '');
				await recipeHandler.searchRecipesGPT(searchQuery.trim());

				await new Promise((resolve) => setTimeout(resolve, 13000));

				// After the delay, call getRecipes
				await recipeHandler.getRecipes(null, 10, 0);
			}
		} catch (e) {
			console.error(e);
		}

		// Reset search query
		searchQuery = '';
	}
</script>

<div class="flex flex-col justify-normal p-2 sm:p-2 md:p-5 lg:p-7">
	<h1
		class="text-secondary-forest mb-6 text-xl sm:mb-6 sm:text-xl md:mb-8 md:text-3xl lg:mb-10 lg:text-4xl"
	>
		What would you like to cook?
	</h1>
	<Tooltip
		>Select from an AI-Generated Recipe or choose from our collection of curated recipes.</Tooltip
	>

	<!-- Search Mode Selector -->
	<div class="mb-4 flex space-x-4">
		{#if authenticated}
			<label
				class="flex cursor-pointer items-center space-x-2 text-sm sm:text-sm md:text-xl lg:text-2xl"
			>
				<input type="radio" bind:group={searchType} value="ingredients" />
				<span> AI Generated Recipe </span>
			</label>
		{/if}
		<label
			class="flex cursor-pointer items-center space-x-2 text-sm sm:text-sm md:text-xl lg:text-2xl"
		>
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
			class="outline-secondary-green sm: rounded-2xl text-sm outline md:text-lg lg:text-xl"
		/>
		<Button
			on:click={handleSearchSubmit}
			class="bg-primary-green outline-secondary-green rounded-2xl p-2 text-sm text-black outline"
			>Search</Button
		>
	</div>

	{#if $isLoading}
		<div class="mt-4 flex justify-center">
			<Spinner size={10} color="green" />
		</div>
	{/if}
</div>
