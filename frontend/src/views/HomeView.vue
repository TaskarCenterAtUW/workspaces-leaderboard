<template>
    <!-- Filters -->
    <div class="row">
        <Suspense>
        <div class="col-12 col-md-7 col-lg-7 mb-3">
            <label for="ws_project_group_picker">Project Group</label>
            <project-group-picker v-model="filterProjectGroup" id="ws_project_group_picker" />
        </div>
        </Suspense>
    </div>
    <div class="row">
        <div class="col-12 col-md-7 col-lg-7 mb-3">
            <label for="ws_dataset_picker">Workspace</label>
            <dataset-picker
                id="ws_dataset_picker"
                v-model="filterWorkspace"
                :project-group-id="filterProjectGroup"
            />
        </div>
        <div class="col-12 col-md-3 col-lg-3 mb-3">
            <label for="filterTime">Time Range</label>
            <select id="filterTime" class="form-select" aria-label="Filter by Time Range" v-model="filterTime">
                <option value="all">All Time</option>
                <option value="month">Last Month</option>
                <option value="week">Last Week</option>
            </select>
        </div>
        <div class="col-12 col-md-2 col-lg-2 mb-3 mt-auto">
            <button class="btn btn-primary me-2" @click="fetchLeaderboard">Filter</button>
        </div>
    </div>

    <!-- Leaderboard Table -->
    <div v-if="!filterWorkspace" class="alert alert-warning" role="alert">
        Please select a Workspace to view the Leaderboard.
    </div>
    <div v-else-if="leaderboard.length === 0" class="alert alert-info" role="alert">
        No results found for the selected filters.
    </div>
    <div v-else class="table-responsive">
        <table class="table table-striped table-bordered">
            <thead style="color: #fff; background-color: #330872;">
                <tr>
                    <th scope="col">Rank</th>
                    <th scope="col">Team</th>
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
import { ref, onMounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router';

const filterProjectGroup = ref('null');
const filterWorkspace = ref('');
const filterTime = ref('all');
const isSearchExpanded = ref(true);
const leaderboard = ref([]);

function fetchLeaderboard() {
    if (!filterWorkspace) {
        leaderboard.value = [];
        return;
    }

    let leaderboardApiUrl = import.meta.env.VITE_LEADERBOARD_API_URL;
    if (!leaderboardApiUrl) {
        leaderboardApiUrl = 'https://api.' + window.location.hostname + '/api/leaderboard';
    }

    const params = new URLSearchParams({
        filterTime: filterTime.value,
        filterWorkspace: filterWorkspace.value
    });
    fetch(leaderboardApiUrl + `?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
        leaderboard.value = data;
    });
}

function toggleSearchCollapse() {
    isSearchExpanded.value = !isSearchExpanded.value;
}

onMounted(() => {
    fetchLeaderboard();
});

</script>