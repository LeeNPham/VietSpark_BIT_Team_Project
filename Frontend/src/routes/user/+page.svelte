<script lang="ts">
	import { Button } from 'flowbite-svelte';
	import RecipeList from '$lib/components/RecipeList.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import type { UserDTO } from '$lib/types';
	import { userHandler, userStore } from '$lib/stores/userStore';

	export let userId: string | null;
	export let user: UserDTO | null;
	let allergies: string[] = ['Test'];
	let authenticated = false;
	let newAllergy = '';

	onMount(fetchUserInfo);

	async function fetchUserInfo() {
		try {
			authenticated = localStorage.getItem('authenticated') === 'true';
			if (!authenticated) {
				goto('/login');
				throw new Error("User is not authentiated");
			}

			userId = localStorage.getItem('userId');
			const expiresAt = localStorage.getItem('expiresAt');
			if (!userId || !expiresAt) {
				goto("/login");
				throw new Error(`Login session expires`);
			}

			const currentTime = new Date().getTime();
			if (currentTime > parseInt(expiresAt)) {
				goto("/login");
				throw new Error(`Login session expires`);
			}

			await userHandler.getUser(userId);
			user = $userStore.currentUser;
		} catch (e) {
			clearCredentials();
			console.error((e as Error).message);
			goto("/login");
		}
	}

	userStore.subscribe((store) => {
		user = store?.currentUser;
		allergies = store?.currentUser?.allergies ?? [];

		console.log("User store has been updated");
	});

	function clearCredentials() {
		localStorage.removeItem('authToken');
		localStorage.removeItem('authenticated');
		localStorage.removeItem('userId');
		localStorage.removeItem('refreshToken');
		localStorage.removeItem('expiresIn');
		document.cookie = 'authToken=; path=/; Secure; HttpOnly; expires=Thu, 01 Jan 1970 00:00:00 GMT';
	}

	async function handleAddAllergy() {
		if (newAllergy.trim() === '') {
			alert('Please enter a valid allergy');
			return;
		}

		allergies = [...allergies, newAllergy.trim()];
		newAllergy = '';

		try {
			await updateUser();
		} catch (e) {
			console.error((e as Error).message);
		}
	}

	async function handleRemoveAllergy(allergy: string) {
		allergies = allergies.filter((a) => a != allergy);
		try {
			await updateUser();
		} catch (e) {
			console.error((e as Error));
		}
	}

	async function updateUser() {
		try {
			if (!userId) throw new Error('UserId not found');
			if (!user) throw new Error('User data not found');
			
			user.allergies = allergies;
			const updatedUser = {
				...user,
				allergies: allergies,
				user_id: userId
			};
			await userHandler.updateUserRecipes(updatedUser);
			fetchUserInfo();
		} catch (e) {
			alert((e as Error).message);
		}
	}
</script>

{#if authenticated && user}
	<div class="flex flex-wrap items-center justify-between rounded-full py-4">
		<div class="font-sans text-3xl font-bold text-teal-400">
			Hello {user.username}!
		</div>
		<div>
			<a href="/" class="text-teal-400">Home</a> |
			<a href="/user" class="text-teal-400">User</a>
		</div>
	</div>

	<!-- Allergies -->
	<div class="flex flex-col space-y-3 mt-6">
		<h2 class="my-2 font-sans text-xl font-semibold text-teal-400 ">Allergies</h2>
		<div class="flex items-center gap-2">
			<input
				type="text"
				bind:value={newAllergy}
				class="rounded-2xl border border-teal-300 px-2 py-1"
				placeholder="Enter new allergy"
			/>
			<Button
				class="rounded-full bg-teal-300 px-3 py-1 font-sans text-lg font-semibold text-teal-900 hover:bg-teal-400 hover:text-white hover:outline hover:outline-teal-400 whitespace-nowrap"
				onclick={handleAddAllergy}
			>
				Add allergy
			</Button>
		</div>
	</div>
	<div class="flex flex-wrap justify-between gap-4">
		{#each user.allergies as allergy, i}
			<div
				class="my-4 gap-4 rounded-2xl bg-white p-2 text-teal-600 outline outline-teal-300 hover:bg-white hover:text-teal-600 focus:outline-none"
			>
				{allergy}
				<Button
					on:click={async () => await handleRemoveAllergy(allergy)}
					class="ml-2 bg-white p-0  text-teal-600 hover:bg-white hover:text-teal-600 focus:outline-none"
				>
					x
				</Button>
			</div>
		{/each}
	</div>

	<!-- Favorite Recipes -->
	<p class="my-2 font-sans text-xl font-semibold text-teal-400">Favorite recipes</p>
	<RecipeList />
{:else}
	<!-- Show login prompt if not authenticated -->
	<div class="flex h-screen flex-col items-center justify-center">
		<p class="text-xl font-semibold text-teal-600">Please login first</p>
		<Button
			on:click={() => goto('/login')}
			class="mt-4 rounded bg-teal-600 px-4 py-2 text-white hover:bg-teal-400"
		>
			Go to Login
		</Button>
	</div>
{/if}
