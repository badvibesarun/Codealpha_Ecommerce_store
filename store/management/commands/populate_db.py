from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, Product
import random


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample categories and products...')
        
        # Create categories
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Latest electronic gadgets and devices'
            },
            {
                'name': 'Clothing',
                'description': 'Fashion and apparel for all occasions'
            },
            {
                'name': 'Books',
                'description': 'Books, magazines, and educational materials'
            },
            {
                'name': 'Home & Garden',
                'description': 'Everything for your home and garden'
            },
            {
                'name': 'Sports',
                'description': 'Sports equipment and fitness gear'
            },
            {
                'name': 'Groceries',
                'description': 'Fresh food, beverages, and daily essentials'
            },
            {
                'name': 'Beauty & Health',
                'description': 'Skincare, cosmetics, and wellness products'
            },
            {
                'name': 'Toys & Games',
                'description': 'Fun toys, games, and entertainment for all ages'
            },
            {
                'name': 'Automotive',
                'description': 'Car accessories, tools, and automotive supplies'
            },
            {
                'name': 'Music & Movies',
                'description': 'Entertainment media, instruments, and accessories'
            }
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create products
        products_data = [
            # Electronics
            {'name': 'Smartphone Pro', 'category': 'Electronics', 'price': 899.99, 'description': 'Latest smartphone with advanced features and high-quality camera.'},
            {'name': 'Laptop Ultra', 'category': 'Electronics', 'price': 1299.99, 'description': 'Powerful laptop for work and gaming with fast processor and graphics.'},
            {'name': 'Wireless Headphones', 'category': 'Electronics', 'price': 199.99, 'description': 'Premium wireless headphones with noise cancellation.'},
            {'name': 'Smart Watch', 'category': 'Electronics', 'price': 299.99, 'description': 'Fitness tracking smartwatch with health monitoring features.'},
            
            # Clothing
            {'name': 'Cotton T-Shirt', 'category': 'Clothing', 'price': 24.99, 'description': 'Comfortable cotton t-shirt available in multiple colors.'},
            {'name': 'Denim Jeans', 'category': 'Clothing', 'price': 79.99, 'description': 'Classic denim jeans with perfect fit and durability.'},
            {'name': 'Winter Jacket', 'category': 'Clothing', 'price': 149.99, 'description': 'Warm winter jacket with water-resistant material.'},
            {'name': 'Running Shoes', 'category': 'Clothing', 'price': 119.99, 'description': 'Comfortable running shoes with excellent cushioning.'},
            
            # Books
            {'name': 'Python Programming Guide', 'category': 'Books', 'price': 39.99, 'description': 'Comprehensive guide to Python programming for beginners and experts.'},
            {'name': 'Web Development Handbook', 'category': 'Books', 'price': 44.99, 'description': 'Complete handbook for modern web development techniques.'},
            {'name': 'Science Fiction Novel', 'category': 'Books', 'price': 14.99, 'description': 'Exciting science fiction novel with thrilling adventures.'},
            
            # Home & Garden
            {'name': 'Coffee Maker', 'category': 'Home & Garden', 'price': 89.99, 'description': 'Automatic coffee maker with programmable features.'},
            {'name': 'Garden Tools Set', 'category': 'Home & Garden', 'price': 59.99, 'description': 'Complete set of essential garden tools for maintenance.'},
            {'name': 'LED Desk Lamp', 'category': 'Home & Garden', 'price': 34.99, 'description': 'Adjustable LED desk lamp with multiple brightness levels.'},
            
            # Sports
            {'name': 'Yoga Mat', 'category': 'Sports', 'price': 29.99, 'description': 'Non-slip yoga mat perfect for exercise and meditation.'},
            {'name': 'Basketball', 'category': 'Sports', 'price': 24.99, 'description': 'Official size basketball for indoor and outdoor play.'},
            {'name': 'Fitness Tracker', 'category': 'Sports', 'price': 79.99, 'description': 'Advanced fitness tracker with heart rate monitoring.'},

            # Groceries
            {'name': 'Organic Apples', 'category': 'Groceries', 'price': 4.99, 'description': 'Fresh organic apples, perfect for healthy snacking.'},
            {'name': 'Whole Grain Bread', 'category': 'Groceries', 'price': 3.49, 'description': 'Nutritious whole grain bread, freshly baked daily.'},
            {'name': 'Premium Coffee Beans', 'category': 'Groceries', 'price': 12.99, 'description': 'Artisan roasted coffee beans from sustainable farms.'},
            {'name': 'Greek Yogurt', 'category': 'Groceries', 'price': 5.99, 'description': 'Creamy Greek yogurt packed with protein and probiotics.'},

            # Beauty & Health
            {'name': 'Vitamin C Serum', 'category': 'Beauty & Health', 'price': 24.99, 'description': 'Anti-aging vitamin C serum for radiant skin.'},
            {'name': 'Moisturizing Face Cream', 'category': 'Beauty & Health', 'price': 18.99, 'description': 'Hydrating face cream for all skin types.'},
            {'name': 'Multivitamin Supplements', 'category': 'Beauty & Health', 'price': 19.99, 'description': 'Daily multivitamin for optimal health and wellness.'},

            # Toys & Games
            {'name': 'Building Blocks Set', 'category': 'Toys & Games', 'price': 34.99, 'description': 'Creative building blocks for imaginative play.'},
            {'name': 'Board Game Collection', 'category': 'Toys & Games', 'price': 29.99, 'description': 'Classic board games for family fun nights.'},
            {'name': 'Remote Control Car', 'category': 'Toys & Games', 'price': 49.99, 'description': 'High-speed remote control car with LED lights.'},

            # Automotive
            {'name': 'Car Phone Mount', 'category': 'Automotive', 'price': 15.99, 'description': 'Secure phone mount for hands-free driving.'},
            {'name': 'Car Air Freshener', 'category': 'Automotive', 'price': 8.99, 'description': 'Long-lasting car air freshener with natural scents.'},
            {'name': 'Emergency Kit', 'category': 'Automotive', 'price': 39.99, 'description': 'Complete emergency kit for roadside assistance.'},

            # Music & Movies
            {'name': 'Bluetooth Speaker', 'category': 'Music & Movies', 'price': 59.99, 'description': 'Portable Bluetooth speaker with premium sound quality.'},
            {'name': 'Guitar Picks Set', 'category': 'Music & Movies', 'price': 9.99, 'description': 'Professional guitar picks in various thicknesses.'},
            {'name': 'Movie Collection Box Set', 'category': 'Music & Movies', 'price': 79.99, 'description': 'Classic movie collection in high-definition format.'},
        ]
        
        for product_data in products_data:
            category = Category.objects.get(name=product_data['category'])
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'slug': slugify(product_data['name']),
                    'category': category,
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'stock': random.randint(5, 50),
                    'available': True
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
