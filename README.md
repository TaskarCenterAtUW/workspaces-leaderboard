# TDEI Workspaces Leaderboard

### ⚠️ Reminder: you must set the tag of the environment you wish to deploy in this repo, then run the deploy workflow in workspaces-stack to deploy to dev, stage or prod.

## Local Setup

# Frontend
```
docker-compose build
docker-compose run --rm -P frontend-dev
cd /app
npm run dev -- --host
```

# Backend
```
docker-compose build
docker-compose up
```