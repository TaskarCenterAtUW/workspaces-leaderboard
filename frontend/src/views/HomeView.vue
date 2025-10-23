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

    <div v-if="profileId">
        <ProfileResults v-model="profileId" :filter-team="filterTeam" :filter-time="filterTime" :filter-workspace="filterWorkspace" />
    </div>
    <div v-else>
       <LeaderboardResults v-model="profileId" :filter-team="filterTeam" :filter-time="filterTime" :filter-workspace="filterWorkspace" />
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import LeaderboardResults from '@/components/LeaderboardResults.vue';
import ProfileResults from '@/components/ProfileResults.vue';

const filterProjectGroup = ref('null');
const filterWorkspace = ref('');
const filterTeam = ref('individual');
const filterTime = ref('all');

const profileId = ref(null);

// whenever the workspace filter changes, we need to return to the leaderboard view to prevent irrelevant profile data
watch(filterWorkspace, (newValue, oldValue) => {
  profileId.value = null;
});

</script>