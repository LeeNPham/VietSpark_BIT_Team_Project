<script lang="ts">
	import { goto } from '$app/navigation';
	import { userHandler } from '$lib/stores/userStore';
	import { customStyles } from '$src/custom';
	import { showToast } from '$lib/stores/alertStore';

	let email = '';
	let userName = '';
	let password = '';
	let phoneNumber = '';
	let errorMessage = '';

	function validateEmail(email: string): boolean{
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email.trim()) {
            errorMessage = "Please enter an email address";
            return false;
        }
		if (!emailRegex.test(email)) {
            errorMessage = "Please enter a valid email address";
            return false;
        }
        errorMessage = '';
        return true;
    }

	function validatePassword(password: string): boolean {
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[a-zA-Z\d!@#$%^&*]{8,}$/;
        // const passwordRegex = /^[a-zA-Z0-9]{6,}$/;
        if (!password.trim()) {
            errorMessage = "Please enter a password";
            return false;
        }
        if (!passwordRegex.test(password)) {
            errorMessage = "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character";
            return false;
        }
        errorMessage = '';
        return true;
    }

	function validateUsername(userName: string): boolean {
        const usernameRegex = /^[a-zA-Z0-9]{4,}$/;
		if (!userName.trim()) {
			errorMessage = "Please enter a username";
			return false;
		} 
		if (!usernameRegex.test(userName)) {
			errorMessage = "Username must be at least 6 characters long and contain alphanumeric characters only";
			return false;
		}
		errorMessage = '';
		return true;
	}

	function validatePhoneNumber(phoneNumber: string): boolean {
		const phoneNumberRegex = /^\d{10}$/;
		if (!phoneNumber.trim()) {
			errorMessage = "Please enter a phone number";
			return false;
		}
		if (!phoneNumberRegex.test(phoneNumber)) {
			errorMessage = "Phone number must be 10 digits long";
			return false;
		}
		errorMessage = '';
		return true;
	}

	async function handleRegister() {
		if (!validateEmail(email)){
			// showToast('error', errorMessage);
			return;
		}
		if (!validateUsername(userName)){
			// showToast('error', errorMessage);
			return;
		}
		if (!validatePassword(password)){
			// showToast('error', errorMessage);
			return;
		}
		if (!validatePhoneNumber(phoneNumber)){
			// showToast('error', errorMessage);
			return;
		}
		errorMessage = '';
		try {
			await userHandler.signup({
				email: email,
				userName: userName,
				password: password,
				phoneNumber: "+1" + phoneNumber,
			});
			showToast('success', 'Account created successfully!');
			goto('/');
		} catch (error) {
			errorMessage = (error as Error).message;
		}
	}
</script>

<div class={customStyles.authMain2}>
	<div class={customStyles.authDiv}>
		<h1 class={customStyles.userH1}>Sign Up</h1>

		{#if errorMessage}
			<p class={customStyles.error}>{errorMessage}</p>
		{/if}

		<input
			type="email"
			bind:value={email}
			placeholder="Email"
			class={customStyles.input}
			required
		/>
		<input
			type="text"
			bind:value={userName}
			placeholder="Username"
			class={customStyles.input}
		/>
		<input
			type="password"
			bind:value={password}
			placeholder="Password"
			class={customStyles.input}
			required
		/>
		<input
			type="tel"
			bind:value={phoneNumber}
			placeholder="Phone number (2063000000)"
			class={customStyles.input}

		/>
		<button
			on:click={handleRegister}
			class="w-full rounded-full bg-secondary-green py-2 font-bold text-white hover:bg-yellow-500"
		>
			Register
		</button>

		<p class="mt-3 text-center text-sm">
			Already have an account? <a
				href="/login"
				class="text-secondary-forest font-bold hover:underline">Login</a
			>
		</p>
	</div>
</div>
