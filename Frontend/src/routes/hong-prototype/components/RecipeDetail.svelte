<script>
	import { Button } from 'flowbite-svelte';
	let { item } = $props();
	let servings = $state(1);

	function increaseServing() {
		servings++;
	}

	function decreaseServing() {
		servings = Math.max(servings - 1, 1);
	}
</script>

<div class="min-h-screen px-4 py-6">
	<img src={item.src} alt="Recipe image" class="h-60 w-40 object-cover" />
	<!-- Servings -->
	<div class="mt-4 flex items-center justify-between">
		<Button
			class="bg-white text-blue-700 hover:bg-blue-700 hover:text-blue-100"
			on:click={decreaseServing}>-</Button
		>
		<div class="text-xl font-semibold">Servings {servings}</div>
		<Button
			class="bg-white text-blue-700 hover:bg-blue-700 hover:text-blue-100"
			on:click={increaseServing}>+</Button
		>
	</div>
	<!-- Details -->
	<div class="mt-4 rounded-lg bg-white p-4">
		{#each item.ingredients as ingredient, i}
			<div class="flex items-center justify-between border-b last:border-none py-2">
                <p>{ingredient.name}</p>
                <p>{ingredient.quantity}</p>
            </div>
		{/each}
	</div>
</div>

<style>
    .modal {
        z-index: 9999;
    }
</style>