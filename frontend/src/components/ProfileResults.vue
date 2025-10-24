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
        <div class="text-center mb-4">
            <h1 class="mb-0" style="line-height: 1;">{{ stats.name }}</h1>
            <p v-if="stats.created" class="small mb-0">joined {{ timeAgo(stats.created) }} ago</p>
        </div>
        <div id="profile-content">
            <ul class="nav nav-tabs" id="content-tabs" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="content-map-tab" data-bs-toggle="tab" data-bs-target="#content-map" type="button" role="tab" aria-controls="content-map" aria-selected="true">{{ timeChanges(filterTime) }}</button>
                </li>
            </ul>
            <div class="tab-content" id="content-div">
                <div class="tab-pane fade show active" id="content-map" role="tabpanel" aria-labelledby="content-map-tab">
                    <app-map :workspace="workspace" :mapMarkers="mapMarkers" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
  import { defineProps, onMounted, reactive, ref, watch } from 'vue';
  import { leaderboardClient, workspacesClient } from '@/services/index';
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

  watch(
      () => props,
      (newValue, oldValue) => {
        fetchProfile();
      },
      {
        deep: true
      }
  );

  const stats = ref(null);
  const workspace = ref(null);
  const mapMarkers = ref([]);

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
        mapMarkers.value = await client.getProfileMapMarkers(params);
    })

    await loading.wrap(workspacesClient, async (client) => {
        workspace.value = await client.getWorkspace(props.filterWorkspace);
    })
  }

  onMounted(() => {
    fetchProfile();
  });

  function timeAgo(datetime) {
    const dateObj = new Date(datetime);
    const now = Date.now();
    const seconds = Math.floor((now - dateObj.getTime()) / 1000);

    if (seconds < 60) {
        return "just now";
    } else if (seconds < 3600) {
        const minutes = Math.floor(seconds / 60);
        return `${minutes} minute${minutes > 1 ? 's' : ''}`;
    } else if (seconds < 86400) {
        const hours = Math.floor(seconds / 3600);
        return `${hours} hour${hours > 1 ? 's' : ''}`;
    } else if (seconds < 2592000) { // Approx 30 days
        const days = Math.floor(seconds / 86400);
        return `${days} day${days > 1 ? 's' : ''}`;
    } else if (seconds < 31536000) { // Approx 365 days
        const months = Math.floor(seconds / 2592000);
        return `${months} month${months > 1 ? 's' : ''}`;
    } else {
        const years = Math.floor(seconds / 31536000);
        return `${years} year${years > 1 ? 's' : ''}`;
    }
  }

  function timeChanges(value) {
    switch (value) {
        case 'all':
            return 'all changes';
        default:
            return 'changes within the last ' + value;
    }
  }
</script>