<script lang="ts">
	import { categories } from '$lib/stores/ingredientStore';
	import { recipeHandler } from '$lib/stores/recipeStore';
	import { customStyles } from '$src/custom';
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
	<div class="flex flex-wrap justify-center gap-3">
		{#each $categories as category, i}
		<Button class={customStyles.categoryBtn} onclick={() => handleCategoryClick(category)} aria-label="selection button">
				<img src="/{category}.png" alt="{category}">
		</Button>
		{/each}
	</div>
</div>
