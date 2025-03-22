<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { recipeHandler } from '$lib/stores/recipeStore';
	import { userHandler, userStore } from '$lib/stores/userStore';
	import { Navbar, NavLi, NavUl, NavHamburger, NavBrand } from 'flowbite-svelte';
	import { customStyles } from '$src/custom';
	import { browser } from '$app/environment';
	import CustomToast from '$lib/components/CustomToast.svelte';

	/** @type {{children: import('svelte').Snippet}} */
	let { children } = $props();
	let authenticated = $derived($userStore.authenticated);
	onMount(async () => {
		userHandler.checkAuthenticated();
		userHandler.checkSessionExpiration();


		console.log('Preloading recipes');
		recipeHandler.getRecipes(null, 10, 0).catch((e) => {
			console.log('Recipe fetch error:', e); // Debug log
		});

		const intervalId = setInterval(async () => {
			if (!browser) return;
			if (!authenticated) return;
			try {
				await userHandler.refreshToken();
			} catch (e) {
				console.log('Token refresh error:', e); // Debug log
			};

		getLocation()

		}, 60 *  60 * 1000);
	});

	function handlerSignOut() {
		userHandler.signOut();
	}


	function getLocation() {
    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                console.log("Latitude:", position.coords.latitude, "Longitude:", position.coords.longitude);
            },
            (err) => {
                console.error("Error getting location:", err.message);
            },
            { enableHighAccuracy: true } // Request high-accuracy location
        );
    } else {
        console.error('Geolocation is not supported in your browser.');
    }
	}
</script>

<div class="app">
	<Navbar class={customStyles.navBar} style="background-color:#ecf3fe;">
		<NavBrand href="/">
			<img src="/VS_CHEF.png" class="h-12 sm:h-12 md:h-18 lg:h-20" alt="Flowbite Logo" />
		</NavBrand>
		<NavHamburger />
		<NavUl>
			<NavLi href="/" class={customStyles.aTag}>Home</NavLi>
			{#if authenticated}
				<NavLi href="/user" class={customStyles.aTag}>User</NavLi>
				<NavLi href="/" class={customStyles.aTag} on:click={handlerSignOut}>Sign out</NavLi>
			{:else}
				<NavLi href="/login" class={customStyles.aTag}>Login</NavLi>
			{/if}
		</NavUl>
	</Navbar>
	<main>
		<CustomToast />
		{@render children()}
	</main>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		position: relative;
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
