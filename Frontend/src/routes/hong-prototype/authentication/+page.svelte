<script lang="ts">
	import { goto } from '$app/navigation';
	import { userHandler } from '../stores/userStore';

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
			goto('/hong-prototype/login');
		} catch (error) {
			errorMessage = (error as Error).message;
		}
	}
</script>

<div class="flex flex-col items-center justify-normal p-9">
    <img
		src="/home.jpg"
		class="py-4 sm:py-4 md:py-6 lg:py-8 w-1/2 sm:w-1/2 md:w-1/3 lg:w-1/4"
		alt="A cartoon of a Black, woman chef making cupcakes in the kitchen."
	/>

    <div class="p-8 py-4 sm:py-4 md:py-6 lg:py-8 w-full max-w-md bg-primary-orange rounded-lg shadow-md outline outline-secondary-green">
        <h2 class="mb-4 text-center text-2xl font-semibold text-secondary-forest ">Create Account</h2>

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
			placeholder="Phone number"
			class="mb-3 w-full rounded-full border p-2"
		
		/>
        <button on:click={handleRegister} class="w-full bg-secondary-green text-white py-2 rounded-full hover:bg-yellow-500 font-bold">
            Register
        </button>

        <p class="mt-3 text-center text-xs sm:text-xs md:text-sm lg:text-sm">
            Already have an account? <a href="/hong-prototype/login" class="text-secondary-forest hover:underline">Login</a>
        </p>
    </div>
</div>
