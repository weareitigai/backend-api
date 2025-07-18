#!/bin/bash

# PostgreSQL Migration Script
# This script helps migrate from SQLite to PostgreSQL

echo "=== Travel Partner API - PostgreSQL Migration ==="
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is not installed. Please install it first:"
    echo "   Ubuntu/Debian: sudo apt install postgresql postgresql-contrib"
    echo "   macOS: brew install postgresql"
    echo "   Windows: Download from https://www.postgresql.org/download/windows/"
    exit 1
fi

echo "✅ PostgreSQL is installed"

# Check if PostgreSQL service is running
if ! pg_isready &> /dev/null; then
    echo "⚠️  PostgreSQL service is not running. Starting it..."
    if command -v systemctl &> /dev/null; then
        sudo systemctl start postgresql
    elif command -v brew &> /dev/null; then
        brew services start postgresql
    else
        echo "❌ Unable to start PostgreSQL service. Please start it manually."
        exit 1
    fi
fi

echo "✅ PostgreSQL service is running"

# Database configuration
DB_NAME="travel_partner_db"
DB_USER="travel_partner_user"
DB_PASSWORD="travel_partner_pass_$(date +%s)"

echo ""
echo "=== Database Setup ==="
echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo "Password: $DB_PASSWORD"
echo ""

# Create database and user
echo "Creating database and user..."
sudo -u postgres psql << EOF
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
ALTER USER $DB_USER CREATEDB;
\q
EOF

if [ $? -eq 0 ]; then
    echo "✅ Database and user created successfully"
else
    echo "❌ Failed to create database and user"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.template .env
    
    # Update .env with database credentials
    sed -i "s/DB_NAME=.*/DB_NAME=$DB_NAME/" .env
    sed -i "s/DB_USER=.*/DB_USER=$DB_USER/" .env
    sed -i "s/DB_PASSWORD=.*/DB_PASSWORD=$DB_PASSWORD/" .env
    
    # Generate a random secret key
    SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    
    echo "✅ .env file created and configured"
else
    echo "⚠️  .env file already exists. Please update it manually with:"
    echo "   DB_NAME=$DB_NAME"
    echo "   DB_USER=$DB_USER"
    echo "   DB_PASSWORD=$DB_PASSWORD"
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Test database connection
echo ""
echo "Testing database connection..."
python manage.py check --database default

if [ $? -eq 0 ]; then
    echo "✅ Database connection successful"
else
    echo "❌ Database connection failed"
    exit 1
fi

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully"
else
    echo "❌ Migrations failed"
    exit 1
fi

# Remove old SQLite database if it exists
if [ -f "db.sqlite3" ]; then
    echo ""
    echo "Removing old SQLite database..."
    rm db.sqlite3
    echo "✅ SQLite database removed"
fi

echo ""
echo "=== Migration Complete! ==="
echo ""
echo "✅ PostgreSQL database is set up and ready"
echo "✅ Migrations have been applied"
echo "✅ SQLite database has been removed"
echo ""
echo "Next steps:"
echo "1. Create a superuser: python manage.py createsuperuser"
echo "2. Load sample data: python manage.py populate_sample_data"
echo "3. Start the server: python manage.py runserver"
echo ""
echo "Database credentials (save these securely):"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"
echo "  Password: $DB_PASSWORD"
echo ""
echo "Frontend setup (optional):"
echo "  cd frontend && npm install && npm start"
echo ""
