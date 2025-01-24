<script>
	import { Button } from 'flowbite-svelte';
	import RecipeList from '../recipe/RecipeList.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	const API_URL = import.meta.env.VITE_API_URL;

	let name = 'Beautiful';
	let allergies = ['Peanuts', 'Shellfish', 'Sumthing else', 'Bad ppl'];
	let myRecipe = [];
	let authenticated = false;

	onMount(() => {
		authenticated = localStorage.getItem('authenticated') === 'true';
	});

	function goToLogin() {
		goto('/hong-prototype/login');
	}
</script>

{#if authenticated}
	<div class="flex flex-wrap items-center justify-between rounded-full py-4">
		<div class="font-sans text-3xl font-bold text-teal-400">Hello {name}! Edit yourself!</div>
		<div>
			<a href="/hong-prototype" class="text-teal-400">Home</a> |
			<a href="/hong-prototype/user" class="text-teal-400">User</a>
		</div>
	</div>

	<!-- Allergies -->
	<p class="my-2 font-sans text-xl font-semibold text-teal-400">Allergies</p>
	<div class="flex flex-wrap justify-between gap-4">
		{#each allergies as allergy, i}
			<Button
				class="my-4 gap-4 bg-white text-teal-600 outline outline-teal-300 hover:bg-teal-300 hover:text-white focus:outline-none"
			>
				{allergy}
			</Button>
		{/each}
	</div>

	<!-- Favorite Recipes -->
	<p class="my-2 font-sans text-xl font-semibold text-teal-400">Favorite recipes</p>
	<div class="flex flex-wrap justify-center gap-4">
		<RecipeList />
	</div>
{:else}
	<!-- Show login prompt if not authenticated -->
	<div class="flex h-screen flex-col items-center justify-center">
		<p class="text-xl font-semibold text-teal-600">Please login first</p>
		<Button
			on:click={goToLogin}
			class="mt-4 rounded bg-teal-600 px-4 py-2 text-white hover:bg-teal-400"
		>
			Go to Login
		</Button>
	</div>
{/if}
