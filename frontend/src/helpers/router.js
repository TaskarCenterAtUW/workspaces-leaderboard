import { reactive } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import { TdeiAuthStore } from '@/services/tdei';
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/LoginView.vue';

export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    linkActiveClass: 'active',
    routes: [
        { path: '/', component: HomeView },
        { path: '/login', component: LoginView }
    ]
});

router.beforeEach(async (to) => {
    // redirect to login page if not logged in and trying to access a restricted page
    const publicPages = ['/login'];
    const authRequired = !publicPages.includes(to.path);

    if (authRequired && !tdeiAuth.username) {
        tdeiAuth.returnUrl = to.fullPath;
        return '/login';
    }
});