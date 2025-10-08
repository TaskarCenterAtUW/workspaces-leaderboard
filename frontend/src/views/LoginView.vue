<template>
    <div class="signin-card card">
      <form class="card-body" @submit.prevent="handleSubmit">
        <div class="mb-3">
          <label for="username" class="form-label">TDEI Username</label>
          <input v-model="username" class="form-control" id="username" aria-describedby="usernameHelp">
          <div id="usernameHelp" class="form-text">
            Enter the same username that you provide to use the TDEI API.
          </div>
        </div>
  
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" id="password">
        </div>
  
        <div v-if="error" class="alert alert-danger" role="alert">
          {{ error }}
        </div>

        <button type="submit" class="btn btn-primary">
          Submit
        </button>
      </form>
    </div>
  </template>
  
  <script setup lang="ts">
    import { ref } from 'vue';
    import { useAuthStore } from '@/stores/auth.store';

    const authStore = useAuthStore();
    const username = ref('');
    const password = ref('');
    const error = ref('');
  
    async function handleSubmit() {
      try {
        await authStore.login(username.value, password.value);
      }
      catch (e) {
        console.log(e);
        error.value = 'Login failed. Please check your username and password.';
      }
    }
  </script>