<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import type { RecipeDetailDTO } from '$lib/types';
	import { recipeHandler, recipeStore } from '$lib/stores/recipeStore';
	import { userStore, userHandler } from '$lib/stores/userStore';
	import { Button } from 'flowbite-svelte';
	import { showToast } from '$lib/stores/alertStore';
	import { reviewHandler } from '$lib/stores/reviewStore';

	let recipe: RecipeDetailDTO | null = null;
	let recipeId: string;
	let authenticated = false;
	let userRecipes: string[] = [];
	let reviews: any[] = []; // Todo, add review section
	let rating = 0;
	let reviewText = '';
	let reviewImages: File[] = [];
	let reviewVideo: File | null = null;

	$: recipeId = $page.params.id;

	async function fetchRecipe() {
		try {
			await recipeHandler.getRecipe(recipeId);
			recipe = $recipeStore.currentRecipe;
		} catch (e) {
			showToast('error', (e as Error).message);
		}
	}

	userStore.subscribe((store) => {
		authenticated = store?.authenticated ?? false;
		userRecipes = store?.recipes ?? [];
		console.log('Current user recipes:', userRecipes);
	});

	onMount(fetchRecipe);

	async function handleAddFavorite() {
		if (userRecipes?.includes(recipeId)) {
			showToast('error', 'Recipe already favorited');
			return;
		}
		try {
			await userHandler.addFavoriteRecipe(recipeId);
			showToast('success', 'Recipe added to favorites');
		} catch (e) {
			showToast('error', (e as Error).message);
		}
	}

	function setRating(newRating: number) {
		rating = newRating;
	}
	async function handleRemoveFavorite() {
		try {
			await userHandler.unfavoriteRecipe(recipeId);
			showToast('success', 'Recipe removed from favorites');
		} catch (e) {
			showToast('error', (e as Error).message);
		}
	}

	async function submitReview() {
		// try {
		// 	await reviewHandler.submitReview(recipeId, rating, reviewText, reviewImages, reviewVideo);
		// 	showToast('success', 'Review submitted successfully');
		// 	reviewText = '';
		// 	reviewImages = [];
		// 	reviewVideo = null;
		// } catch (e) {
		// 	showToast('error', (e as Error).message);
		// }
	}
</script>

