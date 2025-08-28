<template>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Leaderboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container my-4">
        <h1 class="text-center mb-4">TCAT Leaderboard</h1>

        <!-- Filters -->
        <div class="row justify-content-center">
            <div class="col mb-3">
                <select class="form-select" aria-label="Filter by Workspace" v-model="filterWorkspace">
                    <option value="1">Seattle Design Festival 2025</option>
                </select>
            </div>
            <div class="col mb-3">
                <select class="form-select" aria-label="Filter by Time Range" v-model="filterTime">
                    <option value="all">All Time</option>
                    <option value="month">Last Month</option>
                    <option value="week">Last Week</option>
                </select>
            </div>
            <div class="col mb-3">
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
                    <tr style="background-color: #FFD700">
                        <td>1</td>
                        <td>Ostentatious Otters</td>
                        <td>2850</td>
                    </tr>
                    <tr style="background-color: #C0C0C0">
                        <td>2</td>
                        <td>Brave Badgers</td>
                        <td>2400</td>
                    </tr>
                    <tr style="background-color: #e1b284;">
                        <td>3</td>
                        <td>Swift Swans</td>
                        <td>2300</td>
                    </tr>
                    <tr v-for="entry in leaderboard" :key="entry.name">
                      <td>{{ entry.name }}</td>
                      <td>{{ entry.score }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
</template>

<script>
export default {
  data() {
    return {
      leaderboard: [],
      filterTime: '',
      filterWorkspace: ''
    };
  },
  methods: {
    fetchLeaderboard() {
      const params = new URLSearchParams({
        filterTime: this.filterTime,
        filterWorkspace: this.filterWorkspace
      });
      fetch(`/api/leaderboard?${params.toString()}`)
        .then(response => response.json())
        .then(data => {
          this.leaderboard = data;
        });
    }
  }
};
</script>

<style>
/**
.container {
  max-width: 100%;
  padding: 15px;
}
.table-responsive {
  overflow-x: auto;
}
@media (max-width: 768px) {
  h1 {
    font-size: 1.5rem;
  }
  .btn {
    width: 100%;
  }
}
*/
</style>
