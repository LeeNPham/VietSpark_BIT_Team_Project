<script>
	import { Button, Input } from 'flowbite-svelte';
	import { recipeStore, recipeHandler } from '../stores/recipeStore';
	import { onMount } from 'svelte';
	import Modal from '../components/Modal.svelte';

	let recipes = [];
	let showModal = false;
	let newRecipeName = '';
	let newIngredients = [];
	let ingredientRows = [{ name: '', quantity: '' }];
	let newInstructions = [''];
	let newServings = 0;
	let newCalories = 0;
	let newDuration = 0;
	let newImageLink = '';

	recipeStore.subscribe((recipeStore) => {
		recipes = recipeStore?.recipes;
	});

	onMount(async () => {
		await recipeHandler.getRecipes();
	});

	function toggleModal() {
		showModal = !showModal;
	}
	// Ingredients
	function addIngredientRow() {
		ingredientRows = [...ingredientRows, { name: '', quantity: '' }];
	}
	function removeIngredientRow(index) {
		ingredientRows.splice(index, 1);
		ingredientRows = [...ingredientRows];
	}

	function handleIngredientChange(index, field, value) {
		ingredientRows[index][field] = value;
	}

	// Instructions
	function addInstruction() {
		newInstructions = [...newInstructions, ''];
	}
	function removeInstruction(index) {
		newInstructions.splice(index, 1);
		newInstructions = [...newInstructions];
	}
	function handleInstructionChange(index, value) {
		newInstructions[index] = value;
	}

	// Final submission
	async function handleSubmit() {
		newIngredients = ingredientRows.filter((row) => row.name && row.quantity);

		if (newRecipeName && newIngredients.length > 0 && newInstructions.length > 0) {
			const newRecipe = {
				name: newRecipeName,
				ingredients: newIngredients,
				instructions: newInstructions,
				servings: newServings,
				calories: newCalories,
				duration: newDuration,
				image: newImageLink ? newImageLink : 'https://cdn.britannica.com/36/123536-050-95CB0C6E/Variety-fruits-vegetables.jpg',
				numIngredients: newIngredients.length,
			};
			console.log('Add new recipe');
			try {
				await recipeHandler.addRecipe(newRecipe);
				await recipeHandler.getRecipes();
				toggleModal();
			} catch (error) {
				alert('Failed to create the recipe');
			}
		} else {
			alert('Please enter recipe detail');
		}
	}
</script>

<div class="flex items-center justify-between">
	<h2 class="font-sans text-xl font-semibold text-indigo-500 my-2">Recipes</h2>
	<Button
		class="rounded-full bg-indigo-300 px-3 py-1 font-sans font-semibold text-indigo-900 hover:bg-indigo-700 hover:text-indigo-300"
		onclick={toggleModal}>Add recipe</Button
	>
