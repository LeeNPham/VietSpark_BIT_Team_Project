<script lang="ts">
    import { goto } from '$app/navigation';
	import { showToast } from '$lib/stores/alertStore';
    import { userHandler } from '$lib/stores/userStore';
    import { customStyles } from '$src/custom';
    import { HomeSolid } from 'flowbite-svelte-icons';


    let email = '';
    let password = '';
    let errorMessage = '';

    function validateEmail(email: string): boolean{
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email.trim() || !emailRegex.test(email)) {
            errorMessage = "Please enter an email address";
            return false;
        }
        errorMessage = '';
        return true;
    }

    function validatePassword(password: string): boolean {
        // const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        // const passwordRegex = /^[a-zA-Z0-9]{6,}$/;
        if (!password.trim()) {
            errorMessage = "Please enter a password";
            return false;
        }
        // if (!passwordRegex.test(password)) {
        //     errorMessage = "Password must be at least 6 characters long and contain alphanumeric characters only";
        //     return false;
        // }
        errorMessage = '';
        return true;
    }

    async function handleLogin() {
        if (!validateEmail(email)){
            // showToast('error', errorMessage);
            return;
        }
        if (!validatePassword(password)){
            // showToast('error', errorMessage);
            return;
        }
        try {
            await userHandler.login({email: email.toLowerCase(), password: password});
            showToast('success', 'Login successful!');
            goto('/'); // Redirect to a dashboard or home page

        } catch (error) {
            errorMessage = (error as Error).message;
            showToast("error", errorMessage);
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
            <h1 class={customStyles.userH1}>Welcome Back!</h1>
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