<script>
	import { Button } from "flowbite-svelte";
    export let onclose;
</script>

<div class="modal-overlay fixed inset-0 bg-teal-900 flex items-center justify-center z-100">
    <div class="modal-content bg-white p-8 w-3/4 max-w-3xl h-3/4 rounded shadow-lg relative">
        <Button
            class="absolute top-2 right-2 rounded-full bg-white px-3 py-1 text-teal-600 hover:bg-white hover:text-teal-600 hover:outline-none focus:outline-none"
            onclick={onclose}
        >
            X
        </Button>
        <slot></slot>
    </div>
</div>

<style>
    .modal-overlay {
        backdrop-filter: blur(5px);
    }

    .modal-content {
        height: auto; /* Height adjusts to content */
        max-height: 90vh; /* Maximum height to prevent modal from being too tall */
        overflow-y: auto; /* Enable scrolling if content exceeds max height */
    }
</style>