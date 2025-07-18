#!/bin/bash

# Django API Project Setup Script

echo "🚀 Setting up Django API Project..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip first
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

# Check if Django was installed successfully
if ! python -c "import django" 2>/dev/null; then
    echo "❌ Django installation failed. Trying alternative approach..."
    echo "📚 Installing core dependencies individually..."
    pip install Django==4.2.7
    pip install djangorestframework==3.14.0
    pip install django-cors-headers==4.3.1
    pip install python-decouple==3.8
    pip install drf-spectacular==0.26.5
    pip install django-filter==23.4
    
    # Skip optional packages that might have issues
    echo "⚠️  Skipping optional packages due to compatibility issues..."
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update the .env file with your actual configuration values"
fi

# Make migrations
echo "🔧 Creating database migrations..."
python manage.py makemigrations

# Apply migrations
echo "🗄️  Applying database migrations..."
python manage.py migrate

# Populate sample data
echo "📊 Populating sample data..."
python manage.py populate_sample_data

# Create superuser (optional)
echo "👤 Creating superuser (optional)..."
read -p "Do you want to create a superuser? (y/N): " create_superuser
if [[ $create_superuser =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🏃 To start the development server, run:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "📖 API Documentation will be available at:"
echo "   http://127.0.0.1:8000/api/docs/"
echo ""
echo "🔧 Admin panel will be available at:"
echo "   http://127.0.0.1:8000/admin/"
echo ""
