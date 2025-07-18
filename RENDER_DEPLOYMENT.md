# Render Deployment Guide

Deploy your Django Travel Partner API to **Render** with PostgreSQL database.

## 🚀 Quick Deploy (Infrastructure as Code)

### **Method 1: Automatic Deployment with render.yaml**

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click **"New"** → **"Blueprint"**
   - Connect your GitHub repository
   - Render will automatically:
     - Create PostgreSQL database
     - Deploy Django web service
     - Set environment variables
     - Run migrations

---

## 🔧 Manual Deployment (Step by Step)

### **Step 1: Create PostgreSQL Database**

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `travel-partner-db`
   - **Database**: `travel_partner_db`
   - **User**: `travel_partner_user`
   - **Plan**: Free
4. Click **"Create Database"**
5. Copy the **Internal Database URL** (starts with `postgres://`)

### **Step 2: Create Django Web Service**

1. Click **"New"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `django-travel-api`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`
   - **Plan**: Free

### **Step 3: Set Environment Variables**

In the web service **Environment** section, add:

```bash
SECRET_KEY=your-super-secret-django-key-here
DEBUG=false
DATABASE_URL=<paste-your-database-url-here>
```

### **Step 4: Deploy**

Click **"Create Web Service"** and wait for deployment to complete.

---

## 🌐 Your API URLs

Once deployed, your API will be available at:

### **Base URL**
```
https://your-service-name.onrender.com
```

### **Health Check**
```
https://your-service-name.onrender.com/health/
```

### **API Documentation**
```
https://your-service-name.onrender.com/api/docs/
```

### **Django Admin**
```
https://your-service-name.onrender.com/admin/
```

---

## 🔐 Post-Deployment Setup

### **Create Superuser**

1. Go to your web service dashboard
2. Click **"Shell"** tab
3. Run:
   ```bash
   python manage.py createsuperuser
   ```

### **Test APIs**

```bash
# Health check
curl https://your-app.onrender.com/health/

# Test authentication
curl -X POST https://your-app.onrender.com/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com","password":"testpass123"}'
```

---

## 📁 Files Created for Render

- `render.yaml` - Infrastructure as Code configuration
- `build.sh` - Build script with migrations
- `requirements.txt` - Updated with Render dependencies
- `config/settings.py` - Updated ALLOWED_HOSTS for Render

---

## 🆚 Render vs Railway Comparison

| Feature | Render | Railway |
|---------|---------|---------|
| **Free Tier** | ✅ 750 hours/month | ✅ $5 monthly credit |
| **Auto PostgreSQL** | ✅ Automatic | ✅ Automatic |
| **Custom Domains** | ✅ Free | ✅ Free |
| **Sleep Mode** | ⚠️ After 15min inactivity | ❌ No sleep |
| **Deploy Speed** | ⚠️ ~2-3 minutes | ✅ ~30 seconds |
| **Zero Config** | ✅ render.yaml | ✅ Automatic detection |

---

## 🐛 Troubleshooting

### **❌ Build Failed**
- Check `build.sh` is executable: `chmod +x build.sh`
- Verify all dependencies in `requirements.txt`

### **❌ Database Connection Error**
- Ensure `DATABASE_URL` is set correctly
- Check database is in same region as web service

### **❌ Static Files Not Loading**
- Render automatically serves static files with WhiteNoise
- Run `python manage.py collectstatic --noinput` in shell

### **❌ Service Sleeping**
- Free tier sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up

---

## 🎯 Production Readiness

### **Environment Variables to Set**
```bash
SECRET_KEY=generate-a-new-secret-key-for-production
DEBUG=false
DATABASE_URL=automatic-from-render-database
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
```

### **Custom Domain** (Optional)
1. Go to web service → Settings
2. Add your custom domain
3. Update DNS CNAME record

---

Your Django backend is now ready for Render deployment! 🚀

**Choose Method 1 (render.yaml) for the easiest deployment experience.** 