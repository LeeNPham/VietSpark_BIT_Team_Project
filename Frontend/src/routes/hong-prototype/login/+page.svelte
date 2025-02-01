<script lang="ts">
	import { goto } from '$app/navigation';
	import { userHandler } from '../stores/userStore';

	let email = '';
	let password = '';
	let errorMessage = '';

	async function handleLogin() {
		errorMessage = '';
		if (!email || !password) alert('Please fill in login credentials');
		try {
			await userHandler.login({ email: email, password: password });
			goto('/hong-prototype/home'); // Redirect to a dashboard or home page
		} catch (error) {
			errorMessage = (error as Error).message;
			alert(errorMessage);
		}
	}
</script>

<main class="flex flex-col items-center justify-normal p-9">
	<h1
		class="text-secondary-forest py-4 text-center text-3xl font-semibold sm:py-4 sm:text-3xl md:py-6 md:text-4xl lg:py-8 lg:text-6xl"
	>
		User Sign-In
	</h1>
	<img
		src="/home.jpg"
		class="w-1/2 py-4 sm:w-1/2 sm:py-4 md:w-1/3 md:py-6 lg:w-1/4 lg:py-8"
		alt="A cartoon of a Black, woman chef making cupcakes in the kitchen."
	/>

	<div
		class="bg-primary-orange outline-secondary-green w-full max-w-md rounded-lg p-8 py-4 shadow-md outline sm:py-4 md:py-6 lg:py-8"
	>
		<h2 class=" text-secondary-forest mb-4 text-center text-2xl font-semibold">Login</h2>

		{#if errorMessage}
			<p class="mb-2 text-sm text-red-500">{errorMessage}</p>
		{/if}

		<input
			type="email"
			bind:value={email}
			placeholder="Email"
			class="mb-3 w-full rounded-full border p-2"
			required
		/>
		<input
			type="password"
			bind:value={password}
			placeholder="Password"
			class="mb-3 w-full rounded-full border p-2"
			required
		/>

		<button on:click={handleLogin} class="bg-secondary-green w-full rounded-full py-2 text-white">
			Login
		</button>

		<p class="mt-3 text-center text-xs sm:text-xs md:text-sm lg:text-sm">
			Don't have an account? <a
				href="/hong-prototype/authentication"
				class="text-secondary-forest font-semibold hover:underline">Sign Up</a
			>
		</p>
	</div>
</main>
