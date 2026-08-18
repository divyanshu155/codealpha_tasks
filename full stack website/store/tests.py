from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Category, Product, Order, OrderItem
from decimal import Decimal

class StoreModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Audio', slug='audio', icon='headphones')
        self.product = Product.objects.create(
            name='Test Headphones',
            slug='test-headphones',
            category=self.category,
            description='Awesome test sound',
            price=Decimal('150.00'),
            original_price=Decimal('200.00'),
            image_url='http://example.com/test.jpg',
            stock=10
        )

    def test_product_creation_and_discount(self):
        self.assertEqual(self.product.name, 'Test Headphones')
        self.assertEqual(self.product.discount_percent, 25)

    def test_order_creation(self):
        order = Order.objects.create(
            full_name='Jane Doe',
            email='jane@example.com',
            address='123 Main St',
            city='San Jose',
            postal_code='95112',
            total_amount=Decimal('150.00')
        )
        self.assertTrue(order.order_number.startswith('ORD-'))

class StoreViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Gadgets', slug='gadgets')
        self.product = Product.objects.create(
            name='Smart Gadget',
            slug='smart-gadget',
            category=self.category,
            description='Smart gadget description',
            price=Decimal('99.99'),
            stock=5
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smart Gadget')

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=['smart-gadget']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smart gadget description')

    def test_cart_add_and_session(self):
        response = self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': 2})
        self.assertEqual(response.status_code, 302) # Redirects to cart_detail
        session = self.client.session
        self.assertIn(str(self.product.id), session['cart'])
        self.assertEqual(session['cart'][str(self.product.id)]['quantity'], 2)

    def test_checkout_process(self):
        # Add item to cart first
        self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': 1})
        
        # Submit checkout form
        response = self.client.post(reverse('checkout'), {
            'full_name': 'Test Buyer',
            'email': 'buyer@example.com',
            'address': '456 Tech Ave',
            'city': 'San Francisco',
            'postal_code': '94107',
            'country': 'United States',
            'payment_method': 'Credit Card'
        })
        self.assertEqual(response.status_code, 302) # Redirects to order_success
        
        # Verify order was created in DB
        order = Order.objects.filter(email='buyer@example.com').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.full_name, 'Test Buyer')
        self.assertEqual(OrderItem.objects.filter(order=order).count(), 1)
