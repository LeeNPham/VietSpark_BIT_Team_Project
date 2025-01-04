<script>
    import { Modal } from "flowbite-svelte";
    import RecipeDetail from "./RecipeDetail.svelte";
    
    let { item } = $props();  // Props passed into the component
    let isModalOpen = false;  // Directly manage modal state as a regular variable

    function toggleModal() {
        console.log('isModalOpen before toggle:', isModalOpen);  // Log state before toggle
        isModalOpen = !isModalOpen;  // Toggle modal state
        console.log('isModalOpen after toggle:', isModalOpen);  // Log state after toggle
    }
</script>

<div class="items-center gap-4 mb-4 bg-white rounded-lg p-4" onclick={toggleModal}>
    <img 
        src={item.src} 
        alt="Dish image" 
        class="w-16 h-16 rounded-lg object-cover" 
    />
    <div>
        <div class="text-sm text-blue-700 font-medium space-x-2">
            <span>{item.prepTime} Min.</span>
            <span>*</span>
            <span>{item.numIngredients} ingredients</span>
        </div>
        <h3 class="font-semibold text-blue-500 mt-1">{item.description}</h3>
    </div>
</div>

{#if isModalOpen}  <!-- Use the variable directly in the template -->
    <Modal on:close={toggleModal}>
        <RecipeDetail {item}/>
    </Modal>
{/if}
