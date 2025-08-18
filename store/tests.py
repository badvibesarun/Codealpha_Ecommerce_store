from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from .models import Category, Product, Cart, CartItem, Order, OrderItem


class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            description='Test category description'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=self.category,
            description='Test product description',
            price=Decimal('99.99'),
            stock=10,
            available=True
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(str(self.category), 'Test Category')

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, Decimal('99.99'))
        self.assertEqual(str(self.product), 'Test Product')

    def test_cart_creation(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
        self.assertEqual(cart.get_total_items(), 0)
        self.assertEqual(cart.get_total_price(), 0)

    def test_cart_item_creation(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.get_total_price(), Decimal('199.98'))
        self.assertEqual(cart.get_total_items(), 2)


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            description='Test category description'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=self.category,
            description='Test product description',
            price=Decimal('99.99'),
            stock=10,
            available=True
        )

    def test_home_view(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Our Store')

    def test_product_list_view(self):
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_product_detail_view(self):
        response = self.client.get(reverse('store:product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_category_product_list_view(self):
        response = self.client.get(reverse('store:product_list_by_category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_cart_view_requires_login(self):
        response = self.client.get(reverse('store:cart_detail'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_add_to_cart_requires_login(self):
        response = self.client.post(reverse('store:add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_authenticated_cart_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('store:cart_detail'))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('store:add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after adding

        # Check if cart item was created
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().product, self.product)


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_registration(self):
        response = self.client.post(reverse('store:register'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        response = self.client.post(reverse('store:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
