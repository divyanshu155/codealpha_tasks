# CyberStore - Full-Stack E-Commerce Web Application

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![Frontend](https://img.shields.io/badge/Frontend-HTML5%20%7C%20CSS3%20%7C%20JS-E34F26)
![Database](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)

CyberStore is a feature-rich, high-performance **Full-Stack E-Commerce Platform** built using **Django** on the backend and **HTML5, Vanilla CSS, and JavaScript** on the frontend. The project delivers a futuristic obsidian dark theme with glassmorphism UI, real-time AJAX shopping cart interactions, multi-step checkout processing, order receipts, and customer order tracking.

---

## 🚀 Features & Highlights

### 🛍️ Product Catalog & Discovery
- **Dynamic Product Grid**: Displays tech products with discount badges, star ratings, price tags, and quick-view detail links.
- **Search & Filter System**: Instant keyword search, category filtering (Audio & Sound, Wearables, Computers & Laptops, Smart Accessories), and sorting (Price Low to High, Price High to Low, Highest Rated, Newest).
- **Product Detail View**: Dedicated detail view with high-res gallery images, stock status indicators, specifications breakdown, and related product recommendations.

### 🛒 Interactive Shopping Cart
- **AJAX Add-to-Cart**: Seamless item additions without full page reloads.
- **Dynamic Badge Counter**: Live navigation cart item counter with pulse animations.
- **Cart Summary Page**: Full item list, quantity controls (+/-), item removal, subtotal, estimated 8% tax, and shipping status (Free shipping on orders $50+).

### 💳 Order Processing & Checkout
- **Multi-Step Checkout**: Customer shipping address input, payment provider selector (Credit Card, PayPal, Apple Pay), and order item review.
- **Automated Inventory Tracking**: Order placement automatically updates database stock levels and generates a unique order identifier (`ORD-XXXXXXXX`).
- **Order Success Receipt**: Confirmation view displaying shipping details, itemized cost breakdown, and a printable order receipt.

### 🔐 User Authentication & Customer Dashboard
- **Django Auth System**: User Registration, Login, and Logout functionality.
- **Order History Dashboard**: Authenticated user page displaying past orders, order status badges (Processing/Completed/Pending), and date timestamps.
- **Django Admin Panel**: Customized admin management for categories, products, orders, and order items.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.13, Django 6.0
- **Database**: SQLite3
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism, Flexbox/Grid, Animations), JavaScript (Fetch API, DOM Manipulation)
- **Icons**: Bootstrap Icons (CDN)

---

## 📦 Project Structure

```text
fullstack-website/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── ecommerce_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── store/
    ├── models.py          # Category, Product, Order, OrderItem models
    ├── views.py           # Catalog, Detail, Cart, Checkout, Auth & Order views
    ├── urls.py            # App URL routing
    ├── forms.py           # Registration, Login, and Checkout forms
    ├── admin.py           # Customized Django Admin site registrations
    ├── context_processors.py # Global session cart context calculation
    ├── static/
    │   ├── css/style.css  # Dark mode glassmorphism styles & animations
    │   └── js/main.js     # Client-side AJAX cart & toast notifications
    ├── templates/
    │   ├── base.html      # Layout wrapper with sticky navbar & footer
    │   └── store/         # Views templates (list, detail, cart, checkout, etc.)
    └── management/
        └── commands/
            └── seed_db.py # Automated database seeder script
```

---

## ⚡ Quick Start & Installation

### 1. Clone Repository & Navigate to Directory
```bash
git clone https://github.com/divyanshu155/codealpha_tasks.git
cd codealpha_tasks/fullstack-website
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Database Migrations & Seed Sample Data
```bash
python manage.py migrate
python manage.py seed_db
```

### 4. Start Local Development Server
```bash
python manage.py runserver 8000
```

Open your browser and navigate to: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🔑 Demo Admin Credentials

The database seeder automatically initializes a superuser for testing the Django Admin panel:

- **Admin URL**: `http://127.0.0.1:8000/admin/`
- **Username**: `admin`
- **Password**: `admin123`

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
