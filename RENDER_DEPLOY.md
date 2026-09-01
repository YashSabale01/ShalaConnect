# ShalaConnect — Render Deployment Guide

## What's in this folder

| File | Purpose |
|------|---------|
| `render.yaml` | Render Blueprint — defines all services + DB |
| `backend/Dockerfile` | Uses `${PORT}` env var (required by Render) |
| `frontend/Dockerfile` | Accepts `VITE_API_URL` as build arg |
| `frontend/nginx.conf` | Serves React SPA with proper routing |

---

## Steps to Deploy

### 1. Merge these files into your repo

Copy the files into your existing ShalaConnect repo, replacing:
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `frontend/nginx.conf`
- Add `render.yaml` at the root

### 2. Push to GitHub

```bash
git add .
git commit -m "Add Render deployment config"
git push
```

### 3. Create services on Render

1. Go to https://dashboard.render.com
2. Click **New → Blueprint**
3. Connect your GitHub repo (`YashSabale01/ShalaConnect`)
4. Render will detect `render.yaml` and create:
   - `shalaconnect-db` (MySQL-compatible PostgreSQL)
   - `shalaconnect-backend` (Spring Boot)
   - `shalaconnect-frontend` (React/Nginx)

### 4. Set required environment variables

After services are created, go to each service's **Environment** tab and set:

**Backend:**
| Key | Value |
|-----|-------|
| `ADMIN_EMAIL` | your admin email |
| `ADMIN_PASSWORD` | your admin password |
| `ALLOWED_ORIGINS` | `https://shalaconnect-frontend.onrender.com` |

**Frontend:**
| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://shalaconnect-backend.onrender.com/api` |

> ⚠️ After setting `VITE_API_URL`, trigger a **manual redeploy** of the frontend so the build picks up the new value.

### 5. Database note

Render's free tier provides **PostgreSQL**, not MySQL.  
You have two options:

**Option A (Recommended):** Use Render's free PostgreSQL
- Change `pom.xml` dependency from `mysql-connector-j` to `postgresql`
- Update `DB_URL` format to: `jdbc:postgresql://...`

**Option B:** Use an external free MySQL (e.g. [PlanetScale](https://planetscale.com) or [Aiven](https://aiven.io))
- Create a free MySQL instance there
- Set `DB_URL`, `DB_USERNAME`, `DB_PASSWORD` manually in Render backend env vars

---

## Local test with Docker before deploying

```bash
docker build -t shalaconnect-backend ./backend
docker build --build-arg VITE_API_URL=http://localhost:7070/api -t shalaconnect-frontend ./frontend
```
