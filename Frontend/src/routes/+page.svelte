<script lang="ts">
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

<div>
	<img src="/home.jpg" class="mx-auto h-1/2 w-auto" alt="(Adobe stock) Home banner" />
</div>
<div class="flex flex-wrap items-center justify-between rounded-full py-4">
	<div class="font-sans text-3xl font-extrabold text-teal-600">Hello {name}</div>
	<div>
		<a href="/" class="font-semibold text-teal-600">Home</a> |
		<a href="/user" class="font-semibold text-teal-600">User</a>
	</div>
</div>
<!-- Categories -->
<Category />

<!-- Ingredient input -->
<IngredientInput />

<div class="flex items-center justify-between">
	<h2 class="my-2 text-xl font-bold">Recipes</h2>
	{#if authenticated}
		<Button class="bg-teal-300 px-3 py-1 text-teal-900 hover:bg-teal-400" on:click={toggleModal}>
			Add Recipe
		</Button>
	{/if}
</div>
<!-- Recipe -->
<RecipeList />
<AddRecipeModal showModal={showModal} toggleModal={toggleModal} userId={userId} authenticated={authenticated} />
