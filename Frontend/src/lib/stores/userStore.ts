import { writable } from "svelte/store";
import type { UserDTO, UserLoginDTO, UserSignUpDTO } from "$lib/types";
const API_URL = import.meta.env.VITE_API_URL;

export const userStore = writable({
    isLoading: true,
    userId: "",
    authenticated: false,
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
            localStorage.setItem('idToken', newUser.idToken);
            localStorage.setItem('refreshToken', newUser.refreshToken)


            // Store expiration timestamp
            const expiresAt = new Date().getTime() + newUser.expiresIn * 1000;
            localStorage.setItem('expiresAt', expiresAt.toString());

            userStore.update((state) => ({
                ...state,
                isLoading: false,
                currentUser: newUser,
                authenticated: true,
                userId: newUser.localId
            }));
            return newUser.userId;
        } catch (error) {
            console.error((error as Error).message);
            userStore.update((state) => ({
                ...state,
                isLoading: false,
                currentUser: null,
                authenticated: false,
            }));
            throw error;
        }
    },

    checkSessionExpiration: () => {
        const expiresAt = localStorage.getItem('expiresAt');
        if (expiresAt && Date.now() > parseInt(expiresAt)) {
            userHandler.signOut();
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
            userStore.update((state) => ({
                ...state,
                isLoading: true,
            }))
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
            userStore.update((state) => ({
                ...state,
                isLoading: false,
                currentUser: null,
            }));
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
            if (userData === null) {
                throw new Error("User data is null");
            }
            if (userData.user_id === undefined) {
                throw new Error("User ID is undefined");
            }
            userStore.update((state) => ({
                ...state,
                isLoading: true,
            }));
        
            const idToken = localStorage.getItem('idToken');
            if (!idToken) {
                throw new Error("idToken is undefined");
            }

            console.log("Updating user", userData);
            const res = await fetch(`${API_URL}/users/update_all?id_token=${idToken}`, {
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
        document.cookie = "authToken=; path=/; Secure; HttpOnly; SameSite=Strict; Max-Age=0"; 
        userStore.update((state) => ({
            ...state,
            isLoading: false,
            authenticated: false,
            currentUser: null
        }));
    },
    checkAuthenticated() {
        const isAuthenticated = localStorage.getItem('authenticated') === 'true';
        userStore.update(state => ({ ...state, authenticated: isAuthenticated }));
        return isAuthenticated;
    },

    uploadProfileImage: async (image: File) => {
        const idToken = localStorage.getItem('idToken');
        if (!idToken) {throw new Error("User is not signed in");}
        const savePath = `profileImages/${image.name}`;
        try {
            const formData = new FormData();
            formData.append("file", image);
            const res = await fetch(`${API_URL}/upload-image/file?id_token=${idToken}&savePath=${savePath}`, {
                method: "POST",
                body: formData,
            });
            if (!res.ok) throw new Error("Failed to upload image");
    
            const data = await res.json();
            const imageUrl = data; // Assuming the response contains the image URL
    
            // Update currentUser in the local store without using get()
            let updatedUser: typeof data | undefined;
            userStore.update((store) => {
                if (store.currentUser) {
                    updatedUser = { ...store.currentUser, profileImageURL: imageUrl };
                    return { ...store, currentUser: updatedUser };
                }
                return store;
            });
			let userId = localStorage.getItem('userId');
			updatedUser.user_id = userId
            console.log("updateUser: ", updatedUser)
            // If we have an updated user, update the backend as well
            if (updatedUser) {
                await userHandler.updateUserDetail(updatedUser);
            }
            return imageUrl;
        } catch (error) {
            console.error("Image upload failed", (error as Error).message);
            throw error;
        }
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