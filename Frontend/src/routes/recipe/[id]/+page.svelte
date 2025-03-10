<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import type { RecipeDetailDTO, ReviewDTO } from '$lib/types';
	import { recipeHandler, recipeStore } from '$lib/stores/recipeStore';
	import { userStore, userHandler } from '$lib/stores/userStore';
	import { reviewHandler, reviewStore } from '$lib/stores/reviewStore';
	import { imageHandler } from '$lib/stores/imageStore';
	import { Button } from 'flowbite-svelte';
	import { showToast } from '$lib/stores/alertStore';
	import { count } from 'firebase/firestore';

	let recipe: RecipeDetailDTO | null = null;
	let recipeId: string;
	let authenticated = false;
	let userRecipes: string[] = [];
	let reviews: ReviewDTO[] = [];
	let rating = 0;
	let reviewText = '';
	let reviewImages: File[] = [];
	let reviewVideo: File | null = null;

	$: recipeId = $page.params.id;

	async function fetchRecipe() {
		try {
			await recipeHandler.getRecipe(recipeId);
			await reviewHandler.getReviews(recipeId, null, null, null);
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

	reviewStore.subscribe((store) => {
		reviews = store?.reviews ?? [];
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
		if (!authenticated) {
			showToast('error', 'Please login to submit a review');
			return;
		}
		if (!rating) {
			showToast('error', 'Please rate the recipe');
			return;
		}
		if (!reviewText) {
			showToast('error', 'Please write a review');
			return;
		}

		try {
			const reviewImageLinks: string[] = [];
			let counter = 0;
			for (const image of reviewImages) {
				if (!image) continue;
				if (counter >= 3) break;
				const link = await imageHandler.uploadFile(image);
				reviewImageLinks.push(link);
				counter++;
			}

			const reviewVideoLink = reviewVideo ? await imageHandler.uploadFile(reviewVideo) : '';

			const reviewData = {
				rating,
				content: reviewText,
				images: reviewImageLinks,
				video: reviewVideoLink,
				recipe_id: recipeId
			};
			await reviewHandler.submitReview(reviewData);
			showToast('success', 'Review submitted successfully');
			reviewText = '';
			reviewImages = [];
			reviewVideo = null;
		} catch (e) {
			showToast('error', (e as Error).message);
		}
	}
</script>

{#if recipe}
		<!-- Recipe Name with a Gradient Effect -->
	<div class="p-0 sm:p-0 md:p-4 lg:p-6 px-4 sm:px-4 md:px-6 lg:px-0">
		<div class="flex flex-col md:flex-row md:items-end md:justify-between">
			<!-- Recipe Name -->
			<h1 class="text-3xl sm:text-3xl md:text-4xl lg:text-4xl font-medium text-transparent bg-gradient-to-r from-secondary-green to-secondary-forest bg-clip-text">
				{recipe.name}
			</h1>

			<!-- Created By -->
			{#if recipe.author_name}
				<div class="mt-2 flex items-center space-x-4 rounded-lg md:mt-0">
					<div class="group relative">
						<!-- Profile Image with Border -->
						<div class="h-12 w-12 overflow-hidden rounded-full border-2 border-secondary-forest ml-2 sm:ml-2 md:ml-0">
							<img
								class="h-full w-full object-cover"
								src={'https://storage.googleapis.com/chat-app-react-and-firebase.appspot.com/profileImages/' +
									recipe.author_id}
								alt="Profile image of {recipe.author_id}"
							/>
						</div>
						<!-- Tooltip on Hover -->
						<div class="absolute left-full top-1/2 ml-3 -translate-y-1/2 transform whitespace-nowrap rounded bg-gray-900 px-3 py-1 text-sm text-white opacity-0 shadow-lg transition-opacity duration-300 group-hover:opacity-100">
							{recipe.author_name}
						</div>
					</div>
					<!-- Author Name -->
					<p class="text-lg font-semibold text-gray-800">{recipe.author_name}</p>
				</div>
			{/if}
		</div>


		<div class="mt-2 sm:mt-2 md:mt-6 lg:mt-8 flex justify-center">
			<!-- Image with Shadow & Hover Effect -->
			<img
				src={recipe.img_url}
				class="mt-4 w-5/6 sm:w-5/6 md:w-[40%] rounded-lg object-cover  border-2 border-secondary-forest"
				alt={recipe.name}
			/>
		</div>

		<!-- Right Column: Buttons -->
		<div class="flex justify-center space-x-4 mt-10">
			{#if authenticated && !userRecipes.includes(recipeId)}
				<Button
					class="px-5 py-1 text-sm sm:text-sm md:text-lg lg:text-lg font-semibold flex items-center space-x-2  text-secondary-forest border-secondary-forest hover:bg-secondary-blue rounded-full border-2 bg-white shadow-md transition-all duration-300 hover:text-black"
					onclick={handleAddFavorite}
				>
					<span>❤️</span> <span>Add to favorite</span>
				</Button>
			{:else if authenticated}
				<Button
					class="px-5 py-1 text-sm sm:text-sm md:text-lg lg:text-lg font-semibold flex items-center space-x-2  text-secondary-forest border-secondary-forest hover:bg-secondary-blue rounded-full border-2 bg-white shadow-md transition-all duration-300 hover:text-black"
					onclick={handleRemoveFavorite}
				>
					<span>💔 </span> <span>Remove from favorite</span>
				</Button>
			{/if}
		</div>
		<!-- Left Column: Details -->
		<div class="flex flex-col sm:flex-col md:flex-row lg:flex-row justify-evenly mt-8">
			<p class="text-lg"><strong>⏰  Time:</strong> {recipe.time} mins</p>
			<p class="text-lg"><strong>🔥 Calories:</strong> {recipe.calories} kcal</p>
			<p class="text-lg"><strong>🥘 Servings:</strong> {recipe.servings}</p>
		</div>

		<!-- Ingredients Section -->
		<h2 class="mt-4 sm:mt-4 md:mt-6 lg:mt-6 text-2xl text-secondary-green font-medium">
			🥗 Ingredients
		</h2>
		<ul class="mt-4 list-disc rounded-lg bg-white p-4 pl-10 border-2 border-secondary-forest">
			{#each recipe.ingredients as ingredient}
				<li class="font-medium text-gray-800">
					{ingredient.ingredientName} - {ingredient.ingredientAmount}
				</li>
			{/each}
		</ul>

		<!-- Instructions Section -->
		<h2 class="mt-4 text-2xl text-secondary-green font-medium">
			🍽️ Instructions
		</h2>
		<ol class="mt-4 space-y-2 rounded-lg bg-white p-4 border-2 border-secondary-forest">
			{#each recipe.instructions as instruction, i}
				<li class="flex items-start font-medium text-gray-800">
					<span class="flex h-6 w-6 items-center justify-center text-sm">
						{(i + 1).toString().padStart(2) + '. '}
					</span>
					{instruction}
				</li>
			{/each}
		</ol>
	</div>

	{#if authenticated}
		<div class="mt-4 px-4 sm:px-4 md:px-6 lg:px-0">
			<div class="rounded-lg bg-white p-4  border-2 border-secondary-forest">
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
		</div>
	{/if}

	<!-- Display Reviews -->
	<div class="mt-6 px-4 sm:px-4 md:px-6 lg:px-0">
		{#if reviews.length === 0}
			<p class="text-gray-600">No reviews yet. Be the first to rate this recipe!</p>
		{:else}
			{#each reviews as review}
				<div class="mb-6 border-b pb-4">
					<!-- Star Rating -->
					<div class="text-yellow-400">{'⭐'.repeat(review.rating)}</div>

					<!-- Review Text -->
					<p class="mt-1 text-gray-800">{review.content}</p>

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