{#if recipe}
	<div class="p-6">
		<!-- Recipe Name with a Gradient Effect -->
		<div class="flex flex-col md:flex-row md:items-end md:justify-between">
			<!-- Recipe Name -->
			<h1
				class="bg-gradient-to-r from-teal-600 to-blue-500 bg-clip-text text-3xl font-extrabold text-transparent lg:text-6xl"
			>
				{recipe.name}
			</h1>

			<!-- Created By -->
			{#if recipe.author_name}
				<div class="mt-2 flex items-center space-x-4 rounded-lg md:mt-0">
					<div class="group relative">
						<!-- Profile Image with Border -->
						<div class="h-12 w-12 overflow-hidden rounded-full border-2 border-green-500">
							<img
								class="h-full w-full object-cover"
								src={'https://storage.googleapis.com/chat-app-react-and-firebase.appspot.com/profileImages/' +
									recipe.author_id}
								alt="Profile image of {recipe.author_id}"
							/>
						</div>
						<!-- Tooltip on Hover -->
						<div
							class="absolute left-full top-1/2 ml-3 -translate-y-1/2 transform whitespace-nowrap rounded bg-gray-900 px-3 py-1 text-sm text-white opacity-0 shadow-lg transition-opacity duration-300 group-hover:opacity-100"
						>
							{recipe.author_name}
						</div>
					</div>
					<!-- Author Name -->
					<p class="text-lg font-semibold text-gray-800">{recipe.author_name}</p>
				</div>
			{/if}
		</div>
		<!-- Image with Shadow & Hover Effect -->
		<img
			src={recipe.img_url}
			class="mt-4 w-full rounded-lg object-cover shadow-lg transition-transform duration-300 hover:scale-105"
			alt={recipe.name}
		/>

		<!-- Description Section -->
		<h2 class="mt-8 border-b-2 border-blue-400 pb-1 text-xl font-bold text-blue-600">
			📖 Description
		</h2>

		<!-- Two-Column Layout -->
		<div
			class="mt-4 flex flex-col items-start justify-between rounded-lg bg-gray-100 p-6 shadow-md md:flex-row md:items-center"
		>
			<!-- Left Column: Details -->
			<div class="space-y-3 text-gray-800">
				<p class="text-lg"><strong>⏳ Time:</strong> {recipe.time} mins</p>
				<p class="text-lg"><strong>🔥 Calories:</strong> {recipe.calories} kcal</p>
				<p class="text-lg"><strong>🍽️ Servings:</strong> {recipe.servings}</p>
			</div>

			<!-- Right Column: Buttons -->
			<div class="mt-4 flex space-x-4 md:mt-0">
				{#if authenticated && !userRecipes.includes(recipeId)}
					<Button
						class="bg-secondary-forest hover:bg-secondary-blue hover:text-secondary-forest flex items-center space-x-2 rounded-full px-5 py-3 text-lg font-semibold text-white shadow-md transition-all duration-300"
						onclick={handleAddFavorite}
					>
						<span>❤️</span> <span>Add to favorite</span>
					</Button>
				{:else if authenticated}
					<Button
						class="border-secondary-forest text-secondary-forest hover:bg-secondary-blue flex items-center space-x-2 rounded-full border-2 bg-white px-5 py-3 text-lg font-semibold shadow-md transition-all duration-300 hover:text-black"
						onclick={handleRemoveFavorite}
					>
						<span>🖤</span> <span>Remove from favorite</span>
					</Button>
				{/if}
			</div>
		</div>

		<!-- Ingredients Section -->
		<h2 class="mt-8 border-b-2 border-blue-400 pb-1 text-xl font-bold text-blue-600">
			📝 Ingredients
		</h2>
		<ul class="mt-3 list-disc rounded-lg bg-gray-100 p-4 pl-6 shadow-md">
			{#each recipe.ingredients as ingredient}
				<li class="font-medium text-gray-800">
					{ingredient.ingredientName} - {ingredient.ingredientAmount}
				</li>
			{/each}
		</ul>

		<!-- Instructions Section -->
		<h2 class="mt-8 border-b-2 border-blue-400 pb-1 text-xl font-bold text-blue-600">
			📌 Instructions
		</h2>
		<ol class="mt-3 space-y-2 rounded-lg bg-gray-100 p-4 shadow-md">
			{#each recipe.instructions as instruction, i}
				<li class="flex items-start font-medium text-gray-800">
					<span
						class="mr-3 flex h-6 w-6 items-center justify-center rounded-full bg-blue-500 text-sm font-bold text-white"
					>
						{i + 1}
					</span>
					{instruction}
				</li>
			{/each}
		</ol>
	</div>

	{#if authenticated}
		<div class="mt-4 rounded-lg bg-gray-50 p-6 shadow">
			<h3 class="text-lg font-semibold text-gray-800">Leave a Review</h3>

			<!-- Star Rating -->
			<div class="mt-2 flex space-x-1">
				{#each [1, 2, 3, 4, 5] as star}
					<button class="text-gray-400 hover:text-yellow-400" on:click={() => setRating(star)}>
						{star <= rating ? '⭐' : '☆'}
					</button>
				{/each}
			</div>

			<!-- Text Review -->
			<textarea
				class="mt-2 w-full rounded-lg border p-3 text-gray-800 focus:ring-2 focus:ring-blue-400"
				placeholder="Write your review..."
				bind:value={reviewText}
			></textarea>

			<!-- Image & Video Upload -->
			<div class="mt-4">
				<label for="rv-image" class="font-semibold text-gray-700">Upload Images (Max 3)</label>
				<input
					id="rv-image"
					type="file"
					accept="image/*"
					multiple
					max="3"
					class="mt-2 block w-full rounded-lg border p-2"
					on:change={(e) => {
						const target = e.target as HTMLInputElement;
						reviewImages = Array.from(target.files || []);
					}}
				/>
			</div>

			<div class="mt-4">
				<label for="rv-video" class="font-semibold text-gray-700">Upload Video (Max 1)</label>
				<input
					id="rv-video"
					type="file"
					accept="video/*"
					class="mt-2 block w-full rounded-lg border p-2"
					on:change={(e) => {
						const target = e.target as HTMLInputElement;
						reviewVideo = target.files?.[0] || null;
					}}
				/>
			</div>

			<!-- Submit Button -->
			<button
				class="mt-4 rounded-lg bg-blue-500 px-5 py-2 font-semibold text-white hover:bg-blue-600"
				on:click={submitReview}
			>
				Submit Review
			</button>
		</div>
	{/if}

	<!-- Display Reviews -->
	<div class="mt-6">
		{#if reviews.length === 0}
			<p class="text-gray-600">No reviews yet. Be the first to rate this recipe!</p>
		{:else}
			{#each reviews as review}
				<div class="mb-6 border-b pb-4">
					<!-- Star Rating -->
					<div class="text-yellow-400">{'⭐'.repeat(review.rating)}</div>

					<!-- Review Text -->
					<p class="mt-1 text-gray-800">{review.text}</p>

					<!-- Display Uploaded Images -->
					{#if review.images.length > 0}
						<div class="mt-2 flex space-x-2">
							{#each review.images as img}
								<img src={img} alt="Review image" class="h-20 w-20 rounded-lg object-cover" />
							{/each}
						</div>
					{/if}

					<!-- Display Uploaded Video -->
					{#if review.video}
						<div class="mt-2">
							<video src={review.video} controls class="w-full max-w-sm rounded-lg"></video>
						</div>
					{/if}

					<!-- Reviewer Name -->
					<p class="mt-2 text-sm text-gray-500">Reviewed by {review.userName}</p>
				</div>
			{/each}
		{/if}
	</div>
{:else}
	<p>Recipe not found. <a href="/" class="text-secondary-green">Go back to home.</a></p>
{/if}
