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

<div class="flex flex-col justify-normal p-9">
    <h1 class="mb-4 text-2xl ">What do you want to cook today?</h1>
    <div class="flex gap-3">
        <Input
            aria-label="ingredients-input-box"
            type="text"
            bind:value={newIngredient}
            on:keydown={(event) => {
                if(event.key === "Enter") {
                    addSearchableIngredient();
                    newIngredient = ""
                }
            }}
            placeholder="Add ingredients here: Chicken, Mint, Carrots (max. 5)"
            class="text-lg rounded-2xl outline outline-secondary-green"
        />
        <Button on:click={findRecipe} class="text-lg  text-black bg-primary-orange rounded-2xl outline outline-secondary-green">Search</Button>
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