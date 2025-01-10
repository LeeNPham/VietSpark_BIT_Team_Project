<script>
	let email = '';
	let password = '';
	let errorMessage = '';

	async function handleLogin() {
		// Simple validation for email and password
		if (!email || !password) {
			errorMessage = 'Both fields are required.';
			return;
		}

		// You can replace this with an actual API call to log in
		if (email && password) {
			try {
				// Make the API call to the FastAPI backend for authentication
				const response = await fetch('http://localhost:8000/login', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({ email, password })
				});

				// Check if the response is successful (status code 2xx)
				if (response.ok) {
					// Handle successful login
					const data = await response.json();
					alert('Login successful!');
					console.log('login successful'); // You can store the token for session management
				} else {
					// Handle failed login (invalid credentials, etc.)
					const errorData = await response.json();
					errorMessage = errorData.detail || 'Invalid email or password.';
				}
			} catch (error) {
				// Handle network errors or other unexpected issues
				errorMessage = 'An error occurred. Please try again later.';
				console.error('Error during login:', error);
			}
		} else {
			errorMessage = 'Invalid email or password.';
		}
	}
</script>

<div class="login-container">
	<h2>Login</h2>

	<input class="input" type="email" placeholder="Email" bind:value={email} />

	<input class="input" type="password" placeholder="Password" bind:value={password} />

	{#if errorMessage}
		<div class="error">{errorMessage}</div>
	{/if}

	<button class="btn" on:click={handleLogin}>Log in</button>
</div>

<style>
	.login-container {
		max-width: 400px;
		margin: 100px auto;
		padding: 20px;
		border-radius: 8px;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
		background-color: #fff;
	}

	.input {
		width: 100%;
		padding: 10px;
		margin: 10px 0;
		border-radius: 4px;
		border: 1px solid #ccc;
	}

	.btn {
		width: 100%;
		padding: 10px;
		background-color: #007bff;
		color: #fff;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}

	.btn:hover {
		background-color: #0056b3;
	}

	.error {
		color: red;
		font-size: 12px;
		margin-top: 10px;
	}
</style>
