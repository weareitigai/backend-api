# Django Admin Superuser Setup via Environment Variables

This guide explains how to create Django admin superusers using environment variables, which is particularly useful for deployment scenarios.

## 🚀 Quick Setup

### 1. Configure Environment Variables

Add these variables to your `.env` file:

```bash
# Django Admin Superuser (optional - for automatic creation)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123
CREATE_SUPERUSER=true
```

### 2. Create Superuser

Run the management command:

```bash
python manage.py create_superuser_from_env
```

## 🔧 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `CREATE_SUPERUSER` | Enable/disable superuser creation | `false` | Yes |
| `DJANGO_SUPERUSER_USERNAME` | Admin username | None | Yes (if enabled) |
| `DJANGO_SUPERUSER_EMAIL` | Admin email address | None | Yes (if enabled) |
| `DJANGO_SUPERUSER_PASSWORD` | Admin password | None | Yes (if enabled) |

## 📋 Usage Examples

### Local Development

```bash
# Set environment variables in .env
CREATE_SUPERUSER=true
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@localhost
DJANGO_SUPERUSER_PASSWORD=dev123

# Create superuser
python manage.py create_superuser_from_env
```

### Production Deployment

For production environments (Railway, Render, etc.), set these as environment variables:

```bash
CREATE_SUPERUSER=true
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourcompany.com
DJANGO_SUPERUSER_PASSWORD=your-secure-password
```

### Railway Deployment

Add these environment variables in Railway dashboard:

1. Go to your Railway project
2. Click on your Django service
3. Go to "Variables" tab
4. Add:
   - `CREATE_SUPERUSER=true`
   - `DJANGO_SUPERUSER_USERNAME=admin`
   - `DJANGO_SUPERUSER_EMAIL=admin@yourcompany.com`
   - `DJANGO_SUPERUSER_PASSWORD=your-secure-password`

### Render Deployment

The superuser will be created automatically during build process via `build.sh`.

Set environment variables in Render dashboard:

1. Go to your web service
2. Click "Environment"
3. Add the superuser variables listed above

## 🛠️ Command Options

### Basic Usage
```bash
python manage.py create_superuser_from_env
```

### Force Update Existing User
```bash
python manage.py create_superuser_from_env --force
```

This will update an existing superuser with new values from environment variables.

## 🔐 Security Best Practices

### 1. Strong Passwords
Always use strong passwords for production environments:

```bash
DJANGO_SUPERUSER_PASSWORD=MyStr0ng!P@ssw0rd2024
```

### 2. Secure Email
Use a real email address for password recovery:

```bash
DJANGO_SUPERUSER_EMAIL=admin@yourcompany.com
```

### 3. Environment-Specific Usernames
Consider different usernames for different environments:

```bash
# Development
DJANGO_SUPERUSER_USERNAME=dev_admin

# Production
DJANGO_SUPERUSER_USERNAME=prod_admin
```

### 4. Disable in Production
For production, you might want to disable automatic creation after initial setup:

```bash
CREATE_SUPERUSER=false
```

## 🚨 Troubleshooting

### Superuser Already Exists
```
Superuser "admin" already exists. Use --force to update.
```

**Solution**: Use `--force` flag to update:
```bash
python manage.py create_superuser_from_env --force
```

### Missing Environment Variables
```
Missing required environment variables: DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD
```

**Solution**: Set all required variables in your `.env` file.

### Creation Disabled
```
Superuser creation disabled. Set CREATE_SUPERUSER=true in .env to enable.
```

**Solution**: Set `CREATE_SUPERUSER=true` in your environment variables.

## 🔄 Integration with Setup Scripts

### Automatic Creation in setup.sh
The `setup.sh` script now offers three options:
1. Create from environment variables
2. Create interactively
3. Skip

### Automatic Creation in build.sh
The `build.sh` script (used by Render) automatically creates the superuser during deployment.

## 📱 Admin Panel Access

After creating the superuser, access the admin panel at:

### Local Development
```
http://localhost:8000/admin/
```

### Railway Deployment
```
https://your-app-name.railway.app/admin/
```

### Render Deployment
```
https://your-service-name.onrender.com/admin/
```

## 🔍 Verification

Check if superuser was created successfully:

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
User = get_user_model()

# Check if superuser exists
admin_user = User.objects.filter(username='admin', is_superuser=True).first()
if admin_user:
    print(f"Superuser exists: {admin_user.username} ({admin_user.email})")
else:
    print("No superuser found")
```

## 💡 Pro Tips

1. **Environment-specific configs**: Use different `.env` files for different environments
2. **CI/CD Integration**: Include the command in your deployment pipelines
3. **Backup credentials**: Store admin credentials securely for production
4. **Regular updates**: Periodically update admin passwords using `--force` flag
5. **Multiple admins**: Create additional admin users as needed for team access

This approach ensures consistent superuser creation across all deployment environments while maintaining security best practices. 