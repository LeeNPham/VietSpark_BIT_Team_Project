<script>
	import { categories } from '../stores/ingredientStore';
	import { Button } from 'flowbite-svelte';
</script>

<div class="flex flex-col p-9">
	<h1 class="pb-8 font-sans text-5xl font-bold  text-black">Category</h1>
	<div class="flex flex-wrap gap-3">
		{#each $categories as category, i}
			<Button class="text-2xl text-black  bg-primary-green hover:bg-secondary-blue rounded-2xl outline outline-secondary-green">
				{category}
			</Button>
		{/each}
	</div>
</div>
