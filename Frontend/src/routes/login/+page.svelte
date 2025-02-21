<script lang="ts">
    import { goto } from '$app/navigation';
    import { userHandler } from '$lib/stores/userStore';
    import { customStyles } from '$src/custom';
    import { HomeSolid } from 'flowbite-svelte-icons';


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
<main>
    <div class="flex justify-center p-4 mb-10">
        <a href="/" class="w-12 h-12 justify-center text-secondary-forest">
            <HomeSolid class="w-12 h-12" /> Home
        </a>
    </div>
    <div class={customStyles.authMain}>
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
                Don't have an account? <a href="/authentication" class="text-secondary-forest hover:underline">Sign Up</a>
            </p>
        </div>
    </div>
</main>