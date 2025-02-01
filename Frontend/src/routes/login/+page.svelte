<script lang="ts">
    import { goto } from '$app/navigation';
    import { userHandler } from '$lib/stores/userStore';

    let email = '';
    let password = '';
    let errorMessage = '';


    async function handleLogin() {
        errorMessage = '';
        if (!email || !password) alert("Please fill in login credentials");
        try {
            await userHandler.login({email: email, password: password});
            goto('/home'); // Redirect to a dashboard or home page

        } catch (error) {
            errorMessage = (error as Error).message;
            alert(errorMessage);
        }
    }
</script>

<div class="flex h-screen items-center justify-center">
    <div class="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold text-teal-600 mb-4 text-center">Login</h2>

        {#if errorMessage}
            <p class="text-red-500 text-sm mb-2">{errorMessage}</p>
        {/if}

        <input type="email" bind:value={email} placeholder="Email" class="w-full p-2 mb-3 border rounded-full" required/>
        <input type="password" bind:value={password} placeholder="Password" class="w-full p-2 mb-3 border rounded-full" required/>

        <button on:click={handleLogin} class="w-full bg-teal-600 text-white py-2 rounded-full hover:bg-teal-700">
            Login
        </button>

        <p class="mt-3 text-center text-sm">
            Don't have an account? <a href="/authentication" class="text-teal-600 hover:underline">Sign Up</a>
        </p>
    </div>
</div>