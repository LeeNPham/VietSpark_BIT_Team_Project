<script>
    import { goto } from '$app/navigation';

    let email = '';
    let password = '';
    let errorMessage = '';

    const API_URL = import.meta.env.VITE_API_URL;

    async function handleLogin() {
        errorMessage = '';
        try {
            const res = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            if (!res.ok) {
                throw new Error('Invalid credentials. Please try again.');
            }

            const data = await res.json();
            console.log(data)
            alert('Login successful! Redirecting...');
            document.cookie = `authToken=${data.token}; path=/; Secure; HttpOnly`; // Using Cookies
            localStorage.setItem('authToken', data.idToken); // Using localStorage
            localStorage.setItem('authenticated', 'true'); // Mark user as authenticated
            localStorage.setItem('userId', data.localId); // Mark user as authenticated
            goto('/hong-prototype/home'); // Redirect to a dashboard or home page

        } catch (error) {
            errorMessage = error.message;
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

        <input type="email" bind:value={email} placeholder="Email" class="w-full p-2 mb-3 border rounded-full" />
        <input type="password" bind:value={password} placeholder="Password" class="w-full p-2 mb-3 border rounded-full" />

        <button on:click={handleLogin} class="w-full bg-teal-600 text-white py-2 rounded-full hover:bg-teal-700">
            Login
        </button>

        <p class="mt-3 text-center text-sm">
            Don't have an account? <a href="/hong-prototype/authentication" class="text-teal-600 hover:underline">Sign Up</a>
        </p>
    </div>
</div>