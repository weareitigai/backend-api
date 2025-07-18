#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

echo "🔧 Installing Python dependencies..."
pip install -r requirements.txt

echo "📊 Collecting static files..."
python manage.py collectstatic --noinput

echo "🗄️ Running database migrations..."
python manage.py migrate

echo "✅ Build completed successfully!" 