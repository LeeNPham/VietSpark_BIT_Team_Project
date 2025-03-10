<!-- <script>
    let recipe = {
        name: "Delicious Pancakes",
        img_url: "https://example.com/pancakes.jpg",
        time: "30 mins",
        calories: 250,
        servings: 4,
        ingredients: [
            { ingredientName: "Flour", ingredientAmount: "2 cups" },
            { ingredientName: "Milk", ingredientAmount: "1 cup" },
            { ingredientName: "Eggs", ingredientAmount: "2" },
            { ingredientName: "Sugar", ingredientAmount: "2 tbsp" },
            { ingredientName: "Baking Powder", ingredientAmount: "1 tsp" }
        ],
        instructions: [
            "Mix all dry ingredients together.",
            "Add milk and eggs, and mix until smooth.",
            "Heat a lightly oiled griddle over medium-high heat.",
            "Pour or scoop the batter onto the griddle.",
            "Brown on both sides and serve hot."
        ],
        author_id: "12345",
        author_name: "John Doe"
    };

    function handleAddFavorite() {
        alert("Added to favorite!");
    }
</script>

<div class="p-6">
    <h1 class="text-3xl  text-secondary-green">{recipe.name}</h1>
	<div class="flex justify-center">
		<img src="/Pork.png" class="mt-4 w-1/2 rounded-lg object-cover" alt={recipe.name} />
	</div>

    <h2 class="mt-6 text-xl text-secondary-green">Description</h2>
    <div class="flex items-center justify-center">
        <div class="rounded-full text-center text-xs sm:text-xs md:text-lg lg:text-lg text-white p-3 mx-2 bg-secondary-green">Time {recipe.time}</div>
        <div class="rounded-full text-center text-xs sm:text-xs md:text-lg lg:text-lg text-white p-3 mx-2 bg-secondary-green ">Calories: {recipe.calories ? recipe.calories : "Unknown"}</div>
        <div class="rounded-full text-center text-xs sm:text-xs md:text-lg lg:text-lg text-white p-3 mx-2 bg-secondary-green">Servings: {recipe.servings}</div>
    </div>
    <h2 class="mt-6 text-xl text-secondary-green">Ingredients</h2>
    <ul class="list-disc pl-6">
        {#each recipe.ingredients as ingredient}
            <li>{ingredient.ingredientName} {ingredient.ingredientAmount}</li>
        {/each}
    </ul>

    <h2 class="mt-6 text-xl text-secondary-green">Instructions</h2>
    <ol>
        {#each recipe.instructions as instruction, i}
            <li>{i + 1}. {instruction}</li>
        {/each}
    </ol>
    <h2 class="mt-6 text-xl text-secondary-green">Created by:</h2>
    <div class="flex">
        <div class="relative group">
            <div class="w-10 h-10 overflow-hidden border-green-300 p-0 rounded-full">
                <img class="w-full h-full object-cover" src={"https://storage.googleapis.com/chat-app-react-and-firebase.appspot.com/profileImages/" + recipe.author_id} alt="Profile image of {recipe.author_id}">
            </div>
            <div class="absolute top-1/2 left-full transform -translate-y-1/2 ml-2 bg-gray-800 text-white text-xs rounded py-1 px-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">
                {recipe.author_name}
            </div>
        </div>
    </div>
</div>
<button
    class="mb-3 py-2 font-sans text-lg font-semibold text-white rounded-full bg-secondary-forest hover:bg-secondary-blue hover:text-black hover:outline hover:outline-secondary-forest whitespace-nowrap"
    onclick={handleAddFavorite}>
    Add to favorite
</button> -->

<script lang="ts">
    import { onMount } from 'svelte';
    import { Button } from 'flowbite-svelte';
    import { showToast } from '$lib/stores/alertStore';

    let recipe = {
        name: "Delicious Pancakes",
        img_url: "https://example.com/pancakes.jpg",
        time: "30 mins",
        calories: 250,
        servings: 4,
        ingredients: [
            { ingredientName: "Flour", ingredientAmount: "2 cups" },
            { ingredientName: "Milk", ingredientAmount: "1 cup" },
            { ingredientName: "Eggs", ingredientAmount: "2" },
            { ingredientName: "Sugar", ingredientAmount: "2 tbsp" },
            { ingredientName: "Baking Powder", ingredientAmount: "1 tsp" }
        ],
        instructions: [
            "Mix all dry ingredients together.",
            "Add milk and eggs, and mix until smooth.",
            "Heat a lightly oiled griddle over medium-high heat.",
            "Pour or scoop the batter onto the griddle.",
            "Brown on both sides and serve hot."
        ],
        author_id: "12345",
        author_name: "John Doe"
    };

    let authenticated = true;
    let userRecipes = ["12345"];
    let reviews = [
        {
            rating: 5,
            content: "These pancakes were amazing! So fluffy and delicious!",
            images: ["https://example.com/review-image1.jpg"],
            video: "https://example.com/review-video.mp4",
            userName: "Jane Smith"
        },
        {
            rating: 4,
            content: "Tasty, but could use a little more sugar.",
            images: [],
            video: null,
            userName: "Chris Lee"
        }
    ];
    let rating = 0;
    let reviewText = '';
    let reviewImages = [];
    let reviewVideo = null;

    function setRating(star: number) {
        rating = star;
    }

    function submitReview() {
        reviews.push({
            rating,
            content: reviewText,
            images: reviewImages,
            video: reviewVideo,
            userName: "New User"
        });
        reviewText = '';
        reviewImages = [];
        reviewVideo = null;
    }

    function handleAddFavorite() {
        showToast('Recipe added to favorites');
    }

    function handleRemoveFavorite() {
        showToast('Recipe removed from favorites');
    }
</script>

{#if recipe}
    <div class="p-0 sm:p-0 md:p-4 lg:p-6 px-4 sm:px-4 md:px-6 lg:px-0">
        <div class="flex flex-col md:flex-row md:items-end md:justify-between">
            <h1 class="text-3xl sm:text-3xl md:text-4xl lg:text-4xl font-medium text-transparent bg-gradient-to-r from-secondary-green to-secondary-forest bg-clip-text  ">
                {recipe.name}
            </h1>
            {#if recipe.author_name}
                <div class="mt-2 flex items-center space-x-4 rounded-lg md:mt-0">
                    <div class="group relative">
                        <div class="h-12 w-12 overflow-hidden rounded-full border-2 border-secondary-forest ml-2 sm:ml-2 md:ml-0">
                            <img class="h-full w-full object-cover" src={'https://storage.googleapis.com/chat-app-react-and-firebase.appspot.com/profileImages/' + recipe.author_id} alt="Profile image of {recipe.author_id}" />
                        </div>
                        <div class="absolute left-full top-1/2 ml-3 -translate-y-1/2 transform whitespace-nowrap rounded bg-gray-900 px-3 py-1 text-sm text-white opacity-0 shadow-lg transition-opacity duration-300 group-hover:opacity-100">
                            {recipe.author_name}
                        </div>
                    </div>
                    <p class="text-lg font-semibold text-gray-800">{recipe.author_name}</p>
                </div>
            {/if}
        </div>


        <div class="mt-2 sm:mt-2 md:mt-6 lg:mt-8 flex justify-center">
            <img src="/Pork.png" class="mt-4 w-5/6 sm:w-5/6 md:w-[40%] rounded-lg object-cover  border-2 border-secondary-forest" alt={recipe.name} />
        </div>

        <div class="flex justify-center space-x-4 mt-10">
            {#if authenticated && !userRecipes.includes(recipe.author_id)}
                <Button class="px-5 py-1 text-sm sm:text-sm md:text-lg lg:text-lg font-semibold flex items-center space-x-2  text-secondary-forest border-secondary-forest hover:bg-secondary-blue rounded-full border-2 bg-white shadow-md transition-all duration-300 hover:text-black" onclick={handleAddFavorite}>
                    <span>❤️</span> <span>Add to favorite</span>
                </Button>
            {:else if authenticated}
                <Button class="px-5 py-1 text-sm sm:text-sm md:text-lg lg:text-lg font-semibold flex items-center space-x-2  text-secondary-forest border-secondary-forest hover:bg-secondary-blue rounded-full border-2 bg-white shadow-md transition-all duration-300 hover:text-black" onclick={handleRemoveFavorite}>
                    <span> 💔 </span> <span>Remove from favorite</span>
                </Button>
            {/if}
        </div>

        <div class="flex flex-col sm:flex-col md:flex-row lg:flex-row justify-evenly mt-8">
            <p class="text-lg"><strong>⏰ Time:</strong> {recipe.time} mins</p>
            <p class="text-lg"><strong>🔥 Calories:</strong> {recipe.calories} kcal</p>
            <p class="text-lg"><strong>🥘 Servings:</strong> {recipe.servings}</p>
        </div>

        <h2 class="mt-4 sm:mt-4 md:mt-6 lg:mt-6 text-2xl text-secondary-green font-medium"> 🥗 Ingredients</h2>
        <ul class="mt-4 list-disc rounded-lg bg-white p-4 pl-10 border-2 border-secondary-forest">
            {#each recipe.ingredients as ingredient}
                <li class="font-medium text-gray-800">{ingredient.ingredientName} - {ingredient.ingredientAmount}</li>
            {/each}
        </ul>

        <h2 class="mt-4 text-2xl text-secondary-green font-medium"> 🍽️ Instructions</h2>
        <ol class="mt-4 space-y-2 rounded-lg bg-white p-4 border-2 border-secondary-forest">
            {#each recipe.instructions as instruction, i}
                <li class="flex items-start font-medium text-gray-800">
                    <span class=" flex h-6 w-6 items-center justify-center text-sm ">
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

                <div class="mt-2 flex space-x-1">
                    {#each [1, 2, 3, 4, 5] as star}
                        <button class="text-gray-400 hover:text-yellow-400" on:click={() => setRating(star)}>
                            {star <= rating ? '⭐' : '☆'}
                        </button>
                    {/each}
                </div>

                <textarea class="mt-2 w-full rounded-lg border p-3 text-gray-800 focus:ring-2 focus:ring-blue-400" placeholder="Write your review..." bind:value={reviewText}></textarea>

                <div class="mt-4">
                    <label for="rv-image" class="font-semibold text-gray-700">Upload Images (Max 3)</label>
                    <input id="rv-image" type="file" accept="image/*" multiple max="3" class="mt-2 block w-full rounded-lg border p-2" on:change={(e) => { const target = e.target as HTMLInputElement; reviewImages = Array.from(target.files || []); }} />
                </div>

                <div class="mt-4">
                    <label for="rv-video" class="font-semibold text-gray-700">Upload Video (Max 1)</label>
                    <input id="rv-video" type="file" accept="video/*" class="mt-2 block w-full rounded-lg border p-2" on:change={(e) => { const target = e.target as HTMLInputElement; reviewVideo = target.files?.[0] || null; }} />
                </div>

                <button class="mt-4 rounded-lg bg-blue-500 px-5 py-2 font-semibold text-white hover:bg-blue-600" on:click={submitReview}>
                    Submit Review
                </button>
            </div>
        </div>
    {/if}

    <div class="mt-6 px-4 sm:px-4 md:px-6 lg:px-0">
        {#if reviews.length === 0}
            <p class="text-gray-600">No reviews yet. Be the first to rate this recipe!</p>
        {:else}
            {#each reviews as review}
                <div class="mb-6 border-b pb-4">
                    <div class="text-yellow-400">{'⭐'.repeat(review.rating)}</div>
                    <p class="mt-1 text-gray-800">{review.content}</p>
                    {#if review.images.length > 0}
                        <div class="mt-2 flex space-x-2">
                            {#each review.images as img}
                                <img src={img} alt="Review image" class="h-20 w-20 rounded-lg object-cover" />
                            {/each}
                        </div>
                    {/if}
                    {#if review.video}
                        <div class="mt-2">
                            <video src={review.video} controls class="w-full max-w-sm rounded-lg"></video>
                        </div>
                    {/if}
                    <p class="mt-2 text-sm text-gray-500">Reviewed by {review.userName}</p>
                </div>
            {/each}
        {/if}
    </div>
{:else}
    <p>Recipe not found. <a href="/" class="text-secondary-green">Go back to home.</a></p>
{/if}
