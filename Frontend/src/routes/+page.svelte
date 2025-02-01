<script>
	import Category from './components/Category.svelte';
	import IngredientInput from './components/IngredientInput.svelte';
	import RecipeList from './recipe/RecipeList.svelte';
	let name = 'Beautiful';
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<div>
	<img src="/home.jpg" class="mx-auto h-1/2 w-auto" alt="(Adobe stock) Home banner" />
</div>
<div class="flex flex-wrap items-center justify-between rounded-full py-4">
	<div class="font-sans text-3xl font-extrabold text-teal-600">Hello {name}</div>
	<div>
		<a href="/" class="font-semibold text-teal-600">Home</a> |
		<a href="/user" class="font-semibold text-teal-600">User</a>
	</div>
</div>
<!-- Categories -->
<Category />

<!-- Ingredient input -->
<IngredientInput />

<!-- Recipe -->
<RecipeList />
