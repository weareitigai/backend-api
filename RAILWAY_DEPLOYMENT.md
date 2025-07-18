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

3. **Environment Variables** (Railway will set automatically)
   - `DATABASE_URL` - Auto-generated PostgreSQL connection
   - `SECRET_KEY` - Set a secure secret key
   - `DEBUG` - Set to `False` for production

## What Railway Does Automatically
- ✅ Provisions PostgreSQL database
- ✅ Runs migrations (`python manage.py migrate`)
- ✅ Collects static files (`python manage.py collectstatic`)
- ✅ Starts with Gunicorn
- ✅ Provides HTTPS domain

## Your API will be available at:
```
https://your-app-name.railway.app/api/
```

## API Documentation will be at:
```
https://your-app-name.railway.app/api/docs/
```

## Files Modified for Railway:
- `requirements.txt` - Added dj-database-url, whitenoise, gunicorn
- `config/settings.py` - Updated database config and static files
- `railway.json` - Deployment configuration
- `.railwayignore` - Exclude frontend from deployment

Your Django backend is now Railway-ready! 🚀 