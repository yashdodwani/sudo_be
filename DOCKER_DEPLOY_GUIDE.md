# 🐳 DOCKER DEPLOYMENT ON RENDER - STEP BY STEP

## Why Docker?

**Native Python build on Render fails** because pydantic-core requires Rust compilation, which doesn't work on Render's read-only filesystem.

**Docker solves this** by building everything in a proper environment with full permissions, then deploying the pre-built image.

---

## 🚀 DEPLOY NOW - Complete Guide

### Step 1: Verify Files Are Ready

Your repository already has:
- ✅ `Dockerfile` - Production-ready Docker configuration
- ✅ `.dockerignore` - Optimizes build
- ✅ `requirements.txt` - All dependencies
- ✅ `alembic/` - Database migrations

### Step 2: Push to GitHub

```bash
cd /home/voyager4/projects/openclaw_sudo
git add .
git commit -m "Deploy with Docker to fix pydantic-core build issues"
git push origin main
```

### Step 3: Go to Render

Open: **https://dashboard.render.com/**

### Step 4: Create New Web Service

1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** if GitHub isn't connected
4. Find and select your repository: `openclaw_sudo` or similar
5. Click **"Connect"**

### Step 5: Configure Service Settings

#### Basic Settings

| Field | Value |
|-------|-------|
| **Name** | `openclaw-backend` |
| **Region** | Oregon (or closest to you) |
| **Branch** | `main` |

#### ⚠️ CRITICAL: Select Docker Environment

| Field | Value |
|-------|-------|
| **Environment** | **Docker** ← SELECT THIS! Not "Python"! |
| **Dockerfile Path** | `./Dockerfile` |
| **Docker Build Context Directory** | `.` (root directory) |

#### Instance Settings

| Field | Value |
|-------|-------|
| **Instance Type** | Free |

### Step 6: Environment Variables

Click **"Add Environment Variable"** and add each of these:

**Variable 1:**
```
Key:   APP_NAME
Value: OpenClaw Backend
```

**Variable 2:**
```
Key:   APP_ENV
Value: production
```

**Variable 3:**
```
Key:   LOG_LEVEL
Value: INFO
```

**Variable 4 (MOST IMPORTANT):**
```
Key:   DATABASE_URL
Value: postgresql+asyncpg://neondb_owner:npg_ixqrSu5LZkA3@ep-jolly-feather-aixu2cx1-pooler.c-4.us-east-1.aws.neon.tech/neondb
```

⚠️ Make sure DATABASE_URL starts with `postgresql+asyncpg://`

### Step 7: Advanced Settings

Expand **"Advanced"** section:

| Field | Value |
|-------|-------|
| **Health Check Path** | `/health` |
| **Auto-Deploy** | ✅ Yes (deploys on every git push) |

### Step 8: Create Web Service

Click the big **"Create Web Service"** button at the bottom!

---

## ⏱️ What to Expect

### Build Process (5-8 minutes)

You'll see logs like this:

```
==> Cloning from GitHub...
==> Building Docker image...
    Step 1/12 : FROM python:3.11-slim
    Step 2/12 : WORKDIR /app
    Step 3/12 : ENV PYTHONDONTWRITEBYTECODE=1...
    Step 4/12 : RUN apt-get update && apt-get install -y gcc...
    Step 5/12 : COPY requirements.txt .
    Step 6/12 : RUN pip install --no-cache-dir -r requirements.txt
    Successfully installed fastapi-0.103.2 pydantic-2.3.0 ...
    Step 7/12 : COPY . .
    ...
==> Successfully built Docker image
==> Deploying...
==> Starting service...
    INFO  [alembic] Running upgrade -> 001_initial
    2026-02-28 - INFO - Starting OpenClaw Backend
    2026-02-28 - INFO - Reminder scheduler service started
    INFO:     Uvicorn running on http://0.0.0.0:10000
==> Live! 🎉
```

### Success Indicators

- ✅ "Successfully built Docker image"
- ✅ "Running upgrade -> 001_initial" (migrations ran)
- ✅ "Reminder scheduler service started"
- ✅ "Uvicorn running on http://0.0.0.0:XXXXX"
- ✅ "Your service is live!"

---

## 🧪 Test Your Deployment

### Get Your URL

After deployment, Render gives you a URL like:
```
https://openclaw-backend.onrender.com
```

### Test 1: Health Check

```bash
curl https://openclaw-backend.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "OpenClaw Backend",
  "environment": "production"
}
```

### Test 2: API Documentation

Open in browser:
```
https://openclaw-backend.onrender.com/docs
```

