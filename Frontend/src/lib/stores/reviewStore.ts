import { writable } from "svelte/store";
const API_URL = import.meta.env.VITE_API_URL;

export const reviewStore = writable({
    isLoading: true,
    reviews: [],
    currentReview: null,
    currentIndex: -1,
});
export const reviewHandler = {
    getReviews: async (recipeId: string) => {
        try {
            reviewStore.update((state) => ({
                ...state,
                isLoading: true,
            }));
            const res = await fetch(`${API_URL}/reviews/${recipeId}`);
            const reviews = await res.json();
            if (!res.ok) throw new Error(reviews?.detail || res.statusText);
            reviewStore.update((state) => ({
                ...state,
                isLoading: false,
                reviews: reviews,
            }));
        } catch (e) {
            console.error((e as Error).message);
            reviewStore.update((state) => ({
                ...state,
                isLoading: false,
                reviews: [],
            }));
            throw e;
        }
    },
    getReview: async (reviewId: string) => {
        try {
            reviewStore.update((state) => ({
                ...state,
                isLoading: true,
            }));
            const res = await fetch(`${API_URL}/reviews/${reviewId}`);
            const review = await res.json();
            if (!res.ok) throw new Error(review?.detail || res.statusText);
            reviewStore.update((state) => ({
                ...state,
                isLoading: false,
                currentReview: review,
            }));
        } catch (e) {
            console.error((e as Error).message);
            reviewStore.update((state) => ({
                ...state,
                isLoading: false,
                currentReview: null,
            }));
            throw e;
        }
    },

    submitReviews: async (recipeId: string, rating: number, reviewText: string, reviewImages: File[], reviewVideo: File) => {
        // TODO: Implement this function
        const idToken = localStorage.getItem('idToken');
        if (!idToken) { throw new Error("User is not signed in"); }
        try {
            const url = `${API_URL}/reviews/${recipeId}`;
            const formData = new FormData();
            formData.append('rating', rating.toString());
            formData.append('reviewText', reviewText);
            if (reviewImages.length > 0) {
                reviewImages.forEach((image) => {
                    formData.append('reviewImages', image);
                });
            }

            if (reviewVideo) {
                formData.append('reviewVideo', reviewVideo);
            }

            const res = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (!res.ok) throw new Error(res.statusText || 'Failed to submit review');
            const newReviews = await res.json();
            reviewStore.update((state) => ({
                ...state,
                reviews: newReviews
            }))
            return newReviews;
        } catch (error) {
            console.error("Error submitting review", error);
            throw error
        }
    },
};