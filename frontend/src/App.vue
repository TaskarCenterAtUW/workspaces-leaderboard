<template>
    <div id="app" class="container my-4">
        <h1 class="text-center mb-2">
            <img src="/cropped-tcat-logo_sm.png" alt="Logo" />
            LEADERBOARD
        </h1>
        <h5 class="text-center mb-2">The Taskar Center for Accessible Technology</h5>
        <div v-if="auth.username" class="container-fluid text-center">
            <span>Welcome, {{ auth.username }}!&nbsp;&nbsp;</span>
            <a @click="signOut()" class="pl-3"> 
                <app-icon variant="logout" /><span>Logout</span>
            </a>
        </div>
        <div class="container pt-4 pb-4 mt-4">
            <RouterView />
        </div>
    </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { tdeiClient } from '@/services/index';

const auth = tdeiClient.auth;

function signOut() {
    auth.clear();
    location.reload();
}
</script>