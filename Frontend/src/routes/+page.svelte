<script lang="ts">
	import {customStyles} from '../custom'
	import Category from '$lib/components/Category.svelte';
	import IngredientInput from '$lib/components/IngredientInput.svelte';
	import RecipeList from '$lib/components/RecipeList.svelte';
	import AddRecipeModal from '$lib/components/AddRecipeModal.svelte';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';

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
	<!-- <img src="/home.jpg" alt="(Adobe stock) Home banner" /> -->
	<Navbar class={customStyles.navBar}>
		<div  class="font-sans text-3xl  text-secondary-forest">
			Hello, {name}!
		</div>
		<NavHamburger/>
		<NavUl>
			<NavLi href="/" class={customStyles.aTag}>
				Home
			</NavLi>
			<NavLi href="/user" class={customStyles.aTag}>
				User
			</NavLi>
		</NavUl>
	</Navbar>

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