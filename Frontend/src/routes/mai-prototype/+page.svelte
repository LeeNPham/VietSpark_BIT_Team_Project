<script>
    import { Button } from 'flowbite-svelte';
	import RecipeList from '$lib/components/RecipeList.svelte';
	import { goto } from '$app/navigation';

    let authenticated = true;
    let user = { username: "JohnDoe", allergies: ["Peanuts", "Shellfish"] };
    let newAllergy = "";

    function handleAddAllergy() {
        if (newAllergy.trim() !== "") {
            user.allergies = [...user.allergies, newAllergy];
            newAllergy = "";
        }
    }

    async function handleRemoveAllergy(allergyToRemove) {
        user.allergies = user.allergies.filter(allergy => allergy !== allergyToRemove);
    }
</script>

{#if authenticated && user}



	<!-- Allergies -->
	<div class="flex flex-col space-y-3 mt-6">
		<p class={customStyles.userP}>Allergies</p>
		<div class="flex items-center gap-2">
			<input
				type="text"
				bind:value={newAllergy}
				class=
				placeholder="Enter new allergy"
			/>
			<Button
				class=
				onclick={handleAddAllergy}
			>
				Add allergy
			</Button>
		</div>
	</div>
	<div class="flex flex-wrap gap-4">
		{#each user.allergies as allergy, i}
			<div
				class=""
			>
				{allergy}
				<Button
					on:click={async () => await handleRemoveAllergy(allergy)}
					class=""
				>
					x
				</Button>
			</div>
		{/each}
	</div>

	<!-- Favorite Recipes -->
	<p class=>Favorite recipes</p>
	<RecipeList />
{:else}
	<!-- Show login prompt if not authenticated -->
	<div class="flex h-screen flex-col items-center justify-center">
		<p class={customStyles.userP}>Please Login First</p>
		<Button
			on:click={() => goto('/login')}
			class=
		>
			Go to Login
		</Button>
	</div>
{/if}
