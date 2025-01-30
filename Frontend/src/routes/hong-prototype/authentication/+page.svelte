<script>
    import { goto } from '$app/navigation';

    let email = '';
    let username = '';
    let password = '';
    let errorMessage = '';

    const API_URL = import.meta.env.VITE_API_URL;

    async function handleRegister() {
        errorMessage = '';
        try {
            const res = await fetch(`${API_URL}/authentication`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, username, password }),
            });

            if (!res.ok) {
                throw new Error('Failed to create account. Please try again.');
            }

            const data = await res.json();
            alert('Account created successfully! Redirecting to login...');
            goto('/hong-prototype/login');

        } catch (error) {
            errorMessage = error.message;
            alert(errorMessage);
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
            <p class="text-red-500 text-sm mb-2">{errorMessage}</p>
        {/if}

        <input type="email" bind:value={email} placeholder="Email" class="w-full p-2 mb-3 border rounded-full" />
        <input type="text" bind:value={username} placeholder="Username" class="w-full p-2 mb-3 border rounded-full" />
        <input type="password" bind:value={password} placeholder="Password" class="w-full p-2 mb-3 border rounded-full" />

        <button on:click={handleRegister} class="w-full bg-secondary-green text-white py-2 rounded-full hover:bg-yellow-500 font-bold">
            Register
        </button>

        <p class="mt-3 text-center text-xs sm:text-xs md:text-sm lg:text-sm">
            Already have an account? <a href="/hong-prototype/login" class="text-secondary-forest hover:underline">Login</a>
        </p>
    </div>
</div>
