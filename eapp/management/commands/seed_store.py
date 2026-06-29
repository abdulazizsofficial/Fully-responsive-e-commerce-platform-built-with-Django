from django.core.management.base import BaseCommand

from eapp.models import Brand, Category, Color, Product, ProductType, Size


class Command(BaseCommand):
    help = "Create starter data for the AzizeMart clothing store."

    def handle(self, *args, **options):
        men, _ = Category.objects.get_or_create(name="Men")
        women, _ = Category.objects.get_or_create(name="Women")

        types = {}
        for name in ["T-Shirts", "Shirts", "Jeans", "Pants", "Shoes", "Hoodies", "Dresses", "Jackets"]:
            types[name], _ = ProductType.objects.get_or_create(name=name)

        brands = {}
        for name in ["Azize Basics", "Urban Thread", "North Loom", "SoftStreet"]:
            brands[name], _ = Brand.objects.get_or_create(name=name)

        for name in ["S", "M", "L", "XL", "XXL", "38", "40", "42"]:
            Size.objects.get_or_create(name=name)

        for name, code in [("Black", "#111827"), ("White", "#ffffff"), ("Navy", "#1e3a8a"), ("Olive", "#4d7c0f"), ("Beige", "#d6c5a5"), ("Red", "#dc2626")]:
            Color.objects.get_or_create(name=name, defaults={"hex_code": code})

        samples = [
            ("Classic Oxford Shirt", men, "Shirts", "Urban Thread", 1650, 1180, 760, 24, "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=900&q=80"),
            ("Relaxed Cotton Hoodie", men, "Hoodies", "North Loom", 2450, 1990, 1100, 14, "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=900&q=80"),
            ("Slim Stretch Jeans", men, "Jeans", "Azize Basics", 2200, 1850, 980, 19, "https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&w=900&q=80"),
            ("Minimal White Sneakers", men, "Shoes", "SoftStreet", 3200, 2790, 1700, 9, "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=900&q=80"),
            ("Ribbed Knit Top", women, "T-Shirts", "Azize Basics", 1350, 990, 520, 28, "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?auto=format&fit=crop&w=900&q=80"),
            ("High Rise Blue Jeans", women, "Jeans", "Urban Thread", 2350, 1950, 1050, 16, "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=900&q=80"),
            ("Summer Midi Dress", women, "Dresses", "North Loom", 2800, 2290, 1250, 11, "https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=900&q=80"),
            ("Everyday Denim Jacket", women, "Jackets", "SoftStreet", 3400, 2990, 1800, 6, "https://images.unsplash.com/photo-1543076447-215ad9ba6923?auto=format&fit=crop&w=900&q=80"),
        ]

        all_sizes = Size.objects.all()
        all_colors = Color.objects.all()
        for index, (name, category, type_name, brand_name, price, offer, cost, stock, image_url) in enumerate(samples):
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "product_type": types[type_name],
                    "brand": brands[brand_name],
                    "description": f"{name} made for comfortable everyday clothing with a clean AzizeMart fit.",
                    "price": price,
                    "offer_price": offer,
                    "purchase_cost": cost,
                    "stock": stock,
                    "image_url": image_url,
                    "is_featured": index < 3,
                    "is_new_arrival": index >= 4,
                    "popularity": 20 - index,
                },
            )
            if created:
                product.sizes.set(all_sizes[:5])
                product.colors.set(all_colors[:4])

        self.stdout.write(self.style.SUCCESS("AzizeMart starter data created."))
