import { writable } from 'svelte/store';

export const toastStore = writable({
    message: '',
    type: '',
    show: false
});

export const showToast = (type: string, message: string) => {
    toastStore.set({
        message,
        type,
        show: true
    });
    
    setTimeout(() => {
        toastStore.set({
            message: '',
            type: '',
            show: false
        });
    }, 3000);
};
export function hideToast() {
    toastStore.set({
        message: "",
        type: "success",
        show: false
    });
}