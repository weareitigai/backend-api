# SendGrid Email OTP Integration Guide

## Overview
This project now supports Twilio SendGrid for sending email OTPs with enhanced HTML templates and better error handling.

## Setup Instructions

### 1. SendGrid Account Setup

1. **Create a SendGrid Account**: Go to https://sendgrid.com and create an account
2. **Verify Your Email**: Complete the email verification process
3. **Add a Sender Identity**: 
   - Go to Settings > Sender Authentication
   - Add a single sender or verify a domain
   - Use this verified email as your `DEFAULT_FROM_EMAIL`

### 2. API Key Configuration

1. **Create API Key**:
   - Go to Settings > API Keys
   - Click "Create API Key"
   - Choose "Restricted Access" and enable:
     - Mail Send (Full Access)
     - Mail Settings (Read Access)
   - Copy the API key (you won't see it again!)

2. **Update Environment Variables**:
   ```bash
   EMAIL_BACKEND=sendgrid
   SENDGRID_API_KEY=your-actual-api-key-here
   DEFAULT_FROM_EMAIL=your-verified-email@domain.com
   FROM_NAME=Travel Partner Platform
   ```

### 3. Test the Integration

Run the test script:
```bash
python test_sendgrid_integration.py
```

## Features

✅ **HTML Email Templates**: Beautiful, responsive email templates  
✅ **Plain Text Fallback**: Automatic plain text version for all emails  
✅ **Multiple Backend Support**: SendGrid, SMTP, or console backends  
✅ **Graceful Fallback**: Automatic fallback if SendGrid fails  
✅ **Error Handling**: Comprehensive error handling and logging  
✅ **Testing Tools**: Built-in test scripts for validation  

## Email Template Features

- Professional HTML design
- Responsive layout
- Clear OTP display with large, readable font
- Security warnings and expiry information
- Branded header and footer
- Mobile-friendly design

## Troubleshooting

### Common Issues

1. **403 Forbidden Error**
   - Verify your sender email in SendGrid dashboard
   - Check API key permissions (Mail Send must be enabled)
   - Ensure your account is not in sandbox mode for production

2. **From Email Not Verified**
   - Go to SendGrid > Settings > Sender Authentication
   - Add and verify your sender email address
   - Update `DEFAULT_FROM_EMAIL` in your .env file

3. **Rate Limits**
   - Free accounts have sending limits
   - Check your SendGrid dashboard for usage stats
   - Consider upgrading if you hit limits

### Debug Mode

To test without sending real emails, set:
```bash
EMAIL_BACKEND=console
```

This will print emails to the console instead of sending them.

## API Endpoints

The email OTP functionality is available through these endpoints:

- `POST /api/auth/send-email-otp/` - Send OTP to email
- `POST /api/auth/verify-email-otp/` - Verify OTP code

Example usage:
```bash
# Send OTP
curl -X POST http://localhost:8000/api/auth/send-email-otp/ \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com"}'

# Verify OTP
curl -X POST http://localhost:8000/api/auth/verify-email-otp/ \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "otp": "123456"}'
```

## Production Considerations

1. **Environment Variables**: Never commit API keys to version control
2. **Email Verification**: Always verify sender emails in SendGrid
3. **Rate Limiting**: Implement application-level rate limiting for OTP requests
4. **Monitoring**: Monitor SendGrid dashboard for delivery rates and bounces
5. **Backup**: Keep SMTP configuration as fallback option
