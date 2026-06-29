from decimal import Decimal

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AddressForm,
    BrandForm,
    CategoryForm,
    OrderStatusForm,
    ProductForm,
    ProductTypeForm,
    ProfileForm,
    RegisterForm,
)
from .models import (
    Address,
    Brand,
    CartItem,
    Category,
    Color,
    Order,
    OrderItem,
    Product,
    ProductImage,
    ProductType,
    Size,
    Wishlist,
)


def catalog_context():
    return {
        "categories": Category.objects.filter(is_active=True),
        "types": ProductType.objects.all(),
        "brands": Brand.objects.all(),
        "sizes": Size.objects.all(),
        "colors": Color.objects.all(),
    }


def home(request):
    featured = Product.objects.filter(is_featured=True)[:3]
    popular = Product.objects.select_related("category", "brand").order_by("-popularity", "-created_at")[:8]
    arrivals = Product.objects.filter(is_new_arrival=True)[:8]
    return render(request, "eapp/home.html", {"featured": featured, "popular": popular, "arrivals": arrivals})


def product_list(request):
    products = Product.objects.select_related("category", "product_type", "brand").prefetch_related("sizes", "colors")
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    product_type = request.GET.get("type", "")
    brand = request.GET.get("brand", "")
    size = request.GET.get("size", "")
    color = request.GET.get("color", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")
    sort = request.GET.get("sort", "newest")

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(brand__name__icontains=query))
    if category:
        products = products.filter(category__slug=category)
    if product_type:
        products = products.filter(product_type__slug=product_type)
    if brand:
        products = products.filter(brand__slug=brand)
    if size:
        products = products.filter(sizes__name=size)
    if color:
        products = products.filter(colors__name=color)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    sort_map = {
        "price_low": "price",
        "price_high": "-price",
        "popular": "-popularity",
        "newest": "-created_at",
    }
    products = products.order_by(sort_map.get(sort, "-created_at")).distinct()
    paginator = Paginator(products, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = catalog_context()
    context.update({"page_obj": page_obj, "query": query, "selected": request.GET})
    return render(request, "eapp/product_list.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.prefetch_related("sizes", "colors", "gallery"), slug=slug)
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, "eapp/product_detail.html", {"product": product, "related": related})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to AzizeMart. Your account is ready.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "eapp/auth_form.html", {"form": form, "title": "Create account", "button": "Register"})


def forgot_password(request):
    form = PasswordResetForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        messages.success(request, "If that email exists, password reset instructions would be sent.")
        return redirect("login")
    return render(request, "eapp/auth_form.html", {"form": form, "title": "Forgot password", "button": "Send reset link"})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get("size", "")
    color = request.POST.get("color", "")
    quantity = int(request.POST.get("quantity", 1))
    item, created = CartItem.objects.get_or_create(user=request.user, product=product, size=size, color=color)
    item.quantity = quantity if created else item.quantity + quantity
    item.save()
    messages.success(request, f"{product.name} added to your cart.")
    return redirect(request.POST.get("next") or "cart")


@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user).select_related("product")
    subtotal = sum(item.line_total for item in items)
    shipping = Decimal("80.00") if subtotal else Decimal("0.00")
    return render(request, "eapp/cart.html", {"items": items, "subtotal": subtotal, "shipping": shipping, "total": subtotal + shipping})


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    quantity = int(request.POST.get("quantity", 1))
    if quantity <= 0:
        item.delete()
        messages.info(request, "Item removed from cart.")
    else:
        item.quantity = quantity
        item.save()
        messages.success(request, "Cart updated.")
    return redirect("cart")


@login_required
def remove_cart(request, item_id):
    get_object_or_404(CartItem, id=item_id, user=request.user).delete()
    messages.info(request, "Item removed from cart.")
    return redirect("cart")


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user).select_related("product")
    return render(request, "eapp/wishlist.html", {"items": items})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, "Added to wishlist.")
    else:
        item.delete()
        messages.info(request, "Removed from wishlist.")
    return redirect(request.POST.get("next") or product.get_absolute_url())


@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user).select_related("product")
    if not items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("product_list")

    address_id = request.POST.get("address") if request.method == "POST" else None
    addresses = Address.objects.filter(user=request.user)
    selected_address = addresses.filter(id=address_id).first() or addresses.filter(is_default=True).first() or addresses.first()
    form = AddressForm(request.POST or None, instance=selected_address)

    subtotal = sum(item.line_total for item in items)
    shipping = Decimal("80.00")

    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            if address.is_default:
                Address.objects.filter(user=request.user).exclude(id=address.id).update(is_default=False)

            order = Order.objects.create(
                user=request.user,
                address=address,
                full_name=address.full_name,
                phone=address.phone,
                street=address.street,
                city=address.city,
                postal_code=address.postal_code,
                country=address.country,
                subtotal=subtotal,
                shipping_cost=shipping,
                total=subtotal + shipping,
                purchase_cost_total=sum(item.product.purchase_cost * item.quantity for item in items),
            )
            for item in items:
                product = item.product
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    price=product.selling_price,
                    purchase_cost=product.purchase_cost,
                    quantity=item.quantity,
                    size=item.size,
                    color=item.color,
                )
                product.stock = max(product.stock - item.quantity, 0)
                product.popularity += item.quantity
                product.save(update_fields=["stock", "popularity", "updated_at"])
            items.delete()
        messages.success(request, f"Order #{order.id} placed successfully. Pay cash on delivery.")
        return redirect("order_history")

    return render(request, "eapp/checkout.html", {"items": items, "form": form, "addresses": addresses, "subtotal": subtotal, "shipping": shipping, "total": subtotal + shipping})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "eapp/order_history.html", {"orders": orders})


