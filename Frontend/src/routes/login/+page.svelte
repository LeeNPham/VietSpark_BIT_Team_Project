<script lang="ts">
    import { goto } from '$app/navigation';
    import { userHandler } from '$lib/stores/userStore';
    import { customStyles } from '$src/custom';

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
<main class={customStyles.authMain}>
    <div class={customStyles.authDiv}>
        <h1 class={customStyles.userH1}>User Sign-In</h1>

        {#if errorMessage}
            <p class={customStyles.error}>{errorMessage}</p>
        {/if}

        <input type="email" bind:value={email} placeholder="Email" class={customStyles.input} required/>
        <input type="password" bind:value={password} placeholder="Password" class={customStyles.input} required/>

        <button on:click={handleLogin} class="w-full rounded-full bg-secondary-green py-2 text-white">
            Login
        </button>

        <p class="mt-3 text-center text-xs sm:text-xs md:text-sm lg:text-sm">
            Don't have an account? <a href="/authentication" class="text-teal-600 hover:underline">Sign Up</a>
        </p>
    </div>
</main>