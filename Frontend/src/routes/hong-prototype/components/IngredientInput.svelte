<script>
    import { Button, Input } from "flowbite-svelte";
	import { ingredients, ingredientHandler } from "../stores/recipeStore";
	
	let newIngredient = "";
    function findRecipe() {
        console.log("Finding recipe");

    }
    const addSearchableIngredient = async() => {
        await ingredientHandler.addIngredient(newIngredient.trim().split(' '));
    }
    $: if (newIngredient) {
        console.log(newIngredient)
    }

    ingredients.subscribe((ingredient) => {
        console.log(ingredient);
    });

</script>

<div>
    <p class="font-semibold font-sans text-xl text-indigo-500 my-2">What do you want to cook today ?</p>
    <div class="flex items-center gap-2 mb-4">
        <Input 
            type="text"
            bind:value={newIngredient}
            on:submit={addSearchableIngredient}
            placeholder="Put your ingredients here"
            class="px-3 py-1 border rounded-full flex-grow font-sans"
        />
        <Button on:click={findRecipe} class="bg-indigo-300 text-indigo-900 px-3 py-1 rounded-full hover:bg-indigo-700 hover:text-indigo-300 font-semibold font-sans">Search</Button>
    </div>
    <div class="flex flex-wrap gap-2 mb-4">
        {#each $ingredients as ingredient, i}
            <div class="flex items-center bg-indigo-300 text-indigo-900 px-3 py-1 rounded-full h-10 font-semibold font-sans">
                {ingredient}
                <Button on:click={() => ingredientHandler.removeIngredient(i)} 
                    class="ml-2 bg-indigo-300 text-indigo-900 hover:text-indigo-900 hover:bg-indigo-300 font-semibold font-sans">
                    x
                </Button>
            </div>
        {/each}
    </div>
</div>