# ShopSphere - Digital Marketplace

A production-ready e-commerce web application built with Django, featuring product management, user authentication, shopping cart functionality, and order processing. ShopSphere connects customers to a world of premium products with an exceptional shopping experience.

🚀 **Ready for Production Deployment** - Optimized for Vercel, Heroku, and other cloud platforms.

## Features

### Core Functionality
- **Product Management**: Browse products by category, view detailed product information
- **User Authentication**: User registration, login, and logout functionality
- **Shopping Cart**: Add/remove items, update quantities, persistent cart storage
- **Order Processing**: Complete checkout process with order history
- **Admin Interface**: Django admin for managing products, categories, and orders

### Frontend Features
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5
- **Interactive UI**: JavaScript enhancements for better user experience
- **Product Search**: Browse products by category
- **Real-time Updates**: AJAX cart updates and form validation

## Technology Stack

### Backend
- **Django 5.2.4**: Web framework
- **Python 3.13**: Programming language
- **SQLite**: Database (development)
- **Pillow**: Image processing

### Frontend
- **HTML5/CSS3**: Markup and styling
- **Bootstrap 5**: CSS framework
- **JavaScript**: Interactive functionality
- **Font Awesome**: Icons

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Codealpha_Ecommerce
   ```

2. **Create virtual environment**
   ```bash
   python -m venv ecommerce_env
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   ecommerce_env\Scripts\activate
   
   # Linux/Mac
   source ecommerce_env/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Populate database with sample data**
   ```bash
   python manage.py populate_db
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access ShopSphere**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### For Customers
1. **Browse Products**: Visit the home page to see featured products or browse by category
2. **Register/Login**: Create an account or login to existing account
3. **Add to Cart**: Add products to your shopping cart
4. **Checkout**: Complete the purchase process with shipping information
5. **Order History**: View your past orders and their status

### For Administrators
1. **Access Admin Panel**: Login to /admin/ with superuser credentials
2. **Manage Categories**: Add, edit, or delete product categories
3. **Manage Products**: Add new products, update inventory, set prices
4. **Process Orders**: View and update order status
5. **User Management**: Manage customer accounts

## Project Structure

```
Codealpha_Ecommerce/
├── ecommerce_store/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                    # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # URL patterns
│   ├── forms.py             # Django forms
│   ├── admin.py             # Admin configuration
│   ├── tests.py             # Test cases
│   ├── templates/           # HTML templates
│   └── management/          # Custom management commands
├── static/                   # Static files
│   ├── css/                 # Custom CSS
│   └── js/                  # Custom JavaScript
├── media/                    # User uploaded files
├── requirements.txt          # Python dependencies
└── manage.py                # Django management script
```

## Models

- **Category**: Product categories with name, slug, and description
- **Product**: Products with name, price, description, image, and stock
- **Cart**: User shopping carts
- **CartItem**: Individual items in shopping carts
- **Order**: Customer orders with shipping information
- **OrderItem**: Individual items in orders

## API Endpoints

- `/` - Home page with featured products
- `/products/` - Product listing page
- `/category/<slug>/` - Products by category
- `/product/<slug>/` - Product detail page
- `/cart/` - Shopping cart
- `/checkout/` - Checkout process
- `/orders/` - Order history
- `/register/` - User registration
- `/login/` - User login
- `/admin/` - Admin interface

## Testing

Run the test suite:
```bash
python manage.py test
```

The project includes comprehensive tests for:
- Model functionality
- View responses
- Authentication
- Cart operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 🚀 Production Deployment

This application is production-ready and can be deployed to various platforms:

### Quick Deploy to Vercel

1. Fork this repository
2. Connect to Vercel
3. Set environment variables (see `DEPLOYMENT.md`)
4. Deploy automatically

### Other Platforms

- **Heroku**: Supported with included `Procfile`
- **Railway**: Auto-deployment ready
- **DigitalOcean**: Compatible with App Platform

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## License

This project is created for educational purposes as part of the CodeAlpha internship program.

## Support

For questions or issues, please contact the development team or create an issue in the repository.
