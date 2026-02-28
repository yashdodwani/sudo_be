# Render Deployment - Quick Fix Guide

## Issue: Pydantic Build Failure (Rust/Cargo Error)

**Error Message:**
```
error: failed to create directory `/usr/local/cargo/registry/cache/`
Read-only file system (os error 30)
```

### Solution 1: Use Correct Python Version ✅

**Create `runtime.txt` in project root:**
```
python-3.11.9
```

### Solution 2: Updated Build Command ✅

In Render Dashboard, use this build command:
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

### Solution 3: Simplified Requirements ✅

The `requirements.txt` has been updated to use `pydantic==2.5.3` which has pre-built wheels.

---

## Complete Render Setup (Copy-Paste Ready)

### 1. Build Command
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

### 2. Start Command
```bash
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2
```

### 3. Environment Variables

Copy these exactly:

```
APP_NAME=OpenClaw Backend
APP_ENV=production
LOG_LEVEL=INFO
DATABASE_URL=postgresql+asyncpg://neondb_owner:npg_ixqrSu5LZkA3@ep-jolly-feather-aixu2cx1-pooler.c-4.us-east-1.aws.neon.tech/neondb
```

### 4. Health Check Path
```
/health
```

### 5. Additional Settings

- **Runtime**: Auto (will use runtime.txt)
- **Region**: Oregon
- **Plan**: Free
- **Auto-Deploy**: Yes

---

## Alternative: Deploy with Docker

If Python build still fails, use Docker deployment:

### In Render Dashboard:

1. **Environment**: Docker
2. **Dockerfile Path**: `./Dockerfile`
3. **Docker Command**: (leave empty, uses CMD from Dockerfile)
4. Add same environment variables as above

---

## Troubleshooting Other Issues

### Issue: Module Not Found

**Fix:** Clear build cache in Render:
1. Go to your service
2. Settings → Delete → "Clear build cache"
3. Redeploy

### Issue: Database Connection Failed

**Fix:** Ensure DATABASE_URL uses `postgresql+asyncpg://` (not just `postgresql://`)

### Issue: Port Binding Error

**Fix:** Use `$PORT` in start command (not hardcoded 8000)

### Issue: Migration Failed

**Fix:** Check logs, ensure database is accessible. Manually run:
```bash
# In Render Shell
alembic upgrade head
```

---

## Verification Steps After Deployment

1. **Check Logs** - Should see:
   ```
   INFO:     Starting OpenClaw Backend
   INFO:     Reminder scheduler service started
   INFO:     Uvicorn running on http://0.0.0.0:XXXX
   ```

2. **Test Health Endpoint**:
   ```bash
   curl https://your-app.onrender.com/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "service": "OpenClaw Backend",
     "environment": "production"
   }
   ```

3. **Test API Docs**:
   Visit: `https://your-app.onrender.com/docs`

---

## Files Updated for Render Compatibility

✅ `runtime.txt` - Specifies Python 3.11.9
✅ `requirements.txt` - Uses pydantic 2.5.3 (pre-built wheels)
✅ `render.yaml` - Updated build command
✅ `Dockerfile` - Production-ready
✅ `Procfile` - Correct start command

---

## Quick Deploy Checklist

- [ ] Push code to GitHub
- [ ] Create new Web Service on Render
- [ ] Set Runtime to Python 3 (will auto-detect runtime.txt)
- [ ] Use updated build command with pip upgrade
- [ ] Add environment variables (especially DATABASE_URL with asyncpg)
- [ ] Set health check path: `/health`
- [ ] Deploy and watch logs
- [ ] Test `/health` and `/docs` endpoints

---

## Contact Support

If issues persist:
- Render Status: https://status.render.com
- Render Docs: https://render.com/docs
- Render Community: https://community.render.com

---

**Last Updated:** After fixing pydantic build issue
**Status:** ✅ Ready for deployment

