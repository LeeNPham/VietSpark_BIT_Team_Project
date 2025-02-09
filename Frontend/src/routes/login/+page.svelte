<script lang="ts">
    import { goto } from '$app/navigation';
    import { userHandler } from '$lib/stores/userStore';

    let email = '';
    let password = '';
    let errorMessage = '';
    let isEmailValid = true;

    function validateEmail() {
        isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        if (!isEmailValid) errorMessage = "Please enter a valid email address";
        else errorMessage = "";
    }

    async function handleLogin() {
        validateEmail()
        if (!isEmailValid || !password) alert("Please fill in login credentials");
        try {
            await userHandler.login({email: email.toLowerCase(), password: password});
            goto('/'); // Redirect to a dashboard or home page

        } catch (error) {
            errorMessage = (error as Error).message;
            alert(errorMessage);
        }
    }
</script>
<main class="flex flex-col items-center justify-normal p-9">
    <div class="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
        <h1 class="py-4 sm:py-4 md:py-6 lg:py-8 text-center text-3xl sm:text-3xl md:text-4xl lg:text-6xl font-semibold text-secondary-forest">User Sign-In</h1>

        {#if errorMessage}
            <p class="text-red-500 text-sm mb-2">{errorMessage}</p>
        {/if}

        <input type="email" bind:value={email} placeholder="Email" class="mb-3 w-full rounded-full border p-2" required/>
        <input type="password" bind:value={password} placeholder="Password" class="mb-3 w-full rounded-full border p-2" required/>

        <button on:click={handleLogin} class="w-full rounded-full bg-secondary-green py-2 text-white">
            Login
        </button>

        <p class="mt-3 text-center text-xs sm:text-xs md:text-sm lg:text-sm">
            Don't have an account? <a href="/authentication" class="text-teal-600 hover:underline">Sign Up</a>
        </p>
    </div>
</main>