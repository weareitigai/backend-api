# Railway Deployment Guide

## Quick Deploy Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Django and deploy

3. **Add PostgreSQL Service**
   - In Railway dashboard, click "➕ Add Service"
   - Select "PostgreSQL"
   - Railway will automatically connect it to your Django app
   - This creates the `DATABASE_URL` environment variable

4. **Run Migrations** (After PostgreSQL is connected)
   - Go to your Railway app dashboard
   - Click on your Django service
   - Go to "Deploy" tab
   - Run this command in the terminal:
   ```bash
   python manage.py migrate
   ```

5. **Environment Variables** (Set these manually)
   - `SECRET_KEY` - Set a secure Django secret key
   - `DEBUG=False` - For production

## What Railway Does Automatically
- ✅ Provisions PostgreSQL database (when you add the service)
- ✅ Creates `DATABASE_URL` environment variable
- ✅ Collects static files (`python manage.py collectstatic`)
- ✅ Starts with Gunicorn
- ✅ Provides HTTPS domain

## What You Need to Do Manually
- 🔧 Add PostgreSQL service
- 🔧 Run migrations (`python manage.py migrate`)
- 🔧 Set SECRET_KEY environment variable

## Your API will be available at:
```
https://your-app-name.railway.app/api/
```

## API Documentation will be at:
```
https://your-app-name.railway.app/api/docs/
```

## Health Check Endpoint:
```
https://your-app-name.railway.app/health/
```
This endpoint works without database connection and is used by Railway for health checks.

## Files Modified for Railway:
- `requirements.txt` - Added dj-database-url, whitenoise, gunicorn
- `config/settings.py` - Updated database config and static files
- `config/urls.py` - Added health check endpoint
- `railway.json` - Deployment configuration with better Gunicorn settings
- `.railwayignore` - Exclude frontend from deployment
- `railway_migrate.py` - Migration script for after database setup
- `check_deployment.py` - Deployment verification script

## Troubleshooting

### ❌ Container starts then stops immediately
**Problem**: Health check failures or configuration issues
**Solution**: 
- We've added a `/health/` endpoint that doesn't require database
- Updated Gunicorn parameters for better stability
- Check Railway logs for specific error messages

### ❌ "Connection refused" error during deployment
**Problem**: Django tries to connect to database before PostgreSQL service is added
**Solution**: 
1. Add PostgreSQL service in Railway dashboard
2. Wait for `DATABASE_URL` to be set
3. Redeploy or run migrations manually

### ❌ "DisallowedHost" error
**Problem**: ALLOWED_HOSTS not configured for Railway domain
**Solution**: This shouldn't happen as we set `ALLOWED_HOSTS = ['*']`

### ❌ Static files not loading
**Problem**: Static files not collected properly
**Solution**: Railway runs `collectstatic` automatically, but you can run it manually:
```bash
python manage.py collectstatic --noinput
```

### ❌ Migrations not applied
**Problem**: Database tables don't exist
**Solution**: Run migrations manually in Railway terminal:
```bash
python manage.py migrate
```

Your Django backend is now Railway-ready! 🚀 