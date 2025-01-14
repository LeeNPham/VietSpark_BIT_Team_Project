<script>
	import Category from './components/Category.svelte';
	import IngredientInput from './components/IngredientInput.svelte';
	import RecipeList from './recipe/RecipeList.svelte';
	let name = "Beautiful"


</script>

<div class="py-4 flex items-center rounded-full justify-between flex-wrap">
	<div class="font-bold font-sans text-3xl text-indigo-800">Hello {name}</div>
	<div>
		<a href="/hong-prototype" class="text-indigo-700">Home</a> |
		<a href="/hong-prototype/user" class="text-indigo-700">User</a>
	</div>
</div>
<!-- Categories -->
<Category />

<!-- Ingredient input -->
<IngredientInput />


<!-- History -->
<RecipeList />