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

	let userName: string = '';
	let email: string = '';
	let phoneNumber: string = '';
	let allergies: string[] = ['Test'];
	let authenticated = false;
	let newAllergy = '';
	let myRecipes: string[] = [];
	let showFavorites = true;

	async function fetchUserInfo() {
		try {
			authenticated = localStorage.getItem('authenticated') == 'true';

			if (!authenticated) {
				throw new Error('User is not authentiated');
			}

			userId = localStorage.getItem('userId');
			const expiresAt = localStorage.getItem('expiresAt');
			if (!userId || !expiresAt) {
				throw new Error(`Login session expires`);
			}

			if (Date.now() > parseInt(expiresAt)) {
				throw new Error(`Login session expires`);
			}

			await userHandler.getUser(userId);
			authenticated = true;
			console.log('User is authenticated', user);
		} catch (e) {
			console.error((e as Error).message);
			clearCredentials();
			goto('/login');
		}
	}

	userStore.subscribe((store) => {
		if (authenticated && store?.currentUser) {
			user = store?.currentUser ?? '';
			userName = user?.userName ?? '';
			email = user?.userEmail ?? '';
			phoneNumber = user?.phoneNumber ?? '';
			allergies = user?.allergies ?? [];
			myRecipes = user?.recipes ?? [];
		}
	});

	function clearCredentials() {
		localStorage.clear();

		document.cookie = 'authToken=; path=/; Secure; HttpOnly; expires=Thu, 01 Jan 1970 00:00:00 GMT';
	}

	function handlerSignOut() {
		userHandler.signOut();
	}

	async function handleAddAllergy() {
		if (newAllergy.trim() === '') {
			alert('Please enter a valid allergy');
			return;
		}

		allergies = [...allergies, newAllergy.trim()];
		newAllergy = '';
	}

	async function handleRemoveAllergy(allergy: string) {
		allergies = allergies.filter((a) => a != allergy);
		try {
			await updateUser();
		} catch (e) {
			console.error(e as Error);
		}
	}

	async function updateUser() {
		try {
			if (!userId) throw new Error('UserId not found');
			if (!user) throw new Error('User data not found');

			const updatedUser = {
				...user,
				allergies: allergies,
				user_id: userId
			};
			if (userName.trim() !== user.userName.trim()) updatedUser.userName = userName;
			if (email.trim() !== user.userEmail.trim()) updatedUser.userEmail = email;
			if (phoneNumber.trim() !== user.phoneNumber.trim()) updatedUser.phoneNumber = phoneNumber;

			await userHandler.updateUserDetail(updatedUser);
			fetchUserInfo();
		} catch (e) {
			alert((e as Error).message);
		}
	}

	function cancelUpdateUser() {
		userName = user?.userName ?? '';
		email = user?.userEmail ?? '';
		phoneNumber = user?.phoneNumber ?? '';
		allergies = user?.allergies ?? [];
		myRecipes = user?.recipes ?? [];
		goto('/');
	}
	onMount(fetchUserInfo);
</script>

{#if authenticated && user}
	<Navbar class={customStyles.navBar}>
		<NavBrand class="text-secondary-green font-sans  text-3xl">
			Hello, {user.userName}!
		</NavBrand>
		<NavHamburger />
		<NavUl>
			<NavLi href="/" class={customStyles.aTag}>Home</NavLi>
			<NavLi href="/user" class={customStyles.aTag}>User</NavLi>
			<NavLi href="/" class={customStyles.aTag} on:click={handlerSignOut}>Sign out</NavLi>
		</NavUl>
	</Navbar>
	<div class="mt-6 flex gap-3">
		<div class="flex flex-1 flex-col space-y-3">
			<p class={customStyles.userP}>Name</p>
			<input type="text" bind:value={userName} class={customStyles.input} />
		</div>
		<div class="flex flex-1 flex-col space-y-3">
			<p class={customStyles.userP}>Email</p>
			<input type="email" bind:value={email} class={customStyles.input} />
		</div>
	</div>

	<div class="mt-6 flex flex-col space-y-3">
		<p class={customStyles.userP}>Phone number</p>
		<input type="text" bind:value={phoneNumber} class={customStyles.input} />
	</div>

	<!-- Allergies -->
	<div class="mt-6 flex flex-col space-y-3">
		<p class={customStyles.userP}>Allergies</p>
		<div class="flex items-center gap-2">
			<input
				type="text"
				bind:value={newAllergy}
				class={customStyles.input}
				placeholder="Enter new allergy"
			/>
			<Button
				class="bg-primary-orange  outline-secondary-green rounded-2xl text-lg text-black outline"
				onclick={handleAddAllergy}
			>
				+
			</Button>
		</div>
	</div>
	<div class="flex flex-wrap gap-4">
		{#each allergies as allergy, i}
			<div
				class="bg-secondary-green outline-secondary-forest hover:bg-secondary-blue gap-4 rounded-2xl p-2 text-white outline hover:text-black focus:outline-none"
			>
				{allergy}
				<Button
					on:click={async () => await handleRemoveAllergy(allergy)}
					class="hover:bg-secondary-blue ml-2  bg-transparent p-0 text-black hover:text-black focus:outline-none"
				>
					x
				</Button>
			</div>
		{/each}
	</div>

	<!-- Favorite Recipes -->
	<p class={customStyles.userP}>Favorite Recipes</p>
	<RecipeList {myRecipes} {showFavorites}/>
	<div class="mt-6 flex justify-center gap-4">
		<!-- Cancel Button -->
		<Button
			class="bg-primary-gray rounded-2xl text-lg outline  outline-secondary-green text-gray-800 "
			on:click={cancelUpdateUser}
		>
			Close
		</Button>

		<!-- Save Changes Button -->
		<Button
			class="bg-primary-orange  outline-secondary-green rounded-2xl text-lg text-black outline"
			on:click={updateUser}
		>
			Save Changes
		</Button>
	</div>
{:else}
	<!-- Show login prompt if not authenticated -->
	<div class="flex h-screen flex-col items-center justify-center">
		<p class={customStyles.userP}>Please Login First</p>
		<Button on:click={() => goto('/login')} class={customStyles.button}>Go to Login</Button>
	</div>
{/if}
