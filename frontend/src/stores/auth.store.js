import { defineStore } from 'pinia';

import { router } from '@/helpers/router';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        // initialize state from local storage to enable user to stay logged in
        user: JSON.parse(localStorage.getItem('user')),
        returnUrl: null
    }),
    actions: {
        async login(username, password) {
            const tdeiApiUrl = import.meta.env.VITE_TDEI_API_URL;
            const requestBody = {
                username: username,
                password: password
            };
            const jsonBody = JSON.stringify(requestBody);

            const response = await fetch(tdeiApiUrl + 'authenticate', {
                method: 'POST', 
                body: jsonBody
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const user = await response.json();
            this.user = user;

            // store user details and jwt in local storage to keep user logged in between page refreshes
            localStorage.setItem('user', JSON.stringify(user));

            // redirect to previous url or default to home page
            router.push(this.returnUrl || '/');
        },
        logout() {
            this.user = null;
            localStorage.removeItem('user');
            router.push('/login');
        }
    }
});