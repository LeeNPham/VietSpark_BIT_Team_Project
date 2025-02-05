<script>
	import Header from '../lib/components/Header.svelte';
	import '../app.css';
	import { onMount } from 'svelte';
	import { recipeHandler } from '$lib/stores/recipeStore';
	import { userHandler } from "$lib/stores/userStore";


	/** @type {{children: import('svelte').Snippet}} */
	let { children } = $props();

	onMount(async() => {
		userHandler.checkSessionExpiration();
		console.log("Preloading recipes");
		await recipeHandler.getRecipes(null);
	
	})
	
</script>

<div class="app">
	<Header />

	<main>
		{@render children()}
	</main>

</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem;
		width: 100%;
		max-width: 64rem;
		margin: 0 auto;
		box-sizing: border-box;
	}
</style>
