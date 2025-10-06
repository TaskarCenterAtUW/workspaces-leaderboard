<script setup>
import { RouterLink, RouterView } from 'vue-router';

import { useAuthStore } from '@/stores/auth.store';

const authStore = useAuthStore();
</script>

<template>
    <div id="app" class="container my-4">
        <h1 class="text-center mb-2">
            <img src="/cropped-tcat-logo_sm.png" alt="Logo" />
            LEADERBOARD
        </h1>
        <h5 class="text-center mb-5">The Taskar Center for Accessible Technology</h5>
        <nav v-show="authStore.user" class="navbar navbar-expand navbar-dark bg-dark">
            <div class="navbar-nav">
                <RouterLink to="/" class="nav-item nav-link">Home</RouterLink>
                <a @click="authStore.logout()" class="nav-item nav-link">Logout</a>
            </div>
        </nav>
        <div class="container pt-4 pb-4">
            <RouterView />
        </div>
    </div>
</template>

<style>
</style>