<script lang="ts">
	import { categories } from '$lib/stores/ingredientStore';
	import { recipeHandler } from '$lib/stores/recipeStore';
	import { Button } from 'flowbite-svelte';


	async function handleCategoryClick(category: string) {
		try {
			const res = await recipeHandler.searchRecipesGPT(category);
		} catch (e) {
			console.error((e as Error).message);
		}

	}
</script>

<div class="flex flex-col p-3 sm:p-3 md:p-5 lg:p-9">
	<h1
		class="pb-4 font-sans text-lg font-bold text-black sm:pb-4 sm:text-lg md:pb-9 md:text-2xl lg:pb-9 lg:text-5xl"
	>
		Category
	</h1>
	<div class="flex flex-wrap justify-center gap-3">
		{#each $categories as category, i}
			<Button
				class="bg-primary-green hover:bg-secondary-blue outline-secondary-green rounded-2xl text-xs  text-black outline sm:text-xs md:text-2xl lg:text-3xl"
				onclick={() => handleCategoryClick(category)}
			>
				{category}
			</Button>
		{/each}
	</div>
</div>