</div>
<div class="mb-4 gap-2">
	{#each recipes as item, i}
		<a class="mb-4 items-center gap-4 rounded-lg p-4" href="/hong-prototype/recipe">
			<div class="flex items-center gap-4">
				<img src={item.image} class="h-20 w-20 rounded-lg object-cover" alt="Recipe image" />
				<div>
					<p>{item.name}</p>
					<div class="space-x-2 text-sm font-medium text-indigo-700">
						<span>{item.duration} Min.</span>
						<span>*</span>
						<span>{item.numIngredients} ingredients</span>
					</div>
					<h3 class="mt-1 font-semibold text-indigo-500">{item.description}</h3>
				</div>
			</div>

			
		</a>
	{/each}
</div>

{#if showModal}
	<Modal onclose={toggleModal}>
		<!-- Title -->
		<div class="mb-10 space-y-4">
			<label for="recipe-name" class="mb-1 block font-semibold">Recipe name</label>
			<Input
				id="recipe-name"
				type="text"
				bind:value={newRecipeName}
				placeholder="Enter your recipe name"
				class="flex-grow rounded-full border px-3 py-1 font-sans"
			/>
		</div>
		<!-- Image -->
		<div class="mb-10 space-y-4">
			<label for="recipe-image" class="mb-1 block font-semibold">Recipe image</label>
			<Input
				id="recipe-image"
				type="text"
				bind:value={newImageLink}
				placeholder="Paste your image link"
				class="flex-grow rounded-full border px-3 py-1 font-sans"
			/>
		</div>
		<!-- Ingredients -->
		<div class="mb-10 space-y-4">
			<div class="flex items-center justify-between gap-4">
				<label for="recipe-ingredients" class="mb-1 block font-semibold">Recipe ingredients</label>
				<Button
					onclick={addIngredientRow}
					class="rounded-full bg-white px-3 py-1 text-indigo-600 outline outline-indigo-300 hover:bg-white hover:text-indigo-600 focus:outline-none justify-end"
					>Add ingredient</Button
				>
			</div>
			<div class="space-y-3">
				{#each ingredientRows as ingredient, index}
					<div class="intems-center flex gap-2">
						<Input
							type="text"
							bind:value={ingredient.name}
							oninput={(e) => handleIngredientChange(index, 'name', e?.target?.value)}
							placeholder="Ingredient"
							class="flex-grow rounded-full border px-3 py-1 font-sans"
						/>
						<Input
							type="text"
							bind:value={ingredient.quantity}
							placeholder="Quantity (eg 300g)"
							oninput={(e) => handleIngredientChange(index, 'quantity', e?.target?.value)}
							class="flex-grow rounded-full border px-3 py-1 font-sans"
						/>
						<Button
							onclick={removeIngredientRow}
							class="rounded-full bg-white px-3 py-1 text-indigo-600 outline outline-indigo-300 hover:bg-white hover:text-indigo-600 focus:outline-none justify-end"
							>Remove</Button
						>
					</div>
				{/each}
			</div>
		</div>
		<!-- Calories, duration, servings -->
		<div class="flex items-center gap-4 mb-10">
			<div>
				<label for="duration" class="mb-1 block font-semibold">Duration (minutes)</label>
				<Input
					id="duration"
					type="text"
					bind:value={newDuration}
					placeholder="Enter duration (eg. 60)"
					class="flex-grow rounded-full border px-3 py-1 font-sans"
				/>
			</div>
			<div>
				<label for="servings" class="mb-1 block font-semibold">Servings</label>
				<Input
					id="servings"
					type="text"
					bind:value={newServings}
					placeholder="Enter serving"
					class="flex-grow rounded-full border px-3 py-1 font-sans"
				/>
			</div>
			<div>
				<label for="calories" class="mb-1 block font-semibold">Calories</label>
				<Input
					id="calories"
					type="text"
					bind:value={newCalories}
					placeholder="Enter calories"
					class="flex-grow rounded-full border px-3 py-1 font-sans"
				/>
			</div>
		</div>
		<!-- Instruction -->
		<div class="mb-10 space-y-4">
			<div class="flex items-center justify-between gap-4">
				<label for="instructions" class="mb-1 block font-semibold">Instructions</label>
				<Button
					onclick={addInstruction}
					class="rounded-full bg-white px-3 py-1 text-indigo-600 outline outline-indigo-300 hover:bg-white hover:text-indigo-600 focus:outline-none justify-end"
					>Add instruction</Button
				>
			</div>
			<div class="space-y-3">
				{#each newInstructions as instruction, index}
					<div class="flex items-center gap-2">
						<Input
						type="text"
						bind:value={instruction}
						placeholder="Put the instruction here"
						oninput={(e) => handleInstructionChange(index, e?.target?.value)}
						class="flex-grow rounded-full border px-3 py-1 font-sans"
					/>
					<Button
						onclick={removeInstruction}
						class="rounded-full bg-white px-3 py-1 text-indigo-600 outline outline-indigo-300 hover:bg-white hover:text-indigo-600 focus:outline-none justify-end"
						>Remove</Button
					>
					</div>
				{/each}
			</div>
		</div>
		<div class="flex justify-end">
			<Button
				onclick={handleSubmit}
				class="rounded-full bg-indigo-600 px-3 py-1 text-white outline outline-indigo-600 hover:bg-indigo-600 hover:text-white focus:outline-none"
				>Submit</Button
			>
		</div>
	</Modal>
{/if}
