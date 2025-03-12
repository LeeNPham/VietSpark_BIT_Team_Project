<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import type { RecipeDetailDTO, ReviewDTO } from '$lib/types';
	import { recipeHandler, recipeStore } from '$lib/stores/recipeStore';
	import { userStore, userHandler } from '$lib/stores/userStore';
	import { reviewHandler, reviewStore } from '$lib/stores/reviewStore';
	import { imageHandler } from '$lib/stores/imageStore';
	import { Button, Spinner } from 'flowbite-svelte';
	import { showToast } from '$lib/stores/alertStore';

	let recipe: RecipeDetailDTO | null = null;
	let isLoading: boolean = false;
	let recipeId: string;
	let authenticated = false;
	let userRecipes: string[] = [];
	let reviews: ReviewDTO[] = [];
	let rating = 0;
	let reviewText = '';
	let reviewDescription = '';
	let reviewImages: File[] = [];
	let reviewVideo: File | null = null;
	let reviewerProfileImage: string = '';

	$: recipeId = $page.params.id;

	async function fetchRecipe() {
		try {
			await recipeHandler.getRecipe(recipeId);
			await reviewHandler.getReviews(recipeId, null, null, null);
		} catch (e) {
			showToast('error', (e as Error).message);
		}
	}

	recipeStore.subscribe((store) => {
		isLoading = store?.isLoading ?? false;
		recipe = store?.currentRecipe ?? null;
		console.log('recipe', recipe);
	});

	userStore.subscribe((store) => {
		authenticated = store?.authenticated ?? false;
		userRecipes = store?.recipes ?? [];
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
				description: reviewDescription,
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

{#if recipe && !isLoading}
	<div class="p-6">
		<!-- Recipe Name with a Gradient Effect -->
		<div class="p-0 px-4 sm:p-0 sm:px-4 md:p-4 md:px-6 lg:p-6 lg:px-0">
			<div class="flex flex-col md:flex-row md:items-end md:justify-between">
				<!-- Recipe Name -->
				<h1
					class="from-secondary-green to-secondary-forest bg-gradient-to-r bg-clip-text text-3xl font-medium text-transparent sm:text-3xl md:text-4xl lg:text-4xl"
				>
					{recipe.name}
				</h1>

				<!-- Created By -->
				{#if recipe.author_name}
					<div class="mt-2 flex items-center space-x-4 rounded-lg md:mt-0">
						<div class="group relative">
							<!-- Profile Image with Border -->
							<div
								class="border-secondary-forest ml-2 h-12 w-12 overflow-hidden rounded-full border-2 sm:ml-2 md:ml-0"
							>
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

			<div class="mt-2 flex justify-center sm:mt-2 md:mt-6 lg:mt-8">
				<!-- Image with Shadow & Hover Effect -->
				<img
					src={recipe.img_url}
					class="border-secondary-forest mt-4 w-5/6 rounded-lg border-2 object-cover sm:w-5/6 md:w-[40%]"
					alt={recipe.name}
				/>
			</div>

			<!-- Right Column: Buttons -->
			<div class="mt-10 flex justify-center space-x-4">
				{#if authenticated && !userRecipes.includes(recipeId)}
					<Button
						class="text-secondary-forest border-secondary-forest hover:bg-secondary-blue flex items-center space-x-2 rounded-full border-2 bg-white px-5  py-1 text-sm font-semibold shadow-md transition-all duration-300 hover:text-black sm:text-sm md:text-lg lg:text-lg"
						onclick={handleAddFavorite}
					>
						<span>❤️</span> <span>Add to favorite</span>
					</Button>
				{:else if authenticated}
					<Button
						class="text-secondary-forest border-secondary-forest hover:bg-secondary-blue flex items-center space-x-2 rounded-full border-2 bg-white px-5  py-1 text-sm font-semibold shadow-md transition-all duration-300 hover:text-black sm:text-sm md:text-lg lg:text-lg"
						onclick={handleRemoveFavorite}
					>
						<span>💔 </span> <span>Remove from favorite</span>
					</Button>
				{/if}
			</div>
			<!-- Left Column: Details -->
			<div class="mt-8 flex flex-col justify-evenly sm:flex-col md:flex-row lg:flex-row">
				<p class="text-lg"><strong>⏰ Time:</strong> {recipe.time} mins</p>
				<p class="text-lg"><strong>🔥 Calories:</strong> {recipe.calories} kcal</p>
				<p class="text-lg"><strong>🥘 Servings:</strong> {recipe.servings}</p>
			</div>

			<!-- Ingredients Section -->
			<h2 class="text-secondary-green mt-4 text-2xl font-medium sm:mt-4 md:mt-6 lg:mt-6">
				🥗 Ingredients
			</h2>
			<ul class="border-secondary-forest mt-4 list-disc rounded-lg border-2 bg-white p-4 pl-10">
				{#each recipe.ingredients as ingredient}
					<li class="font-medium text-gray-800">
						{ingredient.ingredientName} - {ingredient.ingredientAmount}
					</li>
				{/each}
			</ul>

			<!-- Instructions Section -->
			<h2 class="text-secondary-green mt-4 text-2xl font-medium">🍽️ Instructions</h2>
			<ol class="border-secondary-forest mt-4 space-y-2 rounded-lg border-2 bg-white p-4">
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
				<div class="border-secondary-forest rounded-lg border-2 bg-white p-4">
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
						class="h-10 w-full resize-none rounded-lg border text-gray-800 focus:ring-2 focus:ring-blue-400"
						placeholder="Review title..."
						maxlength="50"
						bind:value={reviewDescription}
					></textarea>
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
				<div class="flex flex-col items-center justify-center space-y-2">
					<p class="text-gray-600">No reviews yet.</p>
				</div>
			{:else}
				<h2
					class="mt-8 flex items-center gap-2 border-b-2 border-blue-400 pb-1 text-xl font-bold text-blue-600"
				>
					<img
						src="https://img.icons8.com/?size=100&id=apsEwjRsibDJ&format=png&color=000000"
						alt="Review Icon"
						class="h-6 w-6"
					/> Reviews
				</h2>
				{#each reviews as review}
					<div class="mb-6 border-b pb-4">
						<!-- Reviewer Name -->
						<div class="mt-1 flex items-center space-x-2">
							<img
								src={review?.userImage ||
									'https://img.icons8.com/?size=100&id=zxB19VPoVLjK&format=png&color=000000'}
								alt="Reviewer Profile"
								class="h-10 w-10 rounded-full object-cover"
							/>
							<p class="mt-2 text-sm">{review.userName}</p>
						</div>

						<!-- Star Rating -->
						<div class="mt-1 flex items-center space-x-2">
							<span class="text-yellow-400">{'⭐'.repeat(review.rating)}</span>
							<strong class="text-lg text-gray-500"
								>{review?.description || 'Test description'}</strong
							>
						</div>

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
					</div>
				{/each}
			{/if}
		</div>
	</div>
{:else if isLoading}
	<div class="mt-4 flex flex-col items-center justify-center">
		<span>Wait while we load the recipe...</span>
		<Spinner size={10} color="green" />
	</div>
{:else}
	<div class="mt-4 flex flex-col items-center justify-center">
		<p>Recipe not found. <a href="/" class="text-secondary-green">Go back to home.</a></p>
	</div>
{/if}
