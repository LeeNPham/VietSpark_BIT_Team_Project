<script>
	import { categories } from '../stores/recipeStore';
	import { Button } from 'flowbite-svelte';
</script>

<div>
	<p class="my-2 font-sans text-xl font-semibold text-indigo-500">Category</p>
	<div class="flex flex-wrap justify-center gap-4">
		{#each $categories as category, i}
			<Button
				class="my-4 gap-4 bg-white text-indigo-600 outline outline-indigo-300 hover:bg-indigo-600 hover:text-white focus:outline-none"
			>
				{category}
			</Button>
		{/each}
	</div>
</div>
