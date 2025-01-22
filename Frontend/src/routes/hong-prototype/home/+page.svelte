<script>
	import Category from '../components/Category.svelte';
	import IngredientInput from '../components/IngredientInput.svelte';
	import RecipeList from '../recipe/RecipeList.svelte';
	let name = "Beautiful"


</script>
<div>
	<img src="/home.jpg" class="w-1/4 h-auto mx-auto" alt="Design by stories / Freepik">
</div>
<div class="py-4 flex items-center rounded-full justify-between flex-wrap">
	
	<div class="font-sans text-3xl font-extrabold text-teal-600">Hello {name}</div>
	<div>
		<a href="/hong-prototype/home" class="text-teal-600 font-semibold">Home</a> |
		<a href="/hong-prototype/user" class="text-teal-600 font-semibold">User</a> |
		<a href="/hong-prototype/login" class="text-teal-600 font-semibold">Login</a>
	</div>
</div>
<!-- Categories -->
<Category />

<!-- Ingredient input -->
<IngredientInput />


<!-- Recipe -->
<RecipeList />