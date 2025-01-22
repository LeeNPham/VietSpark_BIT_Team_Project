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

<div class="flex h-screen items-center justify-center">
    <div class="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold text-yellow-400 mb-4 text-center">Create Account</h2>

        {#if errorMessage}
            <p class="text-red-500 text-sm mb-2">{errorMessage}</p>
        {/if}

        <input type="email" bind:value={email} placeholder="Email" class="w-full p-2 mb-3 border rounded-full" />
        <input type="text" bind:value={username} placeholder="Username" class="w-full p-2 mb-3 border rounded-full" />
        <input type="password" bind:value={password} placeholder="Password" class="w-full p-2 mb-3 border rounded-full" />

        <button on:click={handleRegister} class="w-full bg-yellow-400 text-white py-2 rounded-full hover:bg-yellow-500 font-bold">
            Register
        </button>

        <p class="mt-3 text-center text-sm">
            Already have an account? <a href="/hong-prototype/login" class="text-yellow-600 hover:underline">Login</a>
        </p>
    </div>
</div>
