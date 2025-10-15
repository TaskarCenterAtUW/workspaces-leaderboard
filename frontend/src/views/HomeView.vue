<template>
    <!-- Filters -->
    <Suspense>
    <div>
        <div class="row">
            <div class="col-12 col-md-8 col-lg-8 mb-3">
                <label for="ws_project_group_picker">Project Group</label>
                <project-group-picker v-model="filterProjectGroup" id="ws_project_group_picker" />
            </div>
            <div class="col-12 col-md-4 col-lg-4 mb-3">
                <label for="filterTeam">Show Rankings</label>
                <select id="filterTeam" class="form-select" aria-label="Show Team or Individual Rankings" v-model="filterTeam" @change="fetchLeaderboard">
                    <option disabled value="team">By Team</option>
                    <option value="individual">By Individual</option>
                </select>
            </div>
        </div>
        <div class="row">
            <div class="col-12 col-md-8 col-lg-8 mb-3">
                <label for="ws_workspace_picker">Workspace</label>
                <workspace-picker
                    id="ws_workspace_picker"
                    v-model="filterWorkspace"
                    :project-group-id="filterProjectGroup"
                    @filterChangeEvent="fetchLeaderboard"
                />
            </div>
            <div class="col-12 col-md-4 col-lg-4 mb-3">
                <label for="filterTime">Time Range</label>
                <select id="filterTime" class="form-select" aria-label="Filter by Time Range" v-model="filterTime" @change="fetchLeaderboard">
                    <option value="all">All Time</option>
                    <option value="month">Last Month</option>
                    <option value="week">Last Week</option>
                    <option value="day">Last Day</option>
                </select>
            </div>
        </div>
    </div>
    </Suspense>

    <!-- Leaderboard Table -->
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
    <div v-else class="table-responsive">
        <table class="table table-striped table-bordered">
            <thead style="color: #fff; background-color: #330872;">
                <tr>
                    <th scope="col">Rank</th>
                    <th v-if="filterTeam == 'team'" scope="col">Team</th>
                    <th v-else scope="col">Username</th>                   
                    <th scope="col">Score</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(result, index) in leaderboard" :key="result.name" :id="`result-${++index}`">
                    <td>{{ index }}</td>
                    <td>{{ result.name }}</td>
                    <td>{{ result.score }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import { LoadingContext } from '@/services/loading';
import { leaderboardClient } from '@/services/index';

const filterProjectGroup = ref('null');
const filterWorkspace = ref('');
const filterTeam = ref('individual');
const filterTime = ref('all');
const leaderboard = ref([]);
const loading = reactive(new LoadingContext());

async function fetchLeaderboard() {
    if (!filterWorkspace) {
        leaderboard.value = [];
        return;
    }

    const params = new URLSearchParams({
        filterTime: filterTime.value,
        filterWorkspace: filterWorkspace.value
    });

    await loading.wrap(leaderboardClient, async (client) => {
        leaderboard.value = await client.getLeaderboard(params);
    })
}

onMounted(() => {
    //fetchLeaderboard();
});
</script>