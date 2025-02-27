<script lang="ts">
	import { Button } from 'flowbite-svelte';
	import RecipeList from '$lib/components/RecipeList.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import type { UserDTO } from '$lib/types';
	import { userHandler, userStore } from '$lib/stores/userStore';
	import { customStyles } from '$src/custom';
	import ChangeProfileImageModal from '$lib/components/ChangeProfileImageModal.svelte';

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
	let profileImageURL = '';
	let showProfileImageModal = false;
    let profileImagePreview: string | null = null;
	let imageRefreshed = false;

    function toggleProfileImageModal() {
        showProfileImageModal = !showProfileImageModal;
        profileImagePreview = null;
    }

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
			userId = store?.userId ?? '';
			profileImageURL = user?.profileImageURL ?? '';
		}
	});

	function clearCredentials() {
		localStorage.clear();

		document.cookie = 'authToken=; path=/; Secure; HttpOnly; expires=Thu, 01 Jan 1970 00:00:00 GMT';
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
			alert('User updated successfully');
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
		profileImageURL = user?.profileImageURL ?? '';
		goto('/');
	}

    function handleImageLoad(event: Event) {
        const img = event.target as HTMLImageElement;
        if (!imageRefreshed) {
			img.src = img.src.split('?')[0] + '?' + new Date().getTime();
			imageRefreshed = true; // Set the flag to true after refreshing the image
        }
    }

	onMount(fetchUserInfo);
</script>

{#if authenticated && user}
	<div class="flex">
		<div class="relative group">
			<button 
				class="w-20 h-20 overflow-hidden border-green-300 p-0 rounded-full"
				on:click={toggleProfileImageModal}>
				<img class="w-full h-full object-cover" src={profileImageURL} on:load={handleImageLoad} alt={profileImageURL}>
			</button>
			<div class="absolute top-1/2 left-full transform -translate-y-1/2 ml-2 bg-gray-800 text-white text-xs rounded py-1 px-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">
				Click to change Image
			</div>
		</div>
	</div>
	<ChangeProfileImageModal {toggleProfileImageModal} {showProfileImageModal}/>
	
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
	<div class="allergies-container">
		<h3>Allergies</h3>
		{#if allergies.length > 0}
			<div class="allergy-list">
				{#each allergies as allergy}
					<div class="allergy-item">
						<span class="icon">⚠️</span>
						<span>{allergy}</span>
						<button on:click={async () => await handleRemoveAllergy(allergy)} class="remove-btn">
							×
						</button>
					</div>
				{/each}
			</div>
		{:else}
			<p class="empty">No allergies listed</p>
		{/if}
	</div>
	<!-- Favorite Recipes -->
	<p class={customStyles.userP}>Favorite Recipes</p>
	<RecipeList {myRecipes} {showFavorites} />
	<div class="mt-6 flex justify-center gap-4">
		<!-- Cancel Button -->
		<Button
			class="bg-primary-gray outline-secondary-green rounded-2xl text-lg  text-gray-800 outline "
			on:click={cancelUpdateUser}
		>
			Close
		</Button>

		<!-- Save Changes Button -->
		<Button
			class="bg-primary-orange  outline-secondary-green rounded-2xl text-lg text-black outline"
			on:click={updateUser}
		>
			Save
		</Button>
	</div>
{:else}
	<!-- Show login prompt if not authenticated -->
	<div class="flex h-screen flex-col items-center justify-center">
		<p class={customStyles.userP}>Please Login First</p>
		<Button on:click={() => goto('/login')} class={customStyles.button}>Go to Login</Button>
	</div>
{/if}

<style>
	.allergy-list {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem; /* Matches your original gap-4 (~1rem) */
	}
	.allergy-item {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		background-color: #00695c; /* Deep teal, replacing light #e0f7fa */
		color: #fff; /* White text for contrast */
		padding: 0.5rem 1rem; /* Slightly larger than original p-2 */
		border-radius: 1rem; /* Matches rounded-2xl */
	}
	.icon {
		color: #ef5350; /* Deeper red for warning */
	}
	.remove-btn {
		background: transparent;
		border: none;
		color: #fff; /* White to match text */
		font-size: 1.25rem; /* Larger for visibility */
		cursor: pointer;
		padding: 0 0.5rem;
		transition: color 0.2s;
	}
	.remove-btn:hover {
		color: #ef5350; /* Deep red on hover, richer than #d32f2f */
	}
	.empty {
		color: #b0bec5; /* Lighter gray for dark theme; adjust if needed */
		font-style: italic;
	}
</style>
