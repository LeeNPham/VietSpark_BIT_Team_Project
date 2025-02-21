<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { recipeHandler } from '$lib/stores/recipeStore';
	import { userHandler } from '$lib/stores/userStore';
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
	import { customStyles } from '$src/custom';

	/** @type {{children: import('svelte').Snippet}} */
	let { children } = $props();
	let authenticated = localStorage.getItem('authenticated') == 'true';
	onMount(async () => {
		userHandler.checkSessionExpiration();
		console.log('Preloading recipes');

		try {
			await recipeHandler.getRecipes(null);
		} catch (e) {
			console.error(e as Error);
		}
	});

	function handlerSignOut() {
		userHandler.signOut();
	}

</script>

<div class="app">
	<Navbar class={customStyles.navBar} style="background-color:#ecf3fe;">
		<img src="/VS_CHEF.png" class="h-20" alt="Flowbite Logo" />
		<NavHamburger />
		<NavUl>
			<NavLi href="/" class={customStyles.aTag}>Home</NavLi>
			<NavLi href="/user" class={customStyles.aTag}>User</NavLi>
			{#if authenticated}
			<NavLi href="/" class={customStyles.aTag} on:click={handlerSignOut}>Sign out</NavLi>
			{/if}
		</NavUl>
	</Navbar>
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
