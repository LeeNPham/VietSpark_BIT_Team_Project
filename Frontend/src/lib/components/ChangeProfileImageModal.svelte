<script lang="ts">
    import { userHandler, userStore } from '$lib/stores/userStore';

    export let showProfileImageModal: boolean;
    export let toggleProfileImageModal: () => void;
    let profileImageURL: string | undefined;
    let profileImageFile: File | null = null;
    let profileImagePreview: string | null = null;
    let user

    userStore.subscribe((store) => {
        user = store?.currentUser;
        profileImageURL = store?.currentUser?.profileImageURL;
<<<<<<< HEAD
<<<<<<< HEAD
=======
        console.log("imgURL" ,profileImageURL)
>>>>>>> fd1430c (Add creation time to new recipes, enhance user profile image handling, and streamline token verification)
=======
        console.log("imgURL" ,profileImageURL)
>>>>>>> a9d9892 (Add creation time to new recipes, enhance user profile image handling, and streamline token verification)
    });

    async function uploadProfileImage() {
        try {
            if (!profileImageFile) throw new Error('No file selected');
            const imageUrl = await userHandler.uploadProfileImage(profileImageFile);
            profileImageURL = `${imageUrl}?${new Date().getTime()}`;
            // profileImageURL = imageUrl;
            userStore.update((store) => {
                if (store.currentUser) {
                    if (profileImageURL) {
                        store.currentUser.profileImageURL = profileImageURL;
                    }
                }
                return store;
            });
            toggleProfileImageModal();
        } catch (e) {
            alert((e as Error).message);
        }
    }

    function handleFileChange(e: Event) {
        const target = e.target as HTMLInputElement;
        if (target && target.files) {
            profileImageFile = target.files[0];
            profileImagePreview = URL.createObjectURL(profileImageFile);
        }
    }
</script>

{#if showProfileImageModal}
<div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-80">
        <!-- <h2 class="text-xl font-bold mb-4">Upload Profile Image</h2> -->
        <div class="custom-file-input">
            <input type="file" accept="image/*" id="fileInput" on:change={handleFileChange} />
            <label for="fileInput" class="custom-file-label">Choose File</label>
        </div>
        {#if profileImagePreview}
            <div class="mt-4">
                <img src={profileImagePreview} alt="" class="w-full h-auto rounded-lg" />
            </div>
        {/if}
        <div class="mt-4 flex justify-between">
            <button class="bg-primary-gray outline-secondary-green rounded-2xl text-lg text-gray-800 outline" on:click={toggleProfileImageModal}>Cancel</button>
            <button class="bg-primary-orange outline-secondary-green rounded-2xl text-lg text-gray-800 outline" on:click={uploadProfileImage}>Upload</button>
        </div>
    </div>
</div>
{/if}

<style>
    .custom-file-input {
        position: relative;
        width: 100%;
        height: 40px;
    }
    .custom-file-input input[type="file"] {
        position: absolute;
        width: 100%;
        height: 100%;
        opacity: 0;
        cursor: pointer;
    }
    .custom-file-label {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        background-color: #f3f4f6;
        border: 2px dashed #d1d5db;
        border-radius: 0.375rem;
        color: #6b7280;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.2s, color 0.2s;
    }
    .custom-file-label:hover {
        background-color: #e5e7eb;
        color: #374151;
    }
</style>