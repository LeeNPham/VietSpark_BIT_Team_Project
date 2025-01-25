<script>
	import Category from '../components/Category.svelte';
	import IngredientInput from '../components/IngredientInput.svelte';
	import RecipeList from '../recipe/RecipeList.svelte';
	let name = "Beautiful"


</script>
<nav class="flex justify-between items-center p-9 ">
	<div class="text-4xl text-secondary-forest">Hello, {name}</div>
	<div class="flex space-x-4">
		<a href="/hong-prototype/home" class="px-4 py-2 text-2xl text-background-white rounded-2xl bg-secondary-forest outline outline-secondary-green">Home</a>
		<a href="/hong-prototype/user" class="px-4 py-2 text-2xl text-background-white rounded-2xl bg-secondary-forest outline outline-secondary-green">User</a>
	</div>
</nav>
<div>
	<img src="/home.jpg" class="w-1/4 h-auto mx-auto" alt="A cartoon of a Black, woman chef making cupcakes in the kitchen.">
</div>
<!-- Categories -->
<Category />

<!-- Ingredient input -->
<IngredientInput />

<!-- Recipe -->
<RecipeList />