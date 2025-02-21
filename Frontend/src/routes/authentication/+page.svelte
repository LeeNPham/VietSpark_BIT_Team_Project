<script lang="ts">
	import { goto } from '$app/navigation';
	import { userHandler } from '$lib/stores/userStore';
	import { customStyles } from '$src/custom';

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

<div class={customStyles.authMain2}>
	<div class={customStyles.authDiv}>
		<h1 class={customStyles.userH1}> Create Account</h1>

		{#if errorMessage}
			<p class={customStyles.error}>{errorMessage}</p>
		{/if}

		<input
			type="email"
			bind:value={email}
			placeholder="Email"
			class={customStyles.input}
			required
		/>
		<input
			type="text"
			bind:value={username}
			placeholder="Username"
			class={customStyles.input}
		/>
		<input
			type="password"
			bind:value={password}
			placeholder="Password"
			class={customStyles.input}
			required
		/>
		<input
			type="tel"
			bind:value={phone_number}
			placeholder="Phone number (+12063000000)"
			class={customStyles.input}

		/>
		<button
			on:click={handleRegister}
			class="w-full rounded-full bg-secondary-green py-2 font-bold text-white hover:bg-yellow-500"
		>
			Register
		</button>

		<p class="mt-3 text-center text-sm">
			Already have an account? <a
				href="/login"
				class="text-secondary-forest font-bold hover:underline">Login</a
			>
		</p>
	</div>
</div>
