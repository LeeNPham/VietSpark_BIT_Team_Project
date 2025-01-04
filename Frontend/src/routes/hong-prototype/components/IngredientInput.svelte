<script>
    import { Button, Input } from "flowbite-svelte";
    let { ingredients=[] } = $props();
	

	let newIngredient = "";

    function addIngredient() { 
        if (newIngredient.trim()) {
            ingredients = [...ingredients, newIngredient];
            newIngredient = ""
        }
    }

    function removeIngredient(index) {
        ingredients.slice(index, 1);
    }
</script>

<div>
    <div class="flex flex-wrap gap-2 mb-4">
        {#each ingredients as ingredient, i}
            <div class="flex items-center bg-blue-300 text-blue-900 px-3 py-1 rounded-full h-10 font-semibold font-sans">
                {ingredient}
                <Button on:click={() => removeIngredient(i)} 
                    class="ml-2 bg-blue-300 text-blue-900 hover:text-blue-300 hover:bg-blue-700 font-semibold font-sans">
                    x
                </Button>
            </div>
        {/each}
    </div>

    <div class="flex items-center gap-2 mb-4">
        <Input 
            type="text"
            bind:value={newIngredient}
            on:keydown={(event) => {
                if(event.key === "Enter") {
                    addIngredient();
                    newIngredient = ""
                }
            }}
            placeholder="Add new ingredient"
            class="px-3 py-1 border rounded-full flex-grow font-sans"
        />
        <Button on:click={addIngredient} class="bg-blue-300 text-blue-900 px-3 py-1 rounded-full hover:bg-blue-700 hover:text-blue-300 font-semibold font-sans">Add</Button>
    </div>
</div>