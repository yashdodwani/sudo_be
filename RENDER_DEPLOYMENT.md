# OpenClaw Backend - Render Deployment Guide

This guide covers deploying the OpenClaw Backend to Render.com.

---

## Prerequisites

1. GitHub account with this repository
2. Render account (free tier available)
3. Neon PostgreSQL database (or Render PostgreSQL)

---

## Deployment Options

### Option 1: Deploy via Render Dashboard (Recommended)

#### Step 1: Create PostgreSQL Database (Optional - Skip if using Neon)

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **PostgreSQL**
3. Configure:
   - **Name:** `openclaw-db`
   - **Database:** `openclaw_db`
   - **User:** `openclaw_user`
   - **Region:** Oregon (or nearest)
   - **Plan:** Free
4. Click **Create Database**
5. **Copy the Internal Database URL** (starts with `postgresql://`)

#### Step 2: Create Web Service

1. Click **New** → **Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Name:** `openclaw-backend`
   - **Region:** Oregon (or same as database)
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2`
   - **Plan:** Free

4. **Environment Variables** - Add these:
   ```
   APP_NAME=OpenClaw Backend
   APP_ENV=production
   DATABASE_URL=<your-database-url-with-asyncpg>
   LOG_LEVEL=INFO
   PYTHON_VERSION=3.11.0
   ```

   **Important:** Modify the `DATABASE_URL`:
   - If using Render PostgreSQL: Change `postgresql://` to `postgresql+asyncpg://`
   - If using Neon: Use your existing connection string with `postgresql+asyncpg://`

5. **Advanced Settings:**
   - **Health Check Path:** `/health`
   - **Auto-Deploy:** Yes

6. Click **Create Web Service**

---

### Option 2: Deploy via Blueprint (render.yaml)

1. Push `render.yaml` to your repository
2. In Render Dashboard: **New** → **Blueprint**
3. Connect your repository
4. Render will auto-detect `render.yaml`
5. Update environment variables as needed
6. Click **Apply**

---

### Option 3: Deploy with Docker

1. In Render Dashboard: **New** → **Web Service**
2. Configure:
   - **Runtime:** Docker
   - **Dockerfile Path:** `./Dockerfile`
3. Set environment variables (same as Option 1)
4. Deploy

---

## Environment Variables

### Required Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `DATABASE_URL` | `postgresql+asyncpg://user:pass@host/db` | Must use `asyncpg` driver |
| `APP_ENV` | `production` | Sets production mode |

### Optional Variables

| Variable | Default | Notes |
|----------|---------|-------|
| `APP_NAME` | OpenClaw Backend | Application name |
| `LOG_LEVEL` | INFO | Logging level |
| `HOST` | 0.0.0.0 | Auto-configured by Render |
| `PORT` | Auto | Render provides this |

---

## Database Configuration

### Using Neon PostgreSQL (Current Setup)

Your current `.env` has:
```
DATABASE_URL=postgresql+asyncpg://neondb_owner:npg_ixqrSu5LZkA3@ep-jolly-feather-aixu2cx1-pooler.c-4.us-east-1.aws.neon.tech/neondb
```

**For Render, add this in Environment Variables:**
```
DATABASE_URL=postgresql+asyncpg://neondb_owner:npg_ixqrSu5LZkA3@ep-jolly-feather-aixu2cx1-pooler.c-4.us-east-1.aws.neon.tech/neondb
```

### Using Render PostgreSQL

If you created a Render database, the URL will be like:
```
postgresql://openclaw_user:password@dpg-xxxxx.oregon-postgres.render.com/openclaw_db
```

**Change to:**
```
postgresql+asyncpg://openclaw_user:password@dpg-xxxxx.oregon-postgres.render.com/openclaw_db
```

---

## Deployment Process

1. **Build Phase:**
   - Render installs dependencies from `requirements.txt`
   - Takes ~2-3 minutes

2. **Migration Phase:**
   - `alembic upgrade head` runs automatically
   - Creates/updates database tables

3. **Start Phase:**
   - Uvicorn starts with 2 workers
   - Health check runs every 30 seconds

---

## Post-Deployment

### 1. Verify Deployment

Visit your Render URL (e.g., `https://openclaw-backend.onrender.com`)

You should see:
```json
{
  "message": "Welcome to OpenClaw Backend",
  "docs": "/docs",
  "health": "/health"
}
```

### 2. Check Health Endpoint

Visit: `https://your-app.onrender.com/health`

Expected response:
```json
{
  "status": "healthy",
  "service": "OpenClaw Backend",
  "environment": "production"
}
```

### 3. Test API

Visit: `https://your-app.onrender.com/docs`

Interactive Swagger UI will load.

### 4. Check Logs

In Render Dashboard → Your Service → Logs

Look for:
```
INFO:     Starting OpenClaw Backend
INFO:     Reminder scheduler service started
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Troubleshooting

### Issue: Database Connection Failed

**Error:** `password authentication failed` or `connection refused`

**Solution:**
1. Verify `DATABASE_URL` uses `postgresql+asyncpg://`
2. Check database credentials are correct
3. Ensure database is accessible from Render region
4. For Neon, verify pooler endpoint is correct

