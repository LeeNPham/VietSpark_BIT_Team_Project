<script>
    	import { onMount } from "svelte";
	import { goto } from "$app/navigation";

	let authenticated  = false;
	
	onMount(() => {
		// authenticated = localStorage.getItem('authenticated') === 'true';
		authenticated = true;
		goto('/hong-prototype/home');
	});
	
	// if(authenticated) {
	// 	goto('/hong-prototype/home');
	// } else {
	// 	goto('/hong-prototype/login');
	// }

</script>

<slot />