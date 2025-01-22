<script>
    import { Button, Input } from "flowbite-svelte";
	import { ingredients, ingredientHandler } from "../stores/ingredientStore";
	let newIngredient = "";
    function findRecipe() {
        console.log("Finding recipe");

    }
    const addSearchableIngredient = () => {
        if (newIngredient) {
            ingredientHandler.addIngredient(newIngredient.trim());
        }
    }

    ingredients.subscribe((ingredient) => {
        console.log(ingredient);
    });

</script>

<div>
    <p class="my-2 font-sans text-xl font-bold">What ingredients do you want to cook with ?</p>
    <div class="flex items-center gap-2 mb-4">
        <Input 
            type="text"
            bind:value={newIngredient}
            on:keydown={(event) => {
                if(event.key === "Enter") {
                    addSearchableIngredient();
                    newIngredient = ""
                }
            }}
            placeholder="Put your ingredients here"
            class="px-3 py-1 border rounded-full flex-grow font-sans focus:outline-none focus:ring-2 focus:ring-yellow-200"
        />
        <Button on:click={findRecipe} class="bg-yellow-300 text-lg text-yellow-700 px-3 py-1 rounded-full font-semibold font-sans hover:bg-yellow-400 hover:outline hover:outline-yellow-400  hover:text-white">Search</Button>
    </div>
    <div class="flex flex-wrap gap-2 mb-4">
        {#each $ingredients as ingredient, i}
            <div class="flex items-center justify-between bg-yellow-300 text-yellow-900 px-3 py-1 rounded-full h-10 font-semibold font-sans">
                {ingredient}
                <Button on:click={() => ingredientHandler.removeIngredient(i)} 
                    class="ml-2 bg-yellow-300 text-yellow-900 hover:text-yellow-900 hover:bg-yellow-300 focus:outline-none">
                    x
                </Button>
            </div>
        {/each}
    </div>
</div>