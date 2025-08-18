#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit  # exit on error

echo "🚀 Starting build process..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

# Create media directory and copy files
echo "📁 Setting up media directory..."

# In Render, we're already in /opt/render/project/src/, so files are in the right place
# Just ensure the media directory exists and show the files
if [ -d "media/products" ] && [ "$(ls -A media/products 2>/dev/null)" ]; then
    echo "Media files found in repository:"
    ls -la media/products/ | head -10
    echo "Total media files: $(ls media/products/ | wc -l)"
    echo "Media directory path: $(pwd)/media"
    echo "Media files are ready for serving"
    
    # Test if files can be accessed
    echo "Testing file access:"
    if [ -f "media/products/smartphone-pro_ultra_precise.jpg" ]; then
        echo "✓ smartphone-pro_ultra_precise.jpg exists and is accessible"
        ls -la "media/products/smartphone-pro_ultra_precise.jpg"
    else
        echo "✗ smartphone-pro_ultra_precise.jpg not found"
    fi
else
    echo "No media files found in repository"
    echo "Repository contents:"
    ls -la media/ || echo "No media directory found"
fi

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Load initial data
echo "📥 Loading initial data..."
if [ -f initial_data.json ]; then
    echo "Found initial_data.json"
    
    # Ensure the file has correct line endings
    dos2unix initial_data.json || true
    
    # Clean any BOM characters
    sed -i '1s/^\xEF\xBB\xBF//' initial_data.json
    
    echo "Verifying JSON..."
    if python -c "
import json
with open('initial_data.json', 'r') as f:
    json.load(f)
print('JSON is valid')
    "; then
        echo "Loading data..."
        python manage.py loaddata initial_data.json --verbosity 3
        
        echo "Checking media configuration..."
        python manage.py check_media
        
        echo "Verifying loaded data..."
        python manage.py shell -c "
from store.models import Product, Category
print(f'Products in database: {Product.objects.count()}')
print(f'Categories in database: {Category.objects.count()}')
for p in Product.objects.all():
    print(f'Product: {p.name} (Category: {p.category.name if p.category else None})')
"
    else
        echo "Error: initial_data.json is not valid JSON"
        echo "Content of initial_data.json:"
        cat initial_data.json
    fi
else
    echo "initial_data.json not found!"
    ls -la
fi

# Create superuser if environment variables are set
if [[ $CREATE_SUPERUSER == "true" ]]; then
    echo "👤 Creating superuser..."
    python manage.py setup_production --create-superuser || echo "Warning: Superuser creation failed, continuing..."
fi

echo "Setting up production environment..."
echo "Running database migrations..."
python manage.py migrate
echo "✓ Database migrations completed"
echo "Collecting static files..."
python manage.py collectstatic --no-input
echo "✓ Static files collected"

echo "✅ Build completed successfully!"
