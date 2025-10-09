<template>
    <div id="app" class="container my-4">
        <h1 class="text-center mb-2">
            <img src="/cropped-tcat-logo_sm.png" alt="Logo" />
            LEADERBOARD
        </h1>
        <h5 class="text-center mb-5">The Taskar Center for Accessible Technology</h5>
        <nav v-if="auth.username" class="navbar navbar-expand">
            <div class="navbar-nav">
                <span class="nav-item nav-link">Welcome, {{ auth.username }}!</span>
                <a @click="auth.clear()" class="nav-item nav-link"> 
                    <app-icon variant="logout" class="me-3" /> Logout
                </a>
            </div>
        </nav>
        <div class="container pt-4 pb-4">
            <RouterView />
        </div>
    </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { tdeiClient } from '@/services/index';

const auth = tdeiClient.auth
</script>