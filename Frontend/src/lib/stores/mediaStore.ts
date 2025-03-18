const API_URL = import.meta.env.VITE_API_URL;

export const mediaHandler = {
    uploadImage: async (image: File) => {
        const idToken = localStorage.getItem('idToken');
        if (!idToken) { throw new Error("User is not signed in"); };
        const savePath = `images/${image.name}`;
        try {
            const formData = new FormData();
            formData.append("file", image);
            const res = await fetch(`${API_URL}/upload-image/file?id_token=${idToken}&save_path=${savePath}`, {
                method: "POST",
                body: formData,
            });

            if (!res.ok) throw new Error("Failed to upload image");
            const imageUrl = await res.json();
            return imageUrl;
        } catch (e) {
            console.error("Image upload failed", (e as Error).message);
            throw e;
        }
    },

    uploadVideo: async (video: File) => {
        const idToken = localStorage.getItem('idToken');
        if (!idToken) { throw new Error("User is not signed in"); };
        const savePath = `videos/${video.name}`;
        try {
            const formData = new FormData();
            formData.append("file", video);
            const res = await fetch(`${API_URL}/upload-video/file?id_token=${idToken}&save_path=${savePath}`, {
                method: "POST",
                body: formData,
            });

            if (!res.ok) throw new Error("Failed to upload video");
            const videoUrl = await res.json();
            return videoUrl;
        } catch (e) {
            console.error("Video upload failed", (e as Error).message);
            throw e;
        }
    },

    deleteMedia: async (mediaUrl: string) => {
        const idToken = localStorage.getItem('idToken');
        if (!idToken) { throw new Error("User is not signed in"); }
        if (!mediaUrl) { throw new Error("Media URL is required"); }
        try {
            const res = await fetch(`${API_URL}/media?url=${mediaUrl}&id_token=${idToken}`)

            if (!res.ok) throw new Error("Failed to delete media");
            return await res.json();
        } catch (e) {
            console.error("Delete media failed", (e as Error).message);
            throw e;
        }
    },

    generateImage: async (description: string) => {
        try {
            if (!description.trim()) throw new Error("Image description is required");
            description = description.trim();
            const res = await fetch(`${API_URL}/generate-image?item=${description}`);
            if (!res.ok) throw new Error(`Cannot generate new image with description ${description}`);

            const imageUrl = await res.json();
            return imageUrl;
        } catch (e) {
            console.error("Generate image failed", (e as Error).message);
            throw e;
        }
    },

    getImageUrl: async (imageName: string) => {
        try {
            const res = await fetch(`${API_URL}/get_image_url/${imageName}`);
            if (!res.ok) throw new Error("Cannot find the image with name " + imageName);
            const imageUrl = await res.json();
            return imageUrl;

        } catch (e) {
            console.error("Get image failed", (e as Error).message);
            throw e;
        }
    },


} 
