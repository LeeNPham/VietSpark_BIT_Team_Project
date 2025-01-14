<script>
	import { Button } from "flowbite-svelte";
	import RecipeList from "../recipe/RecipeList.svelte";
    let name = "Beautiful";
	let allergies = ["Peanuts", "Shellfish", "Sumthing else", "Bad ppl"]

	let myRecipe = []
</script>
<div class="py-4 flex items-center rounded-full justify-between flex-wrap">
	<div class="font-bold font-sans text-3xl text-indigo-800">Hello {name}! Edit yourself!</div>
	<div>
		<a href="/hong-prototype" class="text-indigo-700">Home</a> |
		<a href="/hong-prototype/user" class="text-indigo-700">User</a>
	</div>
</div>

<!-- Allegies -->
<p class="font-semibold font-sans text-xl text-indigo-500 my-2">Allergies</p>
<div class="flex flex-wrap justify-center gap-4">
    {#each allergies as allergy, i}
    <Button class="my-4 gap-4 bg-white text-indigo-600 outline outline-indigo-300 hover:bg-indigo-600 hover:text-white focus:outline-none">
        {allergy}
    </Button>
    {/each}
</div>

<!-- Allegies -->
<p class="font-semibold font-sans text-xl text-indigo-500 my-2">Favorite recipes</p>
<div class="flex flex-wrap justify-center gap-4">
    <RecipeList />
</div>