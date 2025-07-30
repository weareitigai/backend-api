# Authentication Setup Guide

## 🔐 **Token Authentication Configuration**

This project uses **Django REST Framework TokenAuthentication** with the following format:

### **Correct Token Format**
```
Authorization: Token <your_token_here>
```

**NOT:**
```
Authorization: Bearer <your_token_here>
```

---

## 📋 **How to Use Authentication**

### **1. Login to Get Token**
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "user": { ... },
  "token": "878f2d8c25c17b3e80756604ca233b0194346582"
}
```

### **2. Use Token in API Requests**
```bash
GET /api/auth/profile/
Authorization: Token 878f2d8c25c17b3e80756604ca233b0194346582
```

---

## 🛠️ **Configuration Details**

### **Backend (Django)**
- **Authentication Class:** `rest_framework.authentication.TokenAuthentication`
- **Token Format:** `Token <token>`
- **Token Storage:** Django's built-in Token model

### **Frontend (React)**
- **Token Storage:** `localStorage.getItem('access_token')`
- **Header Format:** `Authorization: Token ${token}`
- **Auto-injection:** Via axios interceptors

### **Swagger UI**
- **Security Scheme:** `Token` (apiKey)
- **Header Name:** `Authorization`
- **Description:** `Token-based authentication. Use format: Token <your_token>`

---

## 🔧 **Testing Authentication**

### **Using Swagger UI**
1. Go to `/api/docs/`
2. Click "Authorize" button
3. Enter your token with format: `Token <your_token>`
4. Click "Authorize"

### **Using Postman**
1. Set header: `Authorization: Token <your_token>`
2. Make authenticated requests

### **Using Frontend**
1. Login via `/partner/login`
2. Token is automatically stored and used
3. No manual configuration needed

---

## ❌ **Common Issues & Solutions**

### **Issue: "Invalid token" errors**
**Solution:** Ensure you're using `Token` prefix, not `Bearer`

### **Issue: Swagger UI shows wrong format**
**Solution:** Updated configuration in `config/settings.py`

### **Issue: Frontend not sending token**
**Solution:** Check localStorage for `access_token` and axios interceptors

---

## 🔄 **Token Lifecycle**

1. **Login:** User logs in → receives token
2. **Storage:** Token stored in localStorage as `access_token`
3. **Usage:** Token automatically added to all API requests
4. **Logout:** Token deleted from localStorage and backend

---

## 📝 **API Endpoints Requiring Authentication**

- `GET /api/auth/profile/` - Get user profile
- `POST /api/auth/logout/` - Logout user
- `POST /api/auth/change-password/` - Change password
- `GET /api/partner/status/` - Get partner status
- `PATCH /api/partner/business-details/` - Update business details
- `PATCH /api/partner/location-coverage/` - Update location coverage
- `PATCH /api/partner/tours-services/` - Update tours/services
- `PATCH /api/partner/legal-banking/` - Update legal/banking details

---

## 🚀 **Quick Test**

```bash
# 1. Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# 2. Use token (replace TOKEN_HERE with actual token)
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Token TOKEN_HERE"
``` 