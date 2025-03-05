import { writable } from "svelte/store";
import type { ReviewAddDTO, ReviewDTO } from "$lib/types";

const API_URL = import.meta.env.VITE_API_URL;

interface ReviewState {
    isLoading: boolean;
    reviews: ReviewDTO[];
}
export const reviewStore = writable<ReviewState>({
    isLoading: true,
    reviews: [],
});

export const reviewHandler = {
    getReviews: async (recipeId: string, review_id: string | null,  rating: number | null, has_image: boolean | null) => {
        try {
            reviewStore.update((state) => ({
                ...state,
                isLoading: true,
            }));
            const queryParams = new URLSearchParams();
            if (review_id) queryParams.append("review_id", review_id);
            if (rating !== null) queryParams.append("rating", rating.toString());
            if (has_image !== null) queryParams.append("has_image", has_image.toString());
            
            const queryParamsString = queryParams.toString() ? `?${queryParams.toString()}` : "";
            
            const res = await fetch(`${API_URL}/reviews/${recipeId}${queryParamsString}`);
            const reviews = await res.json();
            if (!res.ok) throw new Error(reviews?.detail || res.statusText);
            reviewStore.update((state) => ({
                ...state,
                isLoading: false,
                reviews: reviews as ReviewDTO[],
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

    submitReview: async (reviewData: ReviewAddDTO) => {
        const idToken = localStorage.getItem('idToken');
        if (!idToken) { throw new Error("User is not signed in"); }
        try {
            const url = `${API_URL}/reviews?id_token=${idToken}`;
            const res = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // 'Authorization': `Bearer ${idToken}`,
                },
                body: JSON.stringify(reviewData),
            });

            const newReviews = await res.json();
            if (!res.ok) throw new Error(newReviews?.detail || 'Failed to submit review');
            
            
            reviewHandler.getReviews(reviewData.recipe_id, null, null, null);
        } catch (error) {
            console.error("Error submitting review", error);
            throw error
        }
    },
};