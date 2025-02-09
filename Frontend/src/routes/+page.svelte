<script lang="ts">
	import {customStyles} from '../custom'
	import Category from '$lib/components/Category.svelte';
	import IngredientInput from '$lib/components/IngredientInput.svelte';
	import RecipeList from '$lib/components/RecipeList.svelte';
	import AddRecipeModal from '$lib/components/AddRecipeModal.svelte';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';

	let name = 'Beautiful';
	let showModal = false;
	let userId: string | null = null;
	let authenticated: boolean = false;

	function toggleModal() {
		showModal = !showModal;
	}
	onMount(() => {

		if (browser) {
			const styleElement = document.createElement('style');
			styleElement.innerHTML = customStyles;
			document.head.appendChild(styleElement);
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
	<div>
		<img src="/home.jpg" class="mx-auto h-1/2 w-auto" alt="(Adobe stock) Home banner" />
	</div>
	<nav-bar class={customStyles.navBar}>
		<div class="font-sans text-3xl  text-teal-600">Hello, {name}! </div>
		<div>
			<a href="/" class={customStyles.aTag}>Home</a> |
			<a href="/user" class={customStyles.aTag}>User</a>
		</div>
	</nav-bar>
	<!-- Categories -->
	<Category />

	<!-- Ingredient input -->
	<IngredientInput />

	<div class="flex items-center justify-between p-2 sm:p-2 md:p-5 lg:p-9">
		<h2 class={customStyles.heading}>Recipes</h2>
		{#if authenticated}
			<button class="bg-primary-orange  outline-secondary-green rounded-2xl text-lg text-black outline" on:click={toggleModal}>
				Add Recipe
			</button>
		{/if}
	</div>
	<!-- Recipe -->
	<RecipeList />
	<AddRecipeModal {showModal} {toggleModal} {userId} {authenticated} />

</main>