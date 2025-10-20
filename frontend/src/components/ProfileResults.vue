<template>
    <div v-if="loading.active" class="alert alert-info" role="alert">
        <app-spinner size="sm" />
        Loading profile...
    </div>
    <div v-else-if="stats" id="profile-results">
        <div>
            <p>
                <a href @click.prevent="updateProfileId(null)">
                    <app-icon variant="arrow_back_ios" /><span>Back</span>
                </a>
            </p>
        </div>
        <div class="text-center">
            <p><h2>{{ stats.name }}</h2></p>
        </div>
    </div>
</template>

<script setup>
  import { defineProps, onMounted, reactive, ref } from 'vue';
  import { leaderboardClient } from '@/services/index';
  import { LoadingContext } from '@/services/loading';

  const loading = reactive(new LoadingContext());
  const model = defineModel();

  const props = defineProps({
    filterTeam: {
        type: String,
        required: true,
    },
    filterTime: {
        type: String,
        required: true,
    },
    filterWorkspace: {
        type: String,
        required: true,
    },
  });

  const stats = ref(null);
  const map = ref([]);

  function updateProfileId(newValue) {
    model.value = newValue;
  }

  async function fetchProfile() {
    const params = new URLSearchParams({
        filterTeam: props.filterTeam,
        filterId: model.value,
        filterTime: props.filterTime,
        filterWorkspace: props.filterWorkspace
    });

    await loading.wrap(leaderboardClient, async (client) => {
        stats.value = await client.getProfileStats(params);
        map.value = await client.getProfileMap(params);
    })
  }

  onMounted(() => {
    fetchProfile();
});
</script>