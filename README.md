## Archiva API - Dockerized

Run the FastAPI service with MongoDB using Docker.

### Prerequisites
- Docker and Docker Compose installed on your Ubuntu VM.

### Environment
- The API reads `MONGO_URI` (defaults to `mongodb://mongo:27017/?directConnection=true`).
- Asset files and `assets.json` are read/written under `DATA_DIR` (defaults `/data` in container). Compose mounts `./data` → `/data`.

### Quick start
```bash
docker compose up -d --build
```

API: http://localhost:8000

### Assets handling
- Put your `NA Asset Register 2023.xlsx` (or any `.xlsx`) inside `./data` next to `docker-compose.yml`.
- Endpoints `/assets` and `/update_assets` will read/write `./data/assets.json`.

### Stop / clean
```bash
docker compose down
# Remove Mongo volume (data loss!)
docker volume rm archiva-api_mongo_data
```


