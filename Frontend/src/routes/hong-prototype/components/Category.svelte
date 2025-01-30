<script>
	import { categories } from '../stores/ingredientStore';
	import { Button } from 'flowbite-svelte';
</script>

<div class="flex flex-col p-3 sm:p-3 md:p-5 lg:p-9">
	<h1 class="pb-4 sm:pb-4 md:pb-9 lg:pb-9 font-sans text-lg sm:text-lg md:text-2xl lg:text-5xl font-bold  text-black">Category</h1>
	<div class="flex flex-wrap justify-center gap-3">
		{#each $categories as category, i}
			<Button class="text-xs sm:text-xs md:text-2xl lg:text-3xl text-black  bg-primary-green hover:bg-secondary-blue rounded-2xl outline outline-secondary-green">
				{category}
			</Button>
		{/each}
	</div>
</div>
