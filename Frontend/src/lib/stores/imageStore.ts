const API_URL = import.meta.env.VITE_API_URL;

export const imageHandler = {
    uploadFile: async (image: File) => {
        const idToken = localStorage.getItem('idToken');
        if (!idToken) {throw new Error("User is not signed in");};
        const savePath = `images/${image.name}`;
        try {
            const formData = new FormData();
            formData.append("file", image);
            const res = await fetch(`${API_URL}/upload-image/file?id_token=${idToken}&save_path=${savePath}`, {
                method: "POST",
                body: formData,
            });
            console.log(savePath)

            if (!res.ok) throw new Error("Failed to upload image");
            const imageUrl = await res.json();
            return imageUrl;
        } catch (e) {
            console.error("Image upload failed", (e as Error).message);
            throw e;
        }
    },

    generateImage: async (description: string) => {
        try {
            if (!description.trim()) throw new Error("Image description is required");
            description = description.trim();
            const res = await fetch(`${API_URL}/generate-image?item=${description }`);
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
    }
} 
