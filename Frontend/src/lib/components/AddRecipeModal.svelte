<script lang="ts">
	import { Input } from 'flowbite-svelte';
	import Modal from '../components/Modal.svelte';
	import { recipeHandler } from '$lib/stores/recipeStore';
	import { mediaHandler } from '$lib/stores/mediaStore';
	import { showToast } from '$lib/stores/alertStore';
	import { customStyles } from '$src/custom';

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
			newImageLink = await mediaHandler.uploadImage(newImageFile);
			console.log(newImageLink);
		} catch (e) {
			console.error('Failed to upload image', e);
			showToast('error', (e as Error).message);
		} finally {
			allowUploadImage = false;
		}
	}

	async function generateImage() {
		if (!newRecipeName.trim()) {
			showToast('error', 'Please enter a recipe name before generating an image');
			return;
		}

		allowUploadImage = true;
		try {
			newImageLink = await mediaHandler.generateImage(newRecipeName);
		} catch (e) {
			console.error('Image generation failed', e);
			showToast('error', (e as Error).message);
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
			showToast('error', 'Please log in to add a recipe.');
			return;
		}
		const newIngredients = ingredientRows.filter(
			(row) => row.ingredientName && row.ingredientAmount
		);

		if (!newRecipeName || newIngredients.length === 0 || newInstructions.length === 0) {
			showToast('error', 'Please enter all recipe details.');
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
			author: userId
		};
		console.log('Add new recipe', newRecipe);
		try {
			await recipeHandler.addRecipe(newRecipe);
			await recipeHandler.getRecipes(null);
			toggleModal();
		} catch (error) {
			showToast('error', (error as Error).message);
		}
	}
</script>

{#if showModal}
	<Modal onclose={toggleModal}>
		<div class="mb-6 space-y-4 sm:mb-6 md:mb-10 lg:mb-10">
			<label for="recipe-name" class={customStyles.recipeHeader}>Recipe name</label>
			<Input
				id="recipe-name"
				type="text"
				bind:value={newRecipeName}
				placeholder="Enter your recipe name"
				class={customStyles.inputBox}
			/>
		</div>

		<!-- Image -->
		<div class="mb-6">
			<label for="image-source" class={customStyles.recipeh2}>Choose image source</label>
			<div id="image-source" class="mt-2 flex space-x-4">
				<label class={customStyles.recipeResponsive}>
					<input type="radio" bind:group={imageOption} value="upload" />
					Upload Image
				</label>
				<label class={customStyles.recipeResponsive}>
					<input type="radio" bind:group={imageOption} value="generate" />
					Generate Image with GPT
				</label>
			</div>
		</div>

		<!-- Upload image -->
		{#if imageOption === 'upload'}
			<div class="mb-10 flex flex-col">
				<label for="recipe-image" class="text-secondary-green mb-2 text-sm"
					>Upload Recipe Image</label
				>
				<input
					id="recipe-image"
					type="file"
					accept="image/*"
					onchange={handleImageChange}
					class="text-secondary-forest text-sm"
				/>
				{#if newImageFile}
					<p class="text-secondary-forest text-sm">Selected: {newImageFile.name}</p>
					<button
						onclick={uploadImage}
						class="bg-secondary-green mt-2 rounded-lg px-4 py-1 text-white"
						>{allowUploadImage ? 'Uploading...' : 'Upload Image'}</button
					>
				{/if}
			</div>
		{/if}

		<!-- Generate image -->
		{#if imageOption === 'generate'}
			<div class="mb-10 space-y-4">
				<p class="text-secondary-forest text-sm sm:text-sm md:text-lg lg:text-lg">
					Generate an image based on the recipe name.
				</p>
				<button onclick={generateImage} class={customStyles.recipeButton}>
					{allowUploadImage ? 'Generating...' : 'Generate Image'}
				</button>
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
				<label for="recipe-ingredients" class={customStyles.recipeHeader}>Recipe ingredients</label>
				<button onclick={addIngredientRow} class={customStyles.recipeButton}>Add ingredient</button>
			</div>
			<div>
				{#each ingredientRows as ingredient, index}
					<div class="mb-3 flex flex-row items-center gap-2 sm:gap-2 md:gap-4 lg:gap-4">
						<Input
							type="text"
							bind:value={ingredient.ingredientName}
							class={customStyles.inputBox}
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
							class={customStyles.inputBox}
							oninput={(e) =>
								handleIngredientChange(
									index,
									'ingredientAmount',
									(e.currentTarget as HTMLInputElement).value
								)}
						/>
						<button onclick={() => removeIngredientRow(index)} class={customStyles.recipeRemove}
							>Remove</button
						>
					</div>
				{/each}
			</div>
		</div>

		<div class="mb-10 flex items-center gap-4">
			<div class="space-y-2">
				<label for="duration" class={customStyles.recipeh2}>Minutes</label>
				<Input
					id="duration"
					type="number"
					min="1"
					bind:value={newTime}
					placeholder="Enter time in minutes (eg. 60)"
					class={customStyles.inputBox}
				/>
			</div>
			<div class="space-y-2">
				<label for="servings" class={customStyles.recipeh2}>Servings</label>
				<Input
					id="servings"
					type="text"
					bind:value={newServings}
					placeholder="Enter serving"
					class={customStyles.inputBox}
				/>
			</div>
			<div class="space-y-2">
				<label for="calories" class={customStyles.recipeh2}>Calories</label>
				<Input
					id="calories"
					type="text"
					bind:value={newCalories}
					placeholder="Enter calories"
					class={customStyles.inputBox}
				/>
			</div>
		</div>

		<div class="mb-10 space-y-4">
			<div class="flex items-center justify-between gap-4">
				<label for="instructions" class={customStyles.recipeHeader}>Instructions</label>
				<button onclick={addInstruction} class={customStyles.recipeButton}>Add instruction</button>
			</div>
			<div class="space-y-3">
				{#each newInstructions as instruction, index}
					<div class="flex items-center gap-2">
						<Input
							type="text"
							bind:value={instruction}
							placeholder="Put the instruction here"
							class={customStyles.inputBox}
							oninput={(e) =>
								handleInstructionChange(index, (e.currentTarget as HTMLInputElement).value)}
						/>
						<button onclick={() => removeInstruction(index)} class={customStyles.recipeRemove}
							>Remove</button
						>
					</div>
				{/each}
			</div>
		</div>
		<div>
			<button
				onclick={handleAddRecipeSubmit}
				class="bg-secondary-forest outline-secondary-green w-full rounded-2xl p-2 text-xs text-white outline sm:text-sm md:text-lg lg:text-lg"
				>Submit</button
			>
		</div>
	</Modal>
{/if}
