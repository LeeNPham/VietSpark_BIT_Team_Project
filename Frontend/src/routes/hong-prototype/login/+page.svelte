<script lang="ts">
    import { goto } from '$app/navigation';

	let email = '';
	let password = '';
	let errorMessage = '';

	const API_URL = import.meta.env.VITE_API_URL;

	async function handleLogin() {
		errorMessage = '';
		try {
			const res = await fetch(`${API_URL}/login`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, password })
			});

			if (!res.ok) {
				throw new Error('Invalid credentials. Please try again.');
			}

            const data = await res.json();
            console.log(data)
            document.cookie = `authToken=${data.token}; path=/; Secure; HttpOnly`; // Using Cookies
            localStorage.setItem('authToken', data.idToken); // Using localStorage
            localStorage.setItem('authenticated', 'true'); // Mark user as authenticated
            localStorage.setItem('userId', data.localId); // Mark user as authenticated
            goto('/hong-prototype/home'); // Redirect to a dashboard or home page

        } catch (error) {
            errorMessage = (error as Error).message;
            alert(errorMessage);
        }
    }
</script>

<main class="flex flex-col items-center justify-normal p-9">
	<h1 class="py-4 sm:py-4 md:py-6 lg:py-8 text-center text-3xl sm:text-3xl md:text-4xl lg:text-6xl font-semibold text-secondary-forest">User Sign-In</h1>
	<img
		src="/home.jpg"
		class="py-4 sm:py-4 md:py-6 lg:py-8 w-1/2 sm:w-1/2 md:w-1/3 lg:w-1/4"
		alt="A cartoon of a Black, woman chef making cupcakes in the kitchen."
	/>

	<div class="p-8 py-4 sm:py-4 md:py-6 lg:py-8 w-full max-w-md rounded-lg bg-primary-orange shadow-md outline outline-secondary-green">
		<h2 class=" mb-4 text-center text-2xl text-secondary-forest font-semibold">Login</h2>

		{#if errorMessage}
			<p class="mb-2 text-sm text-red-500">{errorMessage}</p>
		{/if}

		<input
			type="email"
			bind:value={email}
			placeholder="Email"
			class="mb-3 w-full rounded-full border p-2"
		/>
		<input
			type="password"
			bind:value={password}
			placeholder="Password"
			class="mb-3 w-full rounded-full border p-2"
		/>

		<button on:click={handleLogin} class="w-full rounded-full bg-secondary-green py-2 text-white">
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
