<script>
	import { writable } from 'svelte/store';
	const gApiKey = import.meta.env.VITE_GMAP_API_KEY;

	let mapUrl = writable(
		`https://www.google.com/maps/embed/v1/search?key=${gApiKey}&q=asian+vietnamese+grocery+stores`
	);
	let inputLocation = '';

	function updateMapUrl() {
		mapUrl.set(
			`https://www.google.com/maps/embed/v1/search?key=${gApiKey}&q=asian+vietnamese+grocery+stores+near+${inputLocation}`
		);
	}
	// @ts-ignore
	function pressEnter(event) {
		if (event.key === 'Enter') {
			updateMapUrl;
		}
	}
</script>

<div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <!-- Title -->
    <h3 class="text-2xl sm:text-3xl font-bold text-center mb-4 sm:mb-6">
      Search Local Asian Vietnamese Grocery Stores
    </h3>
  
    <!-- Search Input and Button -->
    <div class="flex flex-col sm:flex-row sm:space-x-4 space-y-3 sm:space-y-0 mb-4 sm:mb-6 justify-center">
      <input
        aria-label="search-input-box"
        placeholder="Enter location or zipcode"
        class="focus:border-primary-500 focus:ring-primary-500 dark:focus:border-primary-500 dark:focus:ring-primary-500 outline-secondary-green w-full sm:w-100 lg:w-120 rounded-2xl border border-gray-300 bg-gray-50 p-3 text-sm text-gray-900 outline disabled:cursor-not-allowed disabled:opacity-50 md:text-lg lg:text-xl rtl:text-right dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400"
        type="text"
        bind:value={inputLocation}
        on:keydown={pressEnter}
      />
  
      <button
        type="button"
        class="bg-primary-green hover:bg-primary-800 dark:bg-primary-600 dark:hover:bg-primary-700 focus-within:ring-primary-300 dark:focus-within:ring-primary-800 outline-secondary-green inline-flex items-center justify-center rounded-2xl px-4 py-2 text-center text-sm font-medium text-black outline focus-within:outline-none focus-within:ring-4 w-full sm:w-auto"
        on:click={updateMapUrl}
      >
        Search
      </button>
    </div>
  
    <!-- Iframe (Map) -->
    <div class="flex justify-center">
      <iframe
        class="w-full max-w-[550px] h-[350px] sm:h-[450px] lg:h-[550px] rounded-lg"
        src={$mapUrl}
        style="border:0"
        loading="lazy"
        allowfullscreen
        referrerpolicy="no-referrer-when-downgrade"
        title="Vietnamese Grocery stores nearby"
      ></iframe>
    </div>
  </div>