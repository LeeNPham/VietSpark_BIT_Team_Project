<script>
	import { Button } from 'flowbite-svelte';
	import IngredientInput from './components/IngredientInput.svelte';
	import HistoryList from './components/HistoryList.svelte';
	
</script>

<!-- <div class="p-4 bg-blue-100 flex items-center rounded-full justify-between flex flex-wrap"> -->
<div class="p-4 flex items-center rounded-full justify-between flex flex-wrap">
	<div class="font-semibold font-sans text-3xl">Not sure what to cook tonight ?</div>
	<Button class="rounded-full outline outline-blue-700 bg-blue-100 text-blue-700 hover:bg-blue-700 hover:text-blue-100 px-6 py-3 text-sm font-semibold font-sans">Settings</Button>
</div>
<br/>

<IngredientInput />


<!-- History -->
<h2 class="font-semibold font-sans text-xl">History</h2>
<HistoryList />