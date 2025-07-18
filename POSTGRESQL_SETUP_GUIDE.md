# PostgreSQL Setup Guide

This guide will help you set up PostgreSQL for the Travel Partner API project.

## Quick Setup (Automated)

For a quick automated setup, you can use the migration script:

```bash
./migrate_to_postgresql.sh
```

This script will:
- Check PostgreSQL installation and service
- Create database and user with auto-generated credentials
- Create and configure .env file
- Install Python dependencies
- Run migrations
- Remove old SQLite database

## Manual Setup (Detailed)

Follow the steps below for a manual setup with custom configuration.

## Prerequisites

Make sure you have PostgreSQL installed on your system.

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### macOS (using Homebrew)
```bash
brew install postgresql
brew services start postgresql
```

### Windows
Download and install PostgreSQL from: https://www.postgresql.org/download/windows/

## Database Setup

### 1. Access PostgreSQL
```bash
sudo -u postgres psql
```

### 2. Create Database and User
```sql
-- Create database
CREATE DATABASE travel_partner_db;

-- Create user
CREATE USER travel_partner_user WITH PASSWORD 'your_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE travel_partner_db TO travel_partner_user;

-- For Django migrations (required in newer PostgreSQL versions)
ALTER USER travel_partner_user CREATEDB;

-- Exit PostgreSQL
\q
```

### 3. Environment Configuration

Create a `.env` file in the project root (if it doesn't exist) with the following database configuration:

```env
# Database Configuration
DB_NAME=travel_partner_db
DB_USER=travel_partner_user
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# Other configuration (keep existing values)
SECRET_KEY=your-secret-key-here
DEBUG=True

# Email Configuration (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Twilio Configuration (optional)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number
```

**Important:** Replace `your_password_here` with a strong password for your database user.

## Migration Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test Database Connection
```bash
python manage.py check --database default
```

### 3. Run Migrations
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Load Sample Data (Optional)
```bash
python manage.py populate_sample_data
```

## Verification

### 1. Start Development Server
```bash
python manage.py runserver
```

### 2. Check Database Connection
Visit `http://localhost:8000/admin/` and log in with your superuser credentials to verify the database is working.

### 3. Test APIs
You can use the frontend (`cd frontend && npm start`) or test the APIs directly:
- `http://localhost:8000/api/auth/`
- `http://localhost:8000/api/partner/`
- `http://localhost:8000/api/common/`

## Troubleshooting

### Connection Issues
1. **Check PostgreSQL Service:**
   ```bash
   # Ubuntu/Debian
   sudo systemctl status postgresql
   sudo systemctl start postgresql
   
   # macOS
   brew services list | grep postgresql
   brew services start postgresql
   ```

2. **Check Database Exists:**
   ```bash
   sudo -u postgres psql -l
   ```

3. **Check User Permissions:**
   ```sql
   sudo -u postgres psql
   \du
   ```

### Authentication Issues
1. **Update pg_hba.conf** (if needed):
   ```bash
   # Find the file location
   sudo -u postgres psql -c "SHOW hba_file;"
   
   # Edit the file and ensure this line exists:
   # local   all             all                                     md5
   
   # Restart PostgreSQL
   sudo systemctl restart postgresql
   ```

### Common Errors

**Error:** `django.db.utils.OperationalError: could not connect to server`
- **Solution:** Ensure PostgreSQL is running and the connection parameters in `.env` are correct.

**Error:** `django.db.utils.OperationalError: FATAL: database "travel_partner_db" does not exist`
- **Solution:** Create the database using the SQL commands above.

**Error:** `django.db.utils.OperationalError: FATAL: password authentication failed`
- **Solution:** Check the username and password in your `.env` file.

## Security Notes

1. **Never commit `.env` files** to version control
2. **Use strong passwords** for database users
3. **Limit database user privileges** in production
4. **Configure PostgreSQL firewall rules** in production
5. **Use SSL connections** in production

## Production Considerations

For production deployment:

1. **Use environment-specific databases**
2. **Enable SSL/TLS connections**
3. **Configure connection pooling**
4. **Set up database backups**
5. **Monitor database performance**
6. **Use read replicas** for scaling

## Backup and Restore

### Create Backup
```bash
pg_dump -U travel_partner_user -h localhost travel_partner_db > backup.sql
```

### Restore Backup
```bash
psql -U travel_partner_user -h localhost travel_partner_db < backup.sql
```

## Next Steps

After PostgreSQL setup is complete:
1. Remove the old SQLite database file: `rm db.sqlite3`
2. Test all API endpoints
3. Verify frontend integration
4. Run the Quick Test API to ensure full flow works
