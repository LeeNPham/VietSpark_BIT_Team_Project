<script>
    import { Button } from "flowbite-svelte";
    import RecipeList from "../recipe/RecipeList.svelte";
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";

    const API_URL = import.meta.env.VITE_API_URL;

    let name = "Beautiful";
    let allergies = ["Peanuts", "Shellfish", "Sumthing else", "Bad ppl"];
    let myRecipe = [];
    let authenticated = false;

    onMount(() => {
        authenticated = localStorage.getItem("authenticated") === "true";
    });

    function goToLogin() {
        goto("/hong-prototype/login");
    }
</script>

{#if authenticated}
    <div class="py-4 flex items-center rounded-full justify-between flex-wrap">
        <div class="font-bold font-sans text-3xl text-teal-800">Hello {name}! Edit yourself!</div>
        <div>
            <a href="/hong-prototype" class="text-teal-700">Home</a> |
            <a href="/hong-prototype/user" class="text-teal-700">User</a>
        </div>
    </div>

    <!-- Allergies -->
    <p class="font-semibold font-sans text-xl text-teal-500 my-2">Allergies</p>
    <div class="flex flex-wrap justify-center gap-4">
        {#each allergies as allergy, i}
            <Button class="my-4 gap-4 bg-white text-teal-600 outline outline-teal-300 hover:bg-teal-600 hover:text-white focus:outline-none">
                {allergy}
            </Button>
        {/each}
    </div>

    <!-- Favorite Recipes -->
    <p class="font-semibold font-sans text-xl text-teal-500 my-2">Favorite recipes</p>
    <div class="flex flex-wrap justify-center gap-4">
        <RecipeList />
    </div>
{:else}
    <!-- Show login prompt if not authenticated -->
    <div class="h-screen flex flex-col items-center justify-center">
        <p class="text-xl font-semibold text-teal-600">Please login first</p>
        <Button on:click={goToLogin} class="mt-4 bg-teal-600 text-white px-4 py-2 rounded hover:bg-teal-700">
            Go to Login
        </Button>
    </div>
{/if}