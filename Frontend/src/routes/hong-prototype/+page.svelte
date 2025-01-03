<script>
	import { Button } from 'flowbite-svelte';
	import IngredientInput from './components/IngredientInput.svelte';
	
	let ingredients = []
	function addIngredient(newIngredient) {
		ingredients = [...ingredients, newIngredient];
	}
</script>

<!-- <div class="p-4 bg-blue-100 flex items-center rounded-full justify-between flex flex-wrap"> -->
<div class="p-4 flex items-center rounded-full justify-between flex flex-wrap">
	<div class="font-semibold font-sans text-3xl w-3/4">Not sure what to cook tonight ?</div>
	<Button class="rounded-full outline outline-blue-700 bg-blue-100 text-blue-700 hover:bg-blue-700 hover:text-blue-100 px-6 py-3 text-sm font-semibold font-sans">Settings</Button>
</div>
<br/>

<IngredientInput {ingredients} on:add={(e) => addIngredient(e.detail)}/>


<!-- History -->