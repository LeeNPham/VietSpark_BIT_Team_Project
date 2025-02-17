import { writable } from "svelte/store";
import type { UserDTO, UserLoginDTO, UserSignUpDTO } from "$lib/types";
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

            // Store token in HttpOnly cookie for security
            document.cookie = `authToken=${newUser.token}; path=/; Secure; HttpOnly; SameSite=Strict; Max-Age=${newUser.expiresIn}`; 

            // Store non-sensitive data in localStorage
            localStorage.setItem('authenticated', 'true');
            localStorage.setItem('userId', newUser.localId);
            localStorage.setItem('userEmail', newUser.userEmail);
            localStorage.setItem('userName', newUser.userName);
            localStorage.setItem('phoneNumber', newUser.phoneNumber);
            localStorage.setItem('allergies', newUser.allergies);
            localStorage.setItem('recipes', newUser.recipes);
            localStorage.setItem('profileImageURL', newUser.profileImageURL);
            localStorage.setItem('idToken', newUser.idToken);
            localStorage.setItem('refreshToken', newUser.refreshToken)


            // Store expiration timestamp
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

    checkSessionExpiration: () => {
        const expiresAt = localStorage.getItem('expiresAt');
        if (expiresAt && new Date().getTime() > parseInt(expiresAt)) {
            // clear local storage
            localStorage.clear();
            
            // clear cookie
            document.cookie = "authToken=; path=/; Secure; HttpOnly; SameSite=Strict; Max-Age=0"; 
        }
    }, 

    // TODO: add refresh token api on backend and then add function on frontend
    // refreshToken: async(refreshToken: string) => {
    //     try {

    //     } catch (e) {
    //         console.error("Failed to refresh token", (e as Error).message);
    //         localStorage.clear();

    //     }
    // }, 

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
    getUsers: async () => {
        try {
            const res = await fetch(`${API_URL}/users`);
            if (!res.ok) throw new Error("Failed to fetch users");

            const users = await res.json();
        } catch (e) {
            console.error((e as Error).message);
            throw e;
        }
    },
    getUser: async (userId: string) => {
        try {
            const res = await fetch(`${API_URL}/users/${userId}`)
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
            const res = await fetch(`${API_URL}/users/recipes_allergies/${userData.user_id}`, {
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
            const res = await fetch(`${API_URL}/users`, {
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

    signOut: () => {
        localStorage.clear();
        userStore.update((state) => ({
            ...state,
            isLoading: false,
            currentUser: null
        }));
    }
}


export function getLSUserData() {
    const userData: { [key: string]: string | null } = {};
    for(let i = 0; i < localStorage.length; i++){
        const key = localStorage.key(i);
        if (key){
            const value = localStorage.getItem(key);
            userData[key] = value
        }
    }
    return userData
}