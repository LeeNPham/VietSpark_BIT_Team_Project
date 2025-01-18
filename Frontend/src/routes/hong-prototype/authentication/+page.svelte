<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    let email = '';
    let username = '';
    let password = '';
    let errorMessage = '';

    async function handleRegister() {
        errorMessage = '';
        try {
            const res = await fetch('https://vietsparktest1.vercel.app/authentication', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, username, password }),
            });

            if (!res.ok) {
                throw new Error('Failed to create account. Please try again.');
            }

            const data = await res.json();
            alert('Account created successfully! Redirecting to login...');
            goto('/login'); // Redirect to login page

        } catch (error) {
            errorMessage = error.message;
        }
    }
</script>

<div class="flex h-screen items-center justify-center">
    <div class="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold text-indigo-600 mb-4 text-center">Create Account</h2>

        {#if errorMessage}
            <p class="text-red-500 text-sm mb-2">{errorMessage}</p>
        {/if}

        <input type="email" bind:value={email} placeholder="Email" class="w-full p-2 mb-3 border rounded" />
        <input type="text" bind:value={username} placeholder="Username" class="w-full p-2 mb-3 border rounded" />
        <input type="password" bind:value={password} placeholder="Password" class="w-full p-2 mb-3 border rounded" />

        <button on:click={handleRegister} class="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700">
            Register
        </button>

        <p class="mt-3 text-center text-sm">
            Already have an account? <a href="/hong-prototype/login" class="text-indigo-600 hover:underline">Login</a>
        </p>
    </div>
</div>
