# 🛒 AzizeMart ecommerce project using Django

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

> AzizeMart is a fully-featured Django e-commerce web application designed for a modern clothing store. It provides a seamless experience for both customers and store administrators.

---

## 📑 Table of Contents
* [Features](#-features)
* [Tech Stack](#-tech-stack)
* [Project Structure](#-project-structure)
* [Quick Start](#-quick-start)
* [Application Structure (URLs)](#-application-structure-urls)
* [Staff & Admin Access](#-staff--admin-access)
* [Database Configuration](#-database-configuration)
* [Development Notes](#-development-notes)

---

## ✨ Features

**For Customers:**
* 🛍️ **Responsive Storefront:** Optimized for both desktop and mobile browsing.
* 🔍 **Advanced Catalog:** Search, filter, and sort products by categories, brands, sizes, and colors.
* ❤️ **User Features:** Full account management, wishlist, and cart systems.
* 💳 **Checkout System:** Save delivery addresses and place orders via Cash on Delivery (COD).
* 📊 **Personal Dashboard:** View profile details, saved addresses, wishlist counts, and order history.

**For Store Management (Staff):**
* 📈 **Seller Dashboard:** View sales metrics, order pipelines, inventory alerts, and top-performing products.
* 📦 **Product Management:** Full CRUD capabilities for products, categories, and brands.
* 🚚 **Order Fulfillment:** Manage customer orders and update tracking statuses.
* 🌱 **Demo Data:** Built-in starter command to populate the store with demo products instantly.

---

## 🛠 Tech Stack

* **Backend:** Python, Django 6.0.6
* **Database:** SQLite (Development) / PostgreSQL ready
* **Frontend:** Bootstrap 5, Custom CSS/JS
* **Media Handling:** Pillow (Image processing)

---

## 📂 Project Structure

```text
AzizeMart/
├── manage.py
├── requirements.txt
├── AzizeMart/              # Core Django Settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── eapp/                   # Main E-commerce App
    ├── models.py
    ├── views.py
    ├── forms.py
    ├── urls.py
    ├── templates/eapp/
    ├── static/eapp/
    └── management/commands/seed_store.py


## Setup

From the repository folder:

```powershell
cd AzizeMart
python -m venv ..\env
..\env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_store
python manage.py createsuperuser
python manage.py runserver
```

Open the site:

```text
http://127.0.0.1:8000/
```

## Useful URLs

```text
/                         Home
/products/                Product catalog
/cart/                    Shopping cart
/checkout/                Checkout
/profile/                 Customer account
/orders/                  Customer order history
/wishlist/                Wishlist
/seller/                  Seller dashboard, staff only
/seller/products/         Manage products
/seller/categories/       Manage categories and product types
/seller/brands/           Manage brands
/seller/orders/           Manage orders
/admin/                   Django admin
```

## Staff Access

The seller dashboard is protected by Django staff permissions. To access it:

1. Create a superuser with `python manage.py createsuperuser`.
2. Log in through `/login/` or `/admin/`.
3. Visit `/seller/`.

Only users with `is_staff=True` can access seller pages.

## Database

By default, the app uses SQLite for local development. The settings also support PostgreSQL when these environment variables are provided:

```text
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT
```

If `POSTGRES_DB` is not set, Django falls back to SQLite.

## Demo Data

Run this command to create starter categories, product types, brands, sizes, colors, and sample products:

```powershell
python manage.py seed_store
```

## Media And Static Files

- Static files are stored in `eapp/static/eapp/`.
- Templates are stored in `eapp/templates/eapp/`.
- Uploaded product images use Django's media settings and are stored under `media/` in development.

## Development Checks

Run Django's system check:

```powershell
python manage.py check
```

Apply migrations after model changes:

```powershell
python manage.py makemigrations
python manage.py migrate
```

## Notes

This project is currently configured for development with `DEBUG=True`. Before deploying, update the secret key, allowed hosts, static/media handling, database credentials, and security settings.