@login_required
def profile(request):
    profile_form = ProfileForm(request.POST or None, instance=request.user, prefix="profile")
    address_form = AddressForm(request.POST or None, prefix="address")
    if request.method == "POST":
        if "save_profile" in request.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile")
        if "save_address" in request.POST and address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()
            if address.is_default:
                Address.objects.filter(user=request.user).exclude(id=address.id).update(is_default=False)
            messages.success(request, "Address saved.")
            return redirect("profile")
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    addresses = request.user.addresses.all()
    context = {
        "profile_form": profile_form,
        "address_form": address_form,
        "addresses": addresses,
        "recent_orders": orders[:3],
        "order_count": orders.count(),
        "address_count": addresses.count(),
        "wishlist_count": Wishlist.objects.filter(user=request.user).count(),
        "default_address": addresses.filter(is_default=True).first(),
    }
    return render(request, "eapp/profile.html", context)


@login_required
def delete_address(request, address_id):
    get_object_or_404(Address, id=address_id, user=request.user).delete()
    messages.info(request, "Address deleted.")
    return redirect("profile")


@staff_member_required
def dashboard(request):
    valid_orders = Order.objects.exclude(status="Cancelled")
    total_sales = valid_orders.aggregate(total=Sum("total"))["total"] or Decimal("0.00")
    purchase_cost = valid_orders.aggregate(total=Sum("purchase_cost_total"))["total"] or Decimal("0.00")
    total_orders = Order.objects.count()
    delivered_orders = Order.objects.filter(status="Delivered").count()
    pending_orders = Order.objects.filter(status="Pending").count()
    active_products = Product.objects.filter(stock__gt=0).count()
    out_of_stock = Product.objects.filter(stock=0).count()
    revenue = total_sales - purchase_cost
    avg_order_value = total_sales / delivered_orders if delivered_orders else Decimal("0.00")
    fulfillment_rate = round((delivered_orders / total_orders) * 100) if total_orders else 0
    profit_margin = round((revenue / total_sales) * 100) if total_sales else 0
    status_counts = {
        item["status"]: item["count"]
        for item in Order.objects.values("status").annotate(count=Count("id"))
    }
    context = {
        "total_products": Product.objects.count(),
        "active_products": active_products,
        "out_of_stock": out_of_stock,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
        "total_sales": total_sales,
        "total_purchase_cost": purchase_cost,
        "revenue": revenue,
        "avg_order_value": avg_order_value,
        "fulfillment_rate": fulfillment_rate,
        "profit_margin": profit_margin,
        "status_counts": status_counts,
        "low_stock": Product.objects.filter(stock__lte=5).order_by("stock", "name")[:8],
        "recent_orders": Order.objects.select_related("user")[:8],
        "top_products": (
            OrderItem.objects.values("product_name")
            .annotate(
                units=Sum("quantity"),
                sales=Sum(ExpressionWrapper(F("price") * F("quantity"), output_field=DecimalField())),
            )
            .order_by("-units")[:5]
        ),
    }
    return render(request, "eapp/dashboard.html", context)


@staff_member_required
def manage_products(request):
    products = Product.objects.select_related("category", "brand").all()
    return render(request, "eapp/manage_products.html", {"products": products})


@staff_member_required
def product_form(request, product_id=None):
    product = get_object_or_404(Product, id=product_id) if product_id else None
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST" and form.is_valid():
        product = form.save()
        for image in request.FILES.getlist("gallery_images"):
            ProductImage.objects.create(product=product, image=image)
        messages.success(request, "Product saved.")
        return redirect("manage_products")
    return render(request, "eapp/product_form.html", {"form": form, "product": product})


@staff_member_required
def delete_product(request, product_id):
    get_object_or_404(Product, id=product_id).delete()
    messages.info(request, "Product deleted.")
    return redirect("manage_products")


@staff_member_required
def manage_categories(request):
    category_form = CategoryForm(request.POST or None, prefix="category")
    type_form = ProductTypeForm(request.POST or None, prefix="type")
    if request.method == "POST":
        if "save_category" in request.POST and category_form.is_valid():
            category_form.save()
            messages.success(request, "Category saved.")
            return redirect("manage_categories")
        if "save_type" in request.POST and type_form.is_valid():
            type_form.save()
            messages.success(request, "Product type saved.")
            return redirect("manage_categories")
    return render(request, "eapp/manage_categories.html", {"category_form": category_form, "type_form": type_form, "categories": Category.objects.all(), "types": ProductType.objects.all()})


@staff_member_required
def manage_brands(request):
    form = BrandForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Brand saved.")
        return redirect("manage_brands")
    return render(request, "eapp/manage_brands.html", {"form": form, "brands": Brand.objects.all()})


@staff_member_required
def manage_orders(request):
    orders = Order.objects.select_related("user").prefetch_related("items")
    return render(request, "eapp/manage_orders.html", {"orders": orders})


@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = OrderStatusForm(request.POST or None, instance=order)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Order status updated.")
    return redirect("manage_orders")
