<template>
    <div class="signin-card card">
      <form class="card-body">
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
  
        <button type="submit" class="btn btn-primary">
          Submit
        </button>
        <span class="ms-3 text-danger align-middle">{{ error }}</span>
      </form>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';

  const error = ref('');
  const username = ref('');
  const password = ref('');
  
  async function submit() {
    const authStore = useAuthStore();

    return authStore.login(username, password)
        .catch(error => setErrors({ apiError: error }));

    /**
    error.value = ''
  
    try {
      await signIn(username, password);
    } catch (e: unknown)  {
      if (e.response?.status === 400) {
        const body = await e.response.json();
  
        if (body.errors?.length > 0) {
          error.value = 'Error: ' + body.errors[0];
          return;
        }
      }
  
      if (e.response?.status === 401 || e.response?.status === 404) {
        error.value = 'Incorrect TDEI username/password.';
        return;
      }
  
      error.value = e.toString();
    }
      */
  }
  </script>