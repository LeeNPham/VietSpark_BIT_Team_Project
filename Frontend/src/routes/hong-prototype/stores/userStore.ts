import { writable } from "svelte/store";
import type { UserDTO, UserLoginDTO, UserSignUpDTO } from "../types";

const API_URL = import.meta.env.VITE_API_URL;


export const userStore = writable({
    isLoading: true,
    useId: "",
    currentUser: null as UserDTO | null,
});


export const userHandler = {
    login: async (userData: UserLoginDTO) => {
        try {
            const res = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(userData),
            });

            if (!res.ok) throw new Error("Failed to login");

            const newUser = await res.json();
            document.cookie = `authToken=${newUser.token}; path=/; Secure; HttpOnly`; // Using Cookies
            localStorage.setItem('authToken', newUser.idToken); // Using localStorage
            localStorage.setItem('authenticated', 'true'); // Mark user as authenticated
            localStorage.setItem('userId', newUser.localId); // Mark user as authenticated
            localStorage.setItem('refreshToken', newUser.refreshToken);

            const expiresAt = new Date().getTime() + newUser.expiresIn * 1000;
            localStorage.setItem('expiresAt', expiresAt.toString());
            userStore.update((state) => ({
                ...state,
                isLoading: false,
                userId: newUser.localId
            }));
            return newUser.userId;
        } catch (error) {
            console.error((error as Error).message);
            throw error;
        }
    },
    signup: async (userData: UserSignUpDTO) => {
        try {
            const res = await fetch(`${API_URL}/authentication`, {
                method: 'POST',
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(userData),
            });
            if (!res.ok) throw new Error(`Failed to sign up`);
            const user = await res.json();
            userStore.update((state) => ({
                ...state,
                isLoading: false,
                currentuser: user
            }));

        } catch (error) {
            console.error((error as Error).message);
            throw error;
        }
    },
    getUsers: () => {},
    getUser: async (userId: string) => {
        try {
            const res = await fetch(`${API_URL}/get_user/${userId}`)
            if (!res.ok) throw new Error(`Failed to fetch user ${userId} information`);
            const user = await res.json();
            userStore.update((state) => ({
                ...state,
                isLoading: false,
                currentUser: user,
            }));
        } catch (e) {
            console.error((e as Error).message);
            throw e;
        }
    },
    updateUserRecipes: async (userData: UserDTO) => {
        try {
            const res = await fetch(`${API_URL}/update_user_recipes_allergies/${userData.user_id}`, {
                method: 'PUT',
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(userData),
            });

            if (!res.ok) throw new Error(`Failed to update user ${userData.user_id} recipe info`);
            const updatedUser = await res.json();
            userStore.update((state) =>( {
                ...state,
                isLoading: false,
                currentUser: updatedUser
            }));
        } catch (error) {
            console.error((error as Error).message);
            throw error;
        }
    },
    updateUserDetail: async (userData: UserDTO) => {
        try {
            const res = await fetch(`${API_URL}/update_user`, {
                method: 'PUT',
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(userData),
            });
            if (!res.ok) throw new Error(`Failed to update user ${userData.user_id} recipe info`);
            const updatedUser = await res.json();
            userStore.update((state) =>( {
                ...state,
                isLoading: false,
                currentUser: updatedUser
            }));
        } catch (error) {
            console.error((error as Error).message);
            throw error;
        }
    },
    deleteuser: () => {},

}