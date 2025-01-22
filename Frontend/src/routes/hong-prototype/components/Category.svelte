<script>
	import { categories } from '../stores/ingredientStore';
	import { Button } from 'flowbite-svelte';
</script>

<div>
	<p class="my-2 font-sans text-xl font-bold">Category</p>
	<div class="flex flex-wrap justify-center gap-4">
		{#each $categories as category, i}
			<Button
				class="my-4 gap-4 text-white bg-blue-500 outline-none outline-white  hover:bg-blue-400 hover:text-white focus:outline-none"
			>
				{category}
			</Button>
		{/each}
	</div>
</div>
