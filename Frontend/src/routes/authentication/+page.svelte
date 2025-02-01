<script lang="ts">
	import { goto } from '$app/navigation';
	import { userHandler } from '$lib/stores/userStore';

	let email = '';
	let username = '';
	let password = '';
	let phone_number = '';
	let errorMessage = '';

	async function handleRegister() {
		errorMessage = '';
		try {
			await userHandler.signup({
				email: email,
				username: username,
				password: password,
				phone_number: phone_number
			});
			goto('/login');
		} catch (error) {
			errorMessage = (error as Error).message;
		}
	}
</script>

<div class="flex h-screen items-center justify-center">
	<div class="w-full max-w-md rounded-lg bg-white p-8 shadow-md">
		<h2 class="mb-4 text-center text-2xl font-semibold text-yellow-400">Create Account</h2>

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
			type="text"
			bind:value={username}
			placeholder="Username"
			class="mb-3 w-full rounded-full border p-2"
		/>
		<input
			type="password"
			bind:value={password}
			placeholder="Password"
			class="mb-3 w-full rounded-full border p-2"
			required
		/>
		<input
			type="tel"
			bind:value={phone_number}
			placeholder="Phone number (+12063000000)"
			class="mb-3 w-full rounded-full border p-2"
		
		/>
		<button
			on:click={handleRegister}
			class="w-full rounded-full bg-yellow-400 py-2 font-bold text-white hover:bg-yellow-500"
		>
			Register
		</button>

		<p class="mt-3 text-center text-sm">
			Already have an account? <a
				href="/login"
				class="text-yellow-600 hover:underline">Login</a
			>
		</p>
	</div>
</div>
