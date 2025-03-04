<script>
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
</button>
