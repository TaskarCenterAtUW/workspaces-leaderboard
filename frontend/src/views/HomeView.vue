<template>
    <!-- Filters -->
    <div :class="{'collapse': true, 'show': isSearchExpanded}">
        <div class="row">
            <Suspense>
            <div class="col-5 mb-3">
                <label for="ws_project_group_picker">Project Group</label>
                <project-group-picker v-model="filterProjectGroup" id="ws_project_group_picker" />
            </div>
            </Suspense>
            <div class="col-7 mb-3 d-flex align-items-center">
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" v-model="filterQuestsOnly" id="checkboxQuests" aria-label="Filter by Quests Only" >
                    <label class="form-check-label" for="checkboxQuests">
                        Workspaces with Quests Only
                    </label>
                </div>
            </div>
        </div>
    </div>
    <div class="row justify-content-center">
        <div class="col-6 mb-3">
            <label for="ws_dataset_picker">Workspace</label>
            <dataset-picker
                id="ws_dataset_picker"
                v-model="filterWorkspace"
                :project-group-id="filterProjectGroup"
            />
        </div>
        <div class="col-3 mb-3">
            <select class="form-select" aria-label="Filter by Time Range" v-model="filterTime">
                <option value="all">All Time</option>
                <option value="month">Last Month</option>
                <option value="week">Last Week</option>
            </select>
        </div>
        <div class="col-2 mb-3">
            <button class="btn btn-primary" @click="fetchLeaderboard">Filter</button>
        </div>
        <div class="col-1 mb-3">
            <button class="btn btn-secondary" @click="toggleSearchCollapse" :aria-expanded="isSearchExpanded ? 'true' : 'false'"><img src="/filter-32-32.png" style="height: 24px;" /></button>
        </div>
    </div>

    <!-- Leaderboard Table -->
    <div class="table-responsive">
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

const filterProjectGroup = ref(null);
const filterWorkspace = ref({});
const filterTime = ref('all');
const filterQuestsOnly = ref(false);
const isSearchExpanded = ref(true);
const leaderboard = ref([]);

function fetchLeaderboard() {
    leaderboard.value = [
        { "name": "Gorgeous Gophers", "score": 2850 },
        { "name": "Tricksy Tigers", "score": 2400 },
        { "name": "Swift Swans", "score": 2300 },
        { "name": "Mighty Meerkats", "score": 2200 },
        { "name": "Brilliant Bears", "score": 1800 },
        { "name": "Ostentatious Otters", "score": 1500 },
        { "name": "Bouncy Birbs", "score": 1400 },
        { "name": "Cute Capybaras", "score": 1350 },
        { "name": "Delightful Ducks", "score": 1300 },
        { "name": "Eager Elephants", "score": 1250 }
    ];
}

function toggleSearchCollapse() {
    isSearchExpanded.value = !isSearchExpanded.value;
}

onMounted(() => {
    fetchLeaderboard();
});

/**
const params = new URLSearchParams({
    filterTime: this.filterTime,
    filterWorkspace: this.filterWorkspace
});
fetch(`/api/leaderboard?${params.toString()}`)
    .then(response => response.json())
    .then(data => {
    this.leaderboard = data;
    });
*/

</script>