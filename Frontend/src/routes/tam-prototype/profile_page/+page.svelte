<script>
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
  
    // Check if the user is logged in by checking for tokens in localStorage
    let isLoggedIn = false;
  
    // This runs when the component mounts
    onMount(() => {
      const idToken = localStorage.getItem("idToken");
      if (idToken) {
        isLoggedIn = true;
      } else {
        // If not logged in, redirect to login page
        goto("/tam-prototype"); // Redirect to login page
      }
    });
  </script>
  
  {#if isLoggedIn}
    <!-- Profile page content -->
    <div class="profile-container">
      <h2>Your Profile</h2>
      <p>Welcome to your profile page!</p>
      <!-- Add additional profile-related content here -->
    </div>
  {:else}
    <!-- You could optionally show a loading spinner or redirect here -->
    <div>Loading...</div>
  {/if}
  
  <style>
    .profile-container {
      max-width: 600px;
      margin: 100px auto;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      background-color: #fff;
    }
  
    h2 {
      font-size: 2rem;
      margin-bottom: 20px;
    }
  </style>
  