from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds initial database with sample categories, products, and admin user'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database data...')

        # Create Admin User if doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created admin user (username: admin, password: admin123)'))

        # Create Categories
        categories_data = [
            {'name': 'Audio & Sound', 'slug': 'audio-sound', 'icon': 'headphones'},
            {'name': 'Wearables', 'slug': 'wearables', 'icon': 'smartwatch'},
            {'name': 'Computers & Laptops', 'slug': 'computers-laptops', 'icon': 'laptop'},
            {'name': 'Smart Accessories', 'slug': 'smart-accessories', 'icon': 'gadget'},
        ]

        cat_objs = {}
        for cat_info in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_info['slug'],
                defaults={'name': cat_info['name'], 'icon': cat_info['icon']}
            )
            cat_objs[cat.slug] = cat

        products_data = [
            {
                'name': 'Apex Pro Wireless ANC Headphones',
                'slug': 'apex-pro-wireless-anc-headphones',
                'category': cat_objs['audio-sound'],
                'description': 'Experience studio-quality audio with Active Noise Cancellation, custom 40mm titanium drivers, ultra-soft memory foam earcups, and up to 45 hours of battery playback.',
                'price': Decimal('249.99'),
                'original_price': Decimal('299.99'),
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80',
                'stock': 25,
                'rating': Decimal('4.9'),
                'num_reviews': 84,
                'is_featured': True,
            },
            {
                'name': 'PulseFit Pro Ultra Smartwatch',
                'slug': 'pulsefit-pro-ultra-smartwatch',
                'category': cat_objs['wearables'],
                'description': 'Next-gen fitness & health tracker featuring continuous SpO2 monitor, dual-frequency GPS, AMOLED sapphire touch display, and 7-day battery life.',
                'price': Decimal('199.50'),
                'original_price': Decimal('249.00'),
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80',
                'stock': 18,
                'rating': Decimal('4.8'),
                'num_reviews': 62,
                'is_featured': True,
            },
            {
                'name': 'Zenith 16-inch M3 Max Laptop',
                'slug': 'zenith-16-inch-m3-max-laptop',
                'category': cat_objs['computers-laptops'],
                'description': 'Unrivaled workstation performance featuring 16-core CPU, 40-core GPU, 32GB Unified RAM, 1TB NVMe SSD, and Liquid Retina XDR display.',
                'price': Decimal('1899.00'),
                'original_price': Decimal('2099.00'),
                'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80',
                'stock': 8,
                'rating': Decimal('5.0'),
                'num_reviews': 41,
                'is_featured': True,
            },
            {
                'name': 'AeroCharge 4-in-1 Magnetic Dock',
                'slug': 'aerocharge-4-in-1-magnetic-dock',
                'category': cat_objs['smart-accessories'],
                'description': 'Fast 15W wireless charging station for smartphone, smartwatch, wireless earbuds, and ambient nightstand LED light.',
                'price': Decimal('69.99'),
                'original_price': Decimal('89.99'),
                'image_url': 'https://images.unsplash.com/photo-1586953208448-b95a79798f07?auto=format&fit=crop&w=800&q=80',
                'stock': 40,
                'rating': Decimal('4.7'),
                'num_reviews': 29,
                'is_featured': True,
            },
            {
                'name': 'SonicBoom Mini Bluetooth Speaker',
                'slug': 'sonicboom-mini-bluetooth-speaker',
                'category': cat_objs['audio-sound'],
                'description': 'IPX7 waterproof portable speaker with deep bass radiator, 360-degree sound dispersion, and 18-hour continuous battery life.',
                'price': Decimal('79.99'),
                'original_price': Decimal('99.99'),
                'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=800&q=80',
                'stock': 30,
                'rating': Decimal('4.6'),
                'num_reviews': 53,
                'is_featured': False,
            },
            {
                'name': 'CyberGlass AR Smart Eyewear',
                'slug': 'cyberglass-ar-smart-eyewear',
                'category': cat_objs['wearables'],
                'description': 'Ultra-lightweight Augmented Reality glasses with Micro-OLED dual displays, directional spatial speakers, and voice assistant support.',
                'price': Decimal('349.00'),
                'original_price': Decimal('399.00'),
                'image_url': 'https://images.unsplash.com/photo-1572635196237-14b3f281503f?auto=format&fit=crop&w=800&q=80',
                'stock': 12,
                'rating': Decimal('4.8'),
                'num_reviews': 19,
                'is_featured': False,
            },
            {
                'name': 'UltraMechanical RGB Wireless Keyboard',
                'slug': 'ultramechanical-rgb-wireless-keyboard',
                'category': cat_objs['smart-accessories'],
                'description': 'Compact 75% hot-swappable mechanical keyboard with lubricated tactile switches, per-key RGB backlight, and tri-mode connectivity (2.4G/BT5.0/USB-C).',
                'price': Decimal('129.99'),
                'original_price': Decimal('159.99'),
                'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80',
                'stock': 22,
                'rating': Decimal('4.9'),
                'num_reviews': 77,
                'is_featured': False,
            },
            {
                'name': 'Precision Track RGB Ergonomic Mouse',
                'slug': 'precision-track-rgb-ergonomic-mouse',
                'category': cat_objs['smart-accessories'],
                'description': 'High-precision 26,000 DPI optical sensor, ultra-lightweight 58g honeycomb shell, and lag-free 1000Hz polling rate.',
                'price': Decimal('59.99'),
                'original_price': Decimal('74.99'),
                'image_url': 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=800&q=80',
                'stock': 35,
                'rating': Decimal('4.7'),
                'num_reviews': 38,
                'is_featured': False,
            },
        ]

        for prod_info in products_data:
            Product.objects.update_or_create(
                slug=prod_info['slug'],
                defaults=prod_info
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(products_data)} products across {len(categories_data)} categories!'))
