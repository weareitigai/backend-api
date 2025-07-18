#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

echo "🔧 Installing Python dependencies..."
pip install -r requirements.txt

echo "🔍 Checking Django configuration..."
python manage.py check --deploy

echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

echo "👤 Creating superuser from environment variables..."
python manage.py create_superuser_from_env

echo "📊 Collecting static files..."
python manage.py collectstatic --noinput

echo "🎯 Creating cache table (if needed)..."
python manage.py createcachetable || echo "Cache table might already exist"

echo "✅ Build completed successfully!"
echo "🚀 Ready to start with: gunicorn config.wsgi:application"