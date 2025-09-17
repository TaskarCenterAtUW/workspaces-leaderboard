<template>
    <div id="app" class="container my-4">
        <h1 class="text-center mb-2">
            <img src="/cropped-tcat-logo_sm.png" alt="Logo" />
            LEADERBOARD
        </h1>
        <h5 class="text-center mb-5">The Taskar Center for Accessible Technology</h5>

        <!-- Filters -->
        <div class="row justify-content-center">
            <div class="col-7 mb-3">
                <select class="form-select" aria-label="Filter by Workspace" v-model="filterWorkspace">
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
    </div>
</template>

<script>
export default {
    data() {
        return {
            leaderboard: [],
            filterTime: 'all',
            filterWorkspace: '125'
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
        }
    },
    mounted() {
        this.fetchLeaderboard();
    }
};
</script>