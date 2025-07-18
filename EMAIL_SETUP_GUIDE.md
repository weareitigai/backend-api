# Email Service Setup Guide for OTP Delivery

This guide shows you how to set up different email services for sending OTPs in your Travel Partner Platform.

## 🔧 Current Setup (Development Mode)

Your app is now configured to use **console backend** for development. This means:
- ✅ **OTP will be printed in Django terminal** (no actual email sent)
- ✅ **Perfect for testing** - no email service setup needed
- ✅ **Always works** - no external dependencies

### How to Test Right Now:
1. Start your Django server
2. Use the frontend to send email OTP
3. **Check your Django terminal** - you'll see the OTP printed there
4. Copy the OTP and use it in the verification step

## 📧 Production Email Services (Choose One)

### 1. 🟢 **Resend (Recommended - Easiest)**
**Free Tier:** 3,000 emails/month
```python
# In your .env file:
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.resend.com
EMAIL_PORT=587
EMAIL_HOST_USER=resend
EMAIL_HOST_PASSWORD=your_resend_api_key
```

**Setup Steps:**
1. Go to [resend.com](https://resend.com)
2. Sign up for free account
3. Get your API key
4. Add your API key to `.env` file
5. Set `DEBUG=False` in settings or override email backend

### 2. 🟡 **SendGrid (Very Reliable)**
**Free Tier:** 100 emails/day forever
```python
# In your .env file:
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your_sendgrid_api_key
```

**Setup Steps:**
1. Go to [sendgrid.com](https://sendgrid.com)
2. Sign up for free account
3. Create an API key
4. Add API key to `.env` file

### 3. 🔵 **Gmail (Traditional)**
**Free Tier:** 100 emails/day
```python
# In your .env file:
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

**Setup Steps:**
1. Enable 2-Factor Authentication on Gmail
2. Generate App Password (not your regular password)
3. Use the app password in `.env` file

### 4. 🟠 **Mailtrap (Testing Only)**
**Free Tier:** 100 emails/month (emails don't actually send)
```python
# In your .env file:
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=2525
EMAIL_HOST_USER=your_mailtrap_username
EMAIL_HOST_PASSWORD=your_mailtrap_password
```

## 🚀 Quick Setup Instructions

### For Development (Current Setup):
```bash
# No setup needed! 
# Just check your Django terminal for OTP codes
```

### For Production with Resend:
```bash
# 1. Sign up at resend.com
# 2. Get your API key
# 3. Add to your .env file:
echo "EMAIL_HOST_PASSWORD=re_your_api_key_here" >> .env
echo "DEBUG=False" >> .env  # This will enable SMTP backend
```

### For Production with SendGrid:
```bash
# 1. Sign up at sendgrid.com
# 2. Create API key
# 3. Add to your .env file:
echo "EMAIL_HOST=smtp.sendgrid.net" >> .env
echo "EMAIL_HOST_USER=apikey" >> .env
echo "EMAIL_HOST_PASSWORD=SG.your_api_key_here" >> .env
echo "DEBUG=False" >> .env
```

## 🔍 How to Test Email Services

1. **Development Mode (Current):**
   - OTPs appear in Django terminal
   - No email service needed
   - Perfect for testing API functionality

2. **Production Mode:**
   - Real emails sent to users
   - Requires email service setup
   - Test with real email addresses

## 💡 Recommendations

- **For Learning/Development:** Use current console backend (already set up)
- **For MVP/Small Projects:** Use Resend (3,000 emails/month free)
- **For Established Projects:** Use SendGrid (reliable, widely used)
- **For Gmail Users:** Use Gmail with app passwords

## 🛠️ Switch Between Services

Your app automatically detects the environment:
- `DEBUG=True` → Console backend (development)
- `DEBUG=False` → SMTP backend (production)

You can also override by setting `EMAIL_BACKEND` directly in `.env`:
```bash
# Force console backend even in production
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Force SMTP backend even in development  
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```