### Issue: Migration Failed

**Error:** `alembic upgrade head` fails

**Solution:**
1. Check database connection
2. Verify `alembic/` directory is in repository
3. Run migrations manually via Render Shell:
   ```bash
   alembic upgrade head
   ```

### Issue: Import Errors

**Error:** `ModuleNotFoundError`

**Solution:**
1. Ensure `requirements.txt` includes all dependencies
2. Check Python version is 3.11+
3. Rebuild the service

### Issue: Port Binding Error

**Error:** `error while attempting to bind on address`

**Solution:**
- Use `$PORT` environment variable (auto-provided by Render)
- Start command should use: `--port $PORT`

### Issue: Health Check Failing

**Solution:**
1. Verify `/health` endpoint is accessible
2. Check application is running
3. Review logs for startup errors

---

## Performance Optimization

### 1. Use Connection Pooling

Already configured in `app/core/database.py`

### 2. Adjust Workers

For Free tier: 2 workers (current)
For Paid tier: 4-8 workers

Update start command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4
```

### 3. Enable Compression

Add to `app/main.py`:
```python
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### 4. Monitor Performance

Use Render's built-in metrics:
- Response time
- Memory usage
- CPU usage

---

## Scaling

### Free Tier Limitations
- Sleeps after 15 minutes of inactivity
- 512 MB RAM
- Shared CPU

### Upgrading
- **Starter ($7/month):** No sleep, 512 MB RAM
- **Standard ($25/month):** 2 GB RAM, dedicated CPU
- **Pro ($85/month):** 4 GB RAM, autoscaling

---

## Security Checklist

- [x] Use environment variables for secrets
- [x] Enable SSL/TLS (automatic on Render)
- [ ] Add rate limiting (TODO)
- [ ] Add authentication (TODO)
- [ ] Configure CORS for specific origins
- [ ] Enable request logging
- [ ] Set up monitoring/alerts

---

## Production Configuration Changes

### Update CORS Origins

In `app/main.py`, change:
```python
allow_origins=["*"]  # Development
```

To:
```python
allow_origins=[
    "https://your-frontend-domain.com",
    "https://openclaw-ui.onrender.com",
]
```

### Update Log Level

Set `LOG_LEVEL=WARNING` or `ERROR` in production

### Enable Production Database Settings

Update `app/core/database.py` for production:
```python
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Disable SQL logging in production
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args={"ssl": "require"}
)
```

---

## Continuous Deployment

### Auto-Deploy on Git Push

Render automatically deploys when you push to `main` branch.

To disable:
1. Go to Service Settings
2. Uncheck "Auto-Deploy"

### Manual Deployment

In Render Dashboard:
1. Select your service
2. Click **Manual Deploy** → **Deploy latest commit**

---

## Monitoring

### Render Built-in Monitoring

- **Metrics:** CPU, Memory, Request count
- **Logs:** Real-time log streaming
- **Events:** Deployment history

### External Monitoring (Optional)

Integrate with:
- Sentry (error tracking)
- Datadog (performance monitoring)
- LogDNA (log management)

---

## Backup Strategy

### Database Backups

**Render PostgreSQL:**
- Free tier: No automatic backups
- Paid tier: Daily backups

**Neon:**
- Automatic point-in-time recovery
- Branch-based backups

### Manual Backup

```bash
# Using Render Shell or local terminal
pg_dump $DATABASE_URL > backup.sql
```

---

## Cost Estimation

### Free Tier (Current)
- Web Service: $0/month
- PostgreSQL (Render): $0/month
- Neon PostgreSQL: $0/month (free tier)

**Total: $0/month**

### Production Tier
- Web Service (Starter): $7/month
- PostgreSQL (Render): $7/month

**Total: $14/month**

---

## Support

- **Render Docs:** https://render.com/docs
- **Render Status:** https://status.render.com
- **Community:** https://community.render.com

---

## Quick Deploy Checklist

- [ ] Push code to GitHub
- [ ] Create/verify database
- [ ] Copy database connection string
- [ ] Create web service on Render
- [ ] Set environment variables
- [ ] Configure health check path: `/health`
- [ ] Set start command with migrations
- [ ] Deploy
- [ ] Verify `/health` endpoint
- [ ] Test `/docs` endpoint
- [ ] Update frontend with production URL

---

## Your Deployment Command

Based on your current setup with Neon:

**Start Command:**
```bash
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2
```

**Environment Variables:**
```
APP_NAME=OpenClaw Backend
APP_ENV=production
DATABASE_URL=postgresql+asyncpg://neondb_owner:npg_ixqrSu5LZkA3@ep-jolly-feather-aixu2cx1-pooler.c-4.us-east-1.aws.neon.tech/neondb
LOG_LEVEL=INFO
```

---

## Next Steps After Deployment

1. Update `API_DOCUMENTATION.md` with production URL
2. Share production URL with frontend team
3. Set up monitoring/alerts
4. Configure CORS for your frontend domain
5. Add authentication (v2.0.0)
6. Set up CI/CD pipeline (optional)

---

**Good luck with your deployment! 🚀**

