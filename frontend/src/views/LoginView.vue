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

        <div class="mb-3">
          <button type="submit" class="btn btn-primary" :disabled="disabled">
            <app-spinner v-if="loading.active" size="sm" />
            <template v-else>Submit</template>
          </button>
        </div>

        <div v-if="error" class="alert alert-danger" role="alert">
          {{ error }}
        </div>
      </form>
    </div>
  </template>
  
  <script setup lang="ts">
    import { computed, reactive, ref } from 'vue';
    import { useRouter } from 'vue-router';
    import { LoadingContext } from '@/services/loading';
    import { tdeiClient } from '@/services/index';

    const loading = reactive(new LoadingContext());
    const router = useRouter();

    const username = ref('');
    const password = ref('');
    const error = ref('');
    const disabled = computed(() => loading.active || !username.value.length || !password.value.length);
  
    async function handleSubmit() {
      error.value = ''

      try {
        await signIn();
      }
      catch (e: unknown)  {
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
    }

    async function signIn() {
      await loading.wrap(tdeiClient, async (client) => {
        await client.authenticate(username.value, password.value);
      })

      router.push('/');
    }
  </script>