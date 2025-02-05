<script lang="ts">
	import { Button, Input } from 'flowbite-svelte';
	import Modal from '../components/Modal.svelte';
	import { recipeHandler } from '$lib/stores/recipeStore';
	import { imageHandler } from '$lib/stores/imageStore';

	export let showModal: boolean;
	export let userId: string | null;
	export let authenticated: boolean;
	export let toggleModal: () => void;

	const defaultImage =
		'https://cdn.britannica.com/36/123536-050-95CB0C6E/Variety-fruits-vegetables.jpg';

	// For creating new recipes
	let newRecipeName = '';
	let ingredientRows = [{ ingredientName: '', ingredientAmount: '' }];
	let newInstructions = [''];
	let newServings = 0;
	let newCalories = 0;
	let newTime = 0;

	let imageOption: 'upload' | 'generate' | 'link' = 'upload'; // Default: upload. Other: generate, link
	let newImageFile: File | null = null;
	let newImageLink = '';
	let allowUploadImage = false;

	// Image
	function handleImageChange(event: Event) {
		const target = event.target as HTMLInputElement;
		if (target.files && target.files.length > 0) {
			newImageFile = target.files[0];
		}
	}

	async function uploadImage() {
		if (!newImageFile) return;

		allowUploadImage = true;
		try {
			newImageLink = await imageHandler.uploadFile(newImageFile);
		} catch (e) {
			console.error('Failed to upload image', e);
			alert('Image upload failed. Please try again');
		} finally {
			allowUploadImage = false;
		}
	}

	async function generateImage() {
		if (!newRecipeName.trim()) {
			alert('Please enter a recipe name before generating an image');
			return;
		}

		allowUploadImage = true;
		try {
			newImageLink = await imageHandler.generateImage(newRecipeName);
		} catch (e) {
			console.error('Image generation failed', e);
			alert('Generate image failed. Please try again');
		} finally {
			allowUploadImage = false;
		}
	}
	// Ingredients
	function addIngredientRow() {
		ingredientRows = [...ingredientRows, { ingredientName: '', ingredientAmount: '' }];
	}
	function removeIngredientRow(index: number) {
		ingredientRows.splice(index, 1);
		ingredientRows = [...ingredientRows];
	}

	function handleIngredientChange(
		index: number,
		field: 'ingredientName' | 'ingredientAmount',
		value: string
	) {
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
	async function handleAddRecipeSubmit() {
		if (!authenticated || !userId) {
			console.log('User is not authenticated');
			return;
		}
		const newIngredients = ingredientRows.filter(
			(row) => row.ingredientName && row.ingredientAmount
		);

		if (!newRecipeName || newIngredients.length === 0 || newInstructions.length === 0) {
			alert('Please enter all recipe details.');
			return;
		}

		// If user upload an image
		if (imageOption === 'upload' && newImageFile && !newImageLink) {
			await uploadImage();
		} else if (imageOption === 'generate' && !newImageLink) {
			await generateImage();
		}

		const newRecipe = {
			name: newRecipeName,
			instructions: newInstructions,
			servings: newServings,
			calories: newCalories,
			time: newTime,
			img_url: newImageLink || defaultImage,
			ingredients: newIngredients,
			author: userId,
		};
		console.log('Add new recipe', newRecipe);
		try {
			await recipeHandler.addRecipe(newRecipe);
			await recipeHandler.getRecipes(null);
			toggleModal();
		} catch (error) {
			alert((error as Error).message);
		}
	}
</script>

{#if showModal}
	<Modal onclose={toggleModal}>
		<div class="mb-10 space-y-4">
			<label for="recipe-name">Recipe name</label>
			<Input
				id="recipe-name"
				type="text"
				bind:value={newRecipeName}
				placeholder="Enter your recipe name"
			/>
		</div>

		<!-- Image -->
		<div class="mb-4">
			<label for="image-source" class="block font-semibold">Choose image source</label>
			<div id="image-source" class="mt-2 flex space-x-4">
				<label>
					<input type="radio" bind:group={imageOption} value="upload" />
					Upload Image
				</label>
				<label>
					<input type="radio" bind:group={imageOption} value="generate" />
					Generate Image with GPT
				</label>
				<label>
					<input type="radio" bind:group={imageOption} value="link" />
					Paste Image Link
				</label>
			</div>
		</div>

		<!-- Upload image -->
		{#if imageOption === 'upload'}
			<div class="mb-4">
				<label for="recipe-image">Upload Recipe Image</label>
				<input id="recipe-image" type="file" accept="image/*" onchange={handleImageChange} />
				{#if newImageFile}
					<p class="text-gray-600">Selected: {newImageFile.name}</p>
					<button onclick={uploadImage} class="mt-2 rounded-lg bg-teal-500 px-4 py-1 text-white"
						>{allowUploadImage ? 'Uploading...' : 'Upload Image'}</button
					>
				{/if}
			</div>
		{/if}

		<!-- Generate image -->
		{#if imageOption === 'generate'}
			<div class="mb-4">
				<p class="text-gray-600">Generate an image based on the recipe name.</p>
				<button onclick={generateImage} class="mt-2 rounded-lg bg-blue-500 px-4 py-1 text-white">
					{allowUploadImage ? 'Generating...' : 'Generate Image'}
				</button>
			</div>
		{/if}
		<!-- Paste Image Link -->
		{#if imageOption === 'link'}
			<div class="mb-4">
				<label for="image-link">Paste Image URL</label>
				<Input
					id="image-link"
					type="text"
					bind:value={newImageLink}
					placeholder="Enter image URL"
				/>
			</div>
		{/if}

		<!-- Preview Image -->
		{#if newImageLink}
			<div class="mb-4">
				<p class="text-gray-600">Preview:</p>
				<img src={newImageLink} alt={newRecipeName} class="mt-2 h-32 rounded-lg shadow-lg" />
			</div>
		{/if}
		<div class="mb-10 space-y-4">
			<div class="flex items-center justify-between gap-4">
				<label for="recipe-ingredients">Recipe ingredients</label>
				<button onclick={addIngredientRow}>Add ingredient</button>
			</div>
			<div class="space-y-3">
				{#each ingredientRows as ingredient, index}
					<div class="intems-center flex gap-2">
						<Input
							type="text"
							bind:value={ingredient.ingredientName}
							oninput={(e) =>
								handleIngredientChange(
									index,
									'ingredientName',
									(e.currentTarget as HTMLInputElement).value
								)}
							placeholder="Ingredient"
						/>
						<Input
							type="text"
							bind:value={ingredient.ingredientAmount}
							placeholder="Amount (eg 300g)"
							oninput={(e) =>
								handleIngredientChange(
									index,
									'ingredientAmount',
									(e.currentTarget as HTMLInputElement).value
								)}
						/>
						<button onclick={() => removeIngredientRow(index)}>Remove</button>
					</div>
				{/each}
			</div>
		</div>

		<div class="mb-10 flex items-center gap-4">
			<div>
				<label for="duration">Time (minutes)</label>
				<Input
					id="duration"
					type="number"
					min="1"
					bind:value={newTime}
					placeholder="Enter time in minutes (eg. 60)"
				/>
			</div>
			<div>
				<label for="servings">Servings</label>
				<Input id="servings" type="text" bind:value={newServings} placeholder="Enter serving" />
			</div>
			<div>
				<label for="calories">Calories</label>
				<Input id="calories" type="text" bind:value={newCalories} placeholder="Enter calories" />
			</div>
		</div>

		<div class="mb-10 space-y-4">
			<div class="flex items-center justify-between gap-4">
				<label for="instructions">Instructions</label>
				<button onclick={addInstruction}>Add instruction</button>
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
						/>
						<button onclick={() => removeInstruction(index)}>Remove</button>
					</div>
				{/each}
			</div>
		</div>
		<div class="flex justify-end">
			<button
				onclick={handleAddRecipeSubmit}
				class="bg-teal-500 text-white">Submit</button>
		</div>
	</Modal>
{/if}

<style>
	:global(label) {
		margin-bottom: 4px;
		display: block;
		font-weight: 600;
		font-size: 16px;
		color: #374151;
	}
	:global(input) {
		border: 2px solid #ccc;
		padding: 10px;
		font-size: 16px;
		border-radius: 10px;
		width: 100%;
		transition: border 0.3s ease;
	}

	:global(input:focus) {
		outline: none;
		border-color: #3b82f6; /* Blue border on focus */
		box-shadow: 0 0 5px rgba(59, 130, 246, 0.5);
	}
	:global(button) {
		background-color: white;
		color: #0d9488; /* Tailwind: text-teal-600 */
		border: 2px solid #5eead4; /* Tailwind: outline-teal-300 */
		padding: 8px 12px;
		font-size: 16px;
		font-weight: 600;
		border-radius: 10px;
		cursor: pointer;
		transition: all 0.3s ease;
	}

	:global(button:hover) {
		background-color: #5eead4; /* Light teal hover */
		color: white;
	}

	:global(button:focus) {
		outline: none;
		box-shadow: 0 0 5px rgba(13, 148, 136, 0.5); /* Focus glow */
	}
</style>
