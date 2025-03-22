<script lang="ts">
	import { customStyles } from '$src/custom';

	import Category from '$lib/components/Category.svelte';
	import IngredientInput from '$lib/components/IngredientInput.svelte';
	import RecipeList from '$lib/components/RecipeList.svelte';
	import AddRecipeModal from '$lib/components/AddRecipeModal.svelte';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { Button } from 'flowbite-svelte';

	let name = 'Beautiful';
	let showModal = false;
	let userId: string | null = null;
	let authenticated: boolean = false;

	function toggleModal() {
		showModal = !showModal;
	}
	onMount(() => {
		if (browser) {
			authenticated = localStorage.getItem('authenticated') === 'true';
			userId = localStorage.getItem('userId');
		}
	});
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<main>
	<!-- Categories -->
	<Category />

	<!-- Ingredient input -->
	<IngredientInput />

	<div class="flex items-center justify-between p-2 sm:p-2 md:p-5 lg:p-7">
		<h2 class={customStyles.heading}>Recipes</h2>
		{#if authenticated}
			<Button
				class="bg-primary-green outline-secondary-green rounded-2xl p-2 text-sm text-black outline"
				on:click={toggleModal}
			>
				+ Recipe
			</Button>
		{/if}
	</div>
	<!-- Recipe -->
	<RecipeList />
	<AddRecipeModal {showModal} {toggleModal} {userId} {authenticated} />
</main>
