<script>
	import Category from '$lib/components/Category.svelte';
	import IngredientInput from '$lib/components/IngredientInput.svelte';
	import RecipeList from '$lib/components/RecipeList.svelte';
	import {AccordionItem, Accordion} from 'flowbite-svelte';
	let name = "Beautiful"


</script>


<nav class="flex flex-col justify-center">
	<div class="text-xl sm:text-xl md:2xl lg:text-4xl text-secondary-forest">Hello, {name}</div>
	<Accordion flush class="outline-secondary-green">
		<AccordionItem>
		<span slot="header" class="text-lg sm:text-lg md:text-xl lg:text-2xl font-semibold text-secondary-forest "><br> Menu </span>
		<div class="flex flex-col">
			<a href="/hong-prototype/home" class="text-secondary-forest hover:text-primary-forest">Home</a>
			<a href="/hong-prototype/user" class="text-secondary-forest hover:text-primary-forest">User</a>
		</div>
		</AccordionItem>
	</Accordion>
</nav>
<div class="flex justify-center pt-3">
	<img src="/home.jpg" class="w-1/3 sm:w-1/3 md:w-1/3 lg:w-1/4" alt="A cartoon of a Black, woman chef making cupcakes in the kitchen.">
</div>
<!-- Categories -->
<Category />

<!-- Ingredient input -->
<IngredientInput />

<!-- Recipe -->
<RecipeList />