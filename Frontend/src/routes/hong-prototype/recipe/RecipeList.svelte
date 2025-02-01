<script lang="ts">
	import { Button, Input } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import Modal from '../components/Modal.svelte';
	import type { Recipe } from '../types';

	const API_URL = import.meta.env.VITE_API_URL;

	let recipes: Recipe[] | [] = [];
	let showModal = false;
	let newRecipeName = '';
	let newIngredients = [];
	let ingredientRows = [{ name: '', amount: '' }];
	let newInstructions = [''];
	let newServings = 0;
	let newCalories = 0;
	let newDuration = 0;
	let newImageLink = '';

	async function fetchRecipes() {
		try {
			const res = await fetch(`${API_URL}/recipes`);
			if (!res.ok) throw new Error('Failed to fetch recipes');
			recipes = await res.json();
		} catch (e) {
			console.error(e);
		}
	}

	onMount(fetchRecipes);

	function toggleModal() {
		showModal = !showModal;
	}
	// Ingredients
	function addIngredientRow() {
		ingredientRows = [...ingredientRows, { name: '', amount: '' }];
	}
	function removeIngredientRow(index: number) {
		ingredientRows.splice(index, 1);
		ingredientRows = [...ingredientRows];
	}

	function handleIngredientChange(index: number, field: 'name' | 'amount', value: string) {
		ingredientRows[index][field] = value;
	}

	// Instructions
	function addInstruction() {
		newInstructions = [...newInstructions, ''];
	}
	function removeInstruction(index: number) {
		newInstructions.splice(index, 1);
		newInstructions = [...newInstructions];
	}
	function handleInstructionChange(index: number, value: string) {
		newInstructions[index] = value;
	}

	// Final submission
	async function handleSubmit() {
		newIngredients = ingredientRows.filter((row) => row.name && row.amount);

		if (newRecipeName && newIngredients.length > 0 && newInstructions.length > 0) {
			const newRecipe = {
				recipe: {
					name: newRecipeName,
					instructions: newInstructions,
					servings: newServings,
					calories: newCalories,
					duration: newDuration,
					img_url: newImageLink
						? newImageLink
						: 'https://cdn.britannica.com/36/123536-050-95CB0C6E/Variety-fruits-vegetables.jpg',
					ingredients: newIngredients,
					numIngredients: newIngredients.length
				}
			};
			console.log('Add new recipe');
			try {
				await fetch(`${API_URL}/recipes`, {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify(newRecipe)
				});
				await fetchRecipes();
				toggleModal();
			} catch (error) {
				alert('Failed to create the recipe');
			}
		} else {
			alert('Please enter recipe detail');
		}
	}
</script>

<div class="flex justify-between items-center p-1 sm:p-1 s md:p-5 lg:p-9">
	<h2 class="text-base sm:text-base md:text-xl lg:text-2xl">Recipes or History </h2>
	<Button
		class="text-sm sm:text-sm md:text-lg lg:text-xl text-black  bg-primary-green hover:bg-secondary-blue rounded-2xl outline outline-secondary-green"
		onclick={toggleModal}>Add recipe
	</Button>
</div>
<div class="mb-4 grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
	{#each recipes as item, i}
		<a
			class="mb-4 flex w-full items-center gap-4 rounded-lg p-4"
			href={`/hong-prototype/recipe/${item.id}`}
		>
			<div class="flex w-full items-center gap-4">
				<img src={item.img_url} class="h-20 w-20 rounded-lg object-cover" alt={item.name} />
				<div class="flex-1">
					<p>{item.name}</p>
					<div class="space-x-2 text-sm font-medium text-teal-700">
						<span>{item.time}</span>
						<span>*</span>
						<span>{item.ingredients.length} ingredients</span>
					</div>
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
					class="justify-end rounded-full bg-white px-3 py-1 text-teal-600 outline outline-teal-300 hover:bg-white hover:text-teal-600 focus:outline-none"
					>Add ingredient</Button
				>
			</div>
			<div class="space-y-3">
				{#each ingredientRows as ingredient, index}
					<div class="intems-center flex gap-2">
						<Input
							type="text"
							bind:value={ingredient.name}
							oninput={(e) =>
								handleIngredientChange(index, 'name', (e.currentTarget as HTMLInputElement).value)}
							placeholder="Ingredient"
							class="flex-grow rounded-full border px-3 py-1 font-sans"
						/>
						<Input
							type="text"
							bind:value={ingredient.amount}
							placeholder="Amount (eg 300g)"
							oninput={(e) =>
								handleIngredientChange(
									index,
									'amount',
									(e.currentTarget as HTMLInputElement).value
								)}
							class="flex-grow rounded-full border px-3 py-1 font-sans"
						/>
						<Button
							onclick={() => removeIngredientRow(index)}
							class="justify-end rounded-full bg-white px-3 py-1 text-teal-600 outline outline-teal-300 hover:bg-white hover:text-teal-600 focus:outline-none"
							>Remove</Button
						>
					</div>
				{/each}
			</div>
		</div>
		<!-- Calories, duration, servings -->
		<div class="mb-10 flex items-center gap-4">
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
					class="justify-end rounded-full bg-white px-3 py-1 text-teal-600 outline outline-teal-300 hover:bg-white hover:text-teal-600 focus:outline-none"
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
							oninput={(e) =>
								handleInstructionChange(index, (e.currentTarget as HTMLInputElement).value)}
							class="flex-grow rounded-full border px-3 py-1 font-sans"
						/>
						<Button
							onclick={() => removeInstruction(index)}
							class="justify-end rounded-full bg-white px-3 py-1 text-teal-600 outline outline-teal-300 hover:bg-white hover:text-teal-600 focus:outline-none"
							>Remove</Button
						>
					</div>
				{/each}
			</div>
		</div>
		<div class="flex justify-end">
			<Button
				onclick={handleSubmit}
				class="rounded-full bg-teal-600 px-3 py-1 text-white outline outline-teal-600 hover:bg-teal-600 hover:text-white focus:outline-none"
				>Submit</Button
			>
		</div>
	</Modal>
{/if}
