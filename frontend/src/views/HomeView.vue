<template>
    <!-- Filters -->
    <div :class="{'collapse': true, 'show': isSearchExpanded}">
        <div class="row">
            <div class="col-5 mb-3">
                <select class="form-select" aria-label="Filter by Project Group" v-model="filterProjectGroup">
                    <option value="" disabled="disabled">Select a Project Group</option>
                    <option value="125">TDEI Default</option>
                    <option value="126">University of Washington</option>
                </select>
            </div>
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
            <select class="form-select" aria-label="Filter by Workspace" v-model="filterWorkspace">
                <option value="" disabled="disabled">Select a Workspace</option>
                <option value="125">Seattle Design Festival 2025</option>
            </select>
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

<script>
import { RouterLink, RouterView } from 'vue-router';

export default {
    data() {
        return {
            leaderboard: [],
            filterTime: 'all',
            filterProjectGroup: '125',
            filterQuestsOnly: false,
            filterWorkspace: '125',
            isSearchExpanded: false
        };
    },
    methods: {
        fetchLeaderboard() {
            this.leaderboard = [
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
        },
        toggleSearchCollapse() {
            this.isSearchExpanded = !this.isSearchExpanded;
        }
    },
    mounted() {
        this.fetchLeaderboard();
    }
};
</script>