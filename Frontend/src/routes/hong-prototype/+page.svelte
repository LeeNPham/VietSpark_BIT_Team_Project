<script>
    	import { onMount } from "svelte";
	import { goto } from "$app/navigation";

	let authenticated  = false;
	
	onMount(() => {
		goto('/hong-prototype/home');
	});
	

</script>

<slot />