<script>
    import { writable } from 'svelte/store';
    const gApiKey = import.meta.env.VITE_GMAP_API_KEY;
    
    let mapUrl = writable(`https://www.google.com/maps/embed/v1/search?key=${gApiKey}&q=asian+vietnamese+grocery+stores`);
    let inputLocation = '';

    function updateMapUrl() {
        mapUrl.set(`https://www.google.com/maps/embed/v1/search?key=${gApiKey}&q=asian+vietnamese+grocery+stores+near+${inputLocation}`);
    }
    // @ts-ignore
    function pressEnter(event) {
        if (event.key === "Enter") { updateMapUrl}
    } 
</script>

<div class="mb-4 flex space-x-4">
    <input 
        aria-label="search-input-box" 
        placeholder="Enter location or zipcode" 
        class="block w-full disabled:cursor-not-allowed disabled:opacity-50 rtl:text-right p-2.5 focus:border-primary-500 focus:ring-primary-500 dark:focus:border-primary-500 dark:focus:ring-primary-500 bg-gray-50 text-gray-900 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 border border-gray-300 dark:border-gray-600 outline-secondary-green sm: rounded-2xl text-sm outline md:text-lg lg:text-xl" 
        type="text"
        bind:value={inputLocation}
        on:keydown={pressEnter}
    />

    <button 
        type="button" 
        class="text-center font-medium focus-within:ring-4 focus-within:outline-none inline-flex items-center justify-center hover:bg-primary-800 dark:bg-primary-600 dark:hover:bg-primary-700 focus-within:ring-primary-300 dark:focus-within:ring-primary-800 bg-primary-green outline-secondary-green rounded-2xl p-2 text-sm text-black outline"
        on:click={updateMapUrl}
    >Search
    </button>
</div>

<div class="flex">
    <iframe
        width="500"
        height="500"
        src={$mapUrl}
        style="border:0"
        loading="lazy"
        allowfullscreen
        referrerpolicy="no-referrer-when-downgrade"
        title="Vietnamese Grocery stores nearby"
    ></iframe>
</div>