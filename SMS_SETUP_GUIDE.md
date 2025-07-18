# SMS/Mobile OTP Setup Guide

This guide shows you how to set up SMS services for sending mobile OTPs in your Travel Partner Platform.

## 🔧 Current Setup (Development Mode)

Your app is now configured to use **console backend** for mobile OTPs. This means:
- ✅ **Mobile OTP will be printed in Django terminal** (no actual SMS sent)
- ✅ **Perfect for testing** - no SMS service setup needed
- ✅ **Always works** - no external dependencies

### How to Test Right Now:
1. Use the frontend to send mobile OTP
2. **Check your Django terminal** - you'll see the OTP printed there
3. Copy the OTP and use it in the verification step

## 📱 Production SMS Services (Choose One)

### 1. 🟢 **Twilio (Most Popular)**
**Free Trial:** $15 credit (about 750 SMS)
**Pricing:** $0.0075 per SMS (very cheap)

```python
# Install Twilio
pip install twilio

# In your .env file:
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

**Setup Steps:**
1. Go to [twilio.com](https://twilio.com)
2. Sign up for free account (get $15 credit)
3. Get a phone number
4. Get Account SID and Auth Token
5. Add credentials to `.env` file

### 2. 🔵 **AWS SNS (Enterprise)**
**Pricing:** $0.00645 per SMS (very cheap)
**Good for:** Large scale applications

```python
# Install AWS SDK
pip install boto3

# Custom implementation needed for AWS SNS
```

### 3. 🟡 **Vonage (formerly Nexmo)**
**Free Trial:** €2 credit
**Pricing:** Similar to Twilio

```python
# Install Vonage
pip install vonage

# Custom implementation needed
```

### 4. 🟠 **MessageBird**
**Free Trial:** €20 credit
**Pricing:** Competitive rates

## 🚀 Quick Setup Instructions

### For Development (Current Setup):
```bash
# No setup needed! 
# Just check your Django terminal for mobile OTP codes
```

### For Production with Twilio:
```bash
# 1. Install Twilio
pip install twilio

# 2. Sign up at twilio.com and get credentials
# 3. Add to your .env file:
echo "TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" >> .env
echo "TWILIO_AUTH_TOKEN=your_auth_token_here" >> .env  
echo "TWILIO_PHONE_NUMBER=+1234567890" >> .env

# 4. Restart Django server
```

## 📋 Twilio Setup Steps (Detailed)

1. **Sign Up:**
   - Go to [twilio.com/try-twilio](https://twilio.com/try-twilio)
   - Create free account (get $15 trial credit)
   - Verify your phone number

2. **Get Phone Number:**
   - Go to Phone Numbers > Manage > Buy a number
   - Choose a number (usually $1/month)
   - Or use trial number for testing

3. **Get Credentials:**
   - Go to Console Dashboard
   - Copy "Account SID" 
   - Copy "Auth Token"
   - Note your Twilio phone number

4. **Add to .env:**
   ```
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_PHONE_NUMBER=+1234567890
   ```

## 🔍 Testing Different Modes

### Development Mode (Current):
```bash
# Send mobile OTP -> Check Django terminal
# You'll see:
# 🔧 CONSOLE FALLBACK - MOBILE OTP for +1234567890: 123456
# 📱 SMS Message: Your OTP is: 123456. This OTP will expire in 10 minutes.
```

### Production Mode (with Twilio):
```bash
# Send mobile OTP -> Real SMS sent to phone
# Django terminal shows:
# ✅ SMS OTP SENT to +1234567890: 123456
```

## 💰 Cost Comparison

| Service | Free Trial | SMS Cost | Best For |
|---------|------------|----------|----------|
| **Twilio** | $15 credit | $0.0075/SMS | Most popular, great docs |
| **AWS SNS** | Free tier | $0.00645/SMS | Enterprise, existing AWS users |
| **Vonage** | €2 credit | $0.008/SMS | Alternative to Twilio |
| **MessageBird** | €20 credit | Varies | European focus |

## 🛠️ Installation Commands

### Install Twilio:
```bash
cd /home/yash/office/apiproject
pip install twilio
pip freeze > requirements.txt  # Update requirements
```

### Install AWS SNS:
```bash
pip install boto3
```

## 🔄 How It Works

1. **Development:** 
   - No SMS service needed
   - OTPs printed in console
   - Perfect for testing API flow

2. **Production:**
   - Real SMS sent via Twilio/other service
   - Users receive OTP on their phones
   - More secure and professional

## 💡 Recommendations

- **For Learning/Testing:** Use current console backend (already working)
- **For MVP/Production:** Use Twilio ($15 free trial covers lots of testing)
- **For Enterprise:** Consider AWS SNS or Twilio with volume discounts

## 🚨 Important Notes

- **Phone Number Format:** Use international format (+1234567890)
- **Trial Limitations:** Twilio trial only sends to verified numbers
- **Production:** Remove trial limitations by adding payment method
- **Console Fallback:** Always works even if SMS service fails

Your mobile OTP functionality is now working for development testing! 🎯
