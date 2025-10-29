<template>
    <div v-if="loading.active" class="alert alert-info" role="alert">
        <app-spinner size="sm" />
        Loading leaderboard...
    </div>
    <div v-else-if="!filterWorkspace" class="alert alert-warning" role="alert">
        Please select a Workspace to view the Leaderboard.
    </div>
    <div v-else-if="leaderboard.length === 0" class="alert alert-primary" role="alert">
        No results found for the selected filters.
    </div>
    <div v-else id="leaderboard-results" class="table-responsive">
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th scope="col">Rank</th>
                    <th v-if="filterTeam == 'team'" scope="col">Team</th>
                    <th v-else scope="col">Username</th>                   
                    <th scope="col">
                        <div class="d-flex align-items-center justify-content-between">
                            <div>
                                <span>Score</span>
                            </div>
                            <div>
                                <app-icon variant="info" tooltip="Score is calculated by total nodes changed." />
                            </div>
                        </div>
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(result, index) in leaderboard" :key="result.name" :id="`result-${++index}`">
                    <td>{{ index }}</td>
                    <td><a href @click.prevent="updateProfileId(result.id)">{{ result.name }}</a></td>
                    <td>{{ result.score }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
  import { defineProps, onMounted, reactive, ref, watch } from 'vue';
  import { LoadingContext } from '@/services/loading';
  import { leaderboardClient } from '@/services/index';

  const loading = reactive(new LoadingContext());

  const leaderboard = ref([]);
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
        fetchLeaderboard();
      },
      {
        deep: true
      }
  );

  function updateProfileId(newValue) {
    model.value = newValue;
  }

  async function fetchLeaderboard() {
    if (!props.filterWorkspace) {
        leaderboard.value = [];
        return;
    }

    const params = new URLSearchParams({
        filterTeam: props.filterTeam,
        filterTime: props.filterTime,
        filterWorkspace: props.filterWorkspace
    });

    await loading.wrap(leaderboardClient, async (client) => {
        updateProfileId(null);
        leaderboard.value = await client.getLeaderboard(params);
    });

    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    });
 }

  onMounted(() => {
    fetchLeaderboard();
  });
</script>