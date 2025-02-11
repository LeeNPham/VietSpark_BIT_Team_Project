<script lang="ts">
	import { Button } from 'flowbite-svelte';
	import RecipeList from '$lib/components/RecipeList.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import type { UserDTO } from '$lib/types';
	import { userHandler, userStore } from '$lib/stores/userStore';
	import { Navbar, NavBrand, NavLi, NavUl, NavHamburger } from 'flowbite-svelte';
    import { customStyles } from '$src/custom';


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
	<Navbar class={customStyles.navBar}>
		<NavBrand  class="font-sans text-3xl  text-secondary-green">
			Hello, {user.username}!
		</NavBrand>
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
	<!-- Allergies -->
	<div class="flex flex-col space-y-3 mt-6">
		<p class={customStyles.userP}>Allergies</p>
		<div class="flex items-center gap-2">
			<input
				type="text"
				bind:value={newAllergy}
				class={customStyles.input}
				placeholder="Enter new allergy"
			/>
			<Button
				class="mb-3  py-2 font-sans text-lg font-semibold text-white rounded-full bg-secondary-forest  hover:bg-secondary-blue hover:text-black hover:outline hover:outline-secondary-forest whitespace-nowrap"
				onclick={handleAddAllergy}
			>
				Add allergy
			</Button>
		</div>
	</div>
	<div class="flex flex-wrap gap-4">
		{#each user.allergies as allergy, i}
			<div
				class="gap-4 rounded-2xl bg-secondary-green p-2 text-white outline outline-secondary-forest hover:bg-secondary-blue hover:text-black focus:outline-none"
			>
				{allergy}
				<Button
					on:click={async () => await handleRemoveAllergy(allergy)}
					class="ml-2 p-0  text-black bg-transparent hover:bg-secondary-blue hover:text-black focus:outline-none"
				>
					x
				</Button>
			</div>
		{/each}
	</div>

	<!-- Favorite Recipes -->
	<p class={customStyles.userP}>Favorite recipes</p>
	<RecipeList />
{:else}
	<!-- Show login prompt if not authenticated -->
	<div class="flex h-screen flex-col items-center justify-center">
		<p class={customStyles.userP}>Please Login First</p>
		<Button
			on:click={() => goto('/login')}
			class={customStyles.button}
		>
			Go to Login
		</Button>
	</div>
{/if}