You should see the Swagger UI with all your endpoints.

### Test 3: Create a Task

```bash
curl -X POST https://openclaw-backend.onrender.com/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "First Production Task",
    "description": "Testing Docker deployment",
    "status": "pending",
    "source": "ui"
  }'
```

**Expected:** Returns the created task with an ID.

### Test 4: Get All Tasks

```bash
curl https://openclaw-backend.onrender.com/tasks
```

Should return an array with your task(s).

---

## 🎯 Troubleshooting

### Issue: "Dockerfile not found"

**Solution:**
- Make sure `Dockerfile` is in the repository root
- Check it's committed and pushed to GitHub
- Verify "Dockerfile Path" is set to `./Dockerfile`

### Issue: Build fails with permission errors

**Solution:**
- This is normal for the `appuser` creation step
- Check if build continues after warnings
- If it completely fails, try removing the USER lines from Dockerfile

### Issue: Can't connect to database

**Solution:**
- Verify DATABASE_URL environment variable is set
- Make sure it uses `postgresql+asyncpg://`
- Check Neon database is accessible
- Try pinging the database host

### Issue: Health check fails

**Solution:**
- Check logs for startup errors
- Verify migrations ran successfully
- Make sure app is listening on the PORT variable
- Check health check path is `/health` (no trailing slash)

### Issue: Port binding error

**Solution:**
- Dockerfile already uses `${PORT:-8000}`
- This auto-detects Render's PORT variable
- Should work automatically

---

## 📊 Deployment Info

### Your Production URLs

Once deployed:

- **Base API**: `https://openclaw-backend.onrender.com`
- **API Docs**: `https://openclaw-backend.onrender.com/docs`
- **ReDoc**: `https://openclaw-backend.onrender.com/redoc`
- **Health Check**: `https://openclaw-backend.onrender.com/health`

### Share with Frontend Team

Send them:
- Base URL
- Link to `API_DOCUMENTATION.md`
- Link to `API_QUICK_REFERENCE.md`

### Update CORS (Important!)

After deployment, edit `app/main.py` to restrict CORS:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-domain.com",
        "http://localhost:3000",  # for local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then commit and push - auto-deploys!

---

## 💡 Docker Benefits

- ✅ **Consistent builds** - Same environment everywhere
- ✅ **No compilation issues** - Builds with full permissions
- ✅ **Faster rebuilds** - Docker layer caching
- ✅ **Easy rollbacks** - Previous images saved
- ✅ **Works with any package** - No Render limitations

---

## 🔄 Auto-Deploy

With Auto-Deploy enabled:

1. Make changes to your code
2. Commit and push to GitHub
3. Render automatically detects the push
4. Rebuilds Docker image
5. Deploys new version
6. Zero-downtime deployment!

---

## 💰 Cost

**Current Setup: $0/month**

- Render Web Service (Docker): Free tier
- Neon PostgreSQL: Free tier

**Free Tier Limitations:**
- Sleeps after 15 min of inactivity
- 512 MB RAM
- Shared CPU

**To Upgrade:**
- Starter ($7/mo): No sleep, same resources
- Standard ($25/mo): 2 GB RAM, better performance

---

## 📋 Deployment Checklist

- [ ] Code pushed to GitHub with Dockerfile
- [ ] Logged into Render Dashboard
- [ ] Created New Web Service
- [ ] Connected GitHub repository
- [ ] Selected **Docker** environment (not Python!)
- [ ] Set Dockerfile path: `./Dockerfile`
- [ ] Added all 4 environment variables
- [ ] Set health check path: `/health`
- [ ] Enabled Auto-Deploy
- [ ] Clicked "Create Web Service"
- [ ] Watched build logs
- [ ] Tested `/health` endpoint
- [ ] Tested `/docs` endpoint
- [ ] Created test task via API
- [ ] Shared URL with team
- [ ] Updated CORS in production

---

## 🎉 You're Done!

Docker deployment bypasses ALL pydantic-core compilation issues.

**Your API is now live and production-ready!**

🚀 **Next:** Share the API docs with your frontend team and start building!

---

## 📚 Additional Resources

- **API Documentation**: `API_DOCUMENTATION.md`
- **Quick Reference**: `API_QUICK_REFERENCE.md`
- **Troubleshooting**: `RENDER_TROUBLESHOOTING.md`
- **Render Docs**: https://render.com/docs/docker
- **Docker Best Practices**: https://docs.docker.com/develop/dev-best-practices/

---

**Questions?** Everything you need is in the docs above. Happy deploying! 🎊

