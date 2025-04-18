import { writable } from "svelte/store";
import type { UserDTO, UserLoginDTO, UserSignUpDTO } from "$lib/types";
const API_URL = import.meta.env.VITE_API_URL;

export const userStore = writable({
    isLoading: true,
    userId: "",
    authenticated: false,
    currentUser: null as UserDTO | null,
    recipes: [] as string[],
});


export const userHandler = {
    login: async (userData: UserLoginDTO) => {
        try {
            const res = await fetch(`${API_URL}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData),
            });

            const newUser = await res.json();
            if (!res.ok) throw new Error(newUser?.detail || res.statusText);


            // Store token in HttpOnly cookie for security
            document.cookie = `authToken=${newUser.token}; path=/; Secure; HttpOnly; SameSite=Strict; Max-Age=${newUser.expiresIn}`;

            // Store non-sensitive data in localStorage
            localStorage.setItem('authenticated', 'true');
            localStorage.setItem('userId', newUser.localId);
            localStorage.setItem('idToken', newUser.idToken);
            localStorage.setItem('refreshToken', newUser.refreshToken)
            localStorage.setItem('recipes',  JSON.stringify(newUser.recipes));


            // Store expiration timestamp
            const expiresAt = new Date().getTime() + newUser.expiresIn * 1000;
            localStorage.setItem('expiresAt', expiresAt.toString());

            userStore.update((state) => ({
                ...state,
                isLoading: false,
                currentUser: newUser,
                authenticated: true,
                userId: newUser.localId,
                recipes: newUser.recipes,
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
    refreshToken: async () => {
        try {
            const refreshToken = localStorage.getItem('refreshToken');
            if (!refreshToken) {
                throw new Error("Refresh token is undefined");
            }
            const res = await fetch(`${API_URL}/refresh_token?refresh_token=${refreshToken}`, {
                method: 'POST',
                headers: { "Content-Type": "application/json" },
            });

            const newUser = await res.json();
            if (!res.ok) throw new Error(newUser?.detail || res.statusText || "Failed to refresh token");

            document.cookie = `authToken=${newUser.id_token}; path=/; Secure; HttpOnly; SameSite=Strict; Max-Age=${newUser.expiresIn}`;
            localStorage.setItem('authenticated', 'true');
            localStorage.setItem('userId', newUser.user_id);
            localStorage.setItem('idToken', newUser.id_token);
            localStorage.setItem('accessToken', newUser.access_token);
            localStorage.setItem('refreshToken', newUser.refresh_token)
            const expiresAt = new Date().getTime() + parseInt(newUser.expires_in) * 1000;
            localStorage.setItem('expiresAt', expiresAt.toString());

            return newUser;

        } catch (e) {
            console.error("Failed to refresh token", (e as Error).message);
            // localStorage.clear();
            // userStore.update((state) => ({
            //     ...state,
            //     isLoading: false,
            //     authenticated: false,
            //     currentUser: null,
            // }));
            throw e;
        }
    },

    signup: async (userData: UserSignUpDTO) => {
        try {
            const res = await fetch(`${API_URL}/authentication`, {
                method: 'POST',
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(userData),
            });
            const result = await res.json();
            if (!res.ok) throw new Error(result?.detail || res.statusText);

            userHandler.login({ email: userData.email, password: userData.password });

        } catch (error) {
            console.error((error as Error).message);
            throw error;
        }
    },
    getUsers: async () => {
        try {
            const res = await fetch(`${API_URL}/users`);
            const users = await res.json();
            if (!res.ok) throw new Error(users?.detail || res.statusText);

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
            const user = await res.json();
            if (!res.ok) throw new Error(user?.detail || res.statusText);
            userStore.update((state) => ({
                ...state,
                isLoading: false,
                currentUser: user,
                recipes: user.recipes,
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

            const res = await fetch(`${API_URL}/users/update_all?id_token=${idToken}`, {
                method: 'PUT',
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(userData),
            });
            if (!res.ok) throw new Error(res.statusText);
            const updatedUser = await res.json();
            userStore.update((state) => ({
                ...state,
                isLoading: false,
                currentUser: updatedUser
            }));
        } catch (error) {
            console.error((error as Error).message);
            throw error;
        }
    },
    deleteuser: () => { },

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
        var userId = localStorage.getItem('userId')
        if (!idToken) {throw new Error("User is not signed in");}
        const savePath = `profileImages/${userId}`;

        try {
            const formData = new FormData();
            formData.append("file", image);
            const res = await fetch(`${API_URL}/upload-image/file?id_token=${idToken}&save_path=${savePath}`, {
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
    },

    addFavoriteRecipe: async (recipeId: string) => {
        const idToken = localStorage.getItem('idToken');
        if (!idToken) { throw new Error("User is not signed in"); }

        try {
            const url = `${API_URL}/users/add_favorite/${idToken}?recipe_id=${recipeId}`

            const res = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!res.ok) throw new Error(res.statusText || 'Failed to add favorite recipe')

            const userRecipes = await res.json();
            localStorage.setItem('recipes', JSON.stringify(userRecipes));
            userStore.update((state) => ({
                ...state,
                recipes: userRecipes
            }))
            return userRecipes;
        } catch (error) {
            console.error("Error adding favorite recipe", error);
            throw error
        }
    },

    unfavoriteRecipe: async (recipeId: string) => {
        const idToken = localStorage.getItem('idToken');
        if (!idToken) { throw new Error("User is not signed in"); }
        try {
            const url = `${API_URL}/users/favorite/${idToken}?recipe_id=${recipeId}`

            const res = await fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (!res.ok) throw new Error(res.statusText || 'Failed to remove favorite recipe');
            const userRecipes = await res.json();
            localStorage.setItem('recipes', JSON.stringify(userRecipes));
            userStore.update((state) => ({
                ...state,
                recipes: userRecipes
            }))
            return userRecipes;
        } catch (error) {
            console.error("Error removing favorite recipe", error);
            throw error
        }
    },

    

}


export function getLSUserData() {
    const userData: { [key: string]: string | null } = {};
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key) {
            const value = localStorage.getItem(key);
            userData[key] = value
        }
    }
    return userData
}