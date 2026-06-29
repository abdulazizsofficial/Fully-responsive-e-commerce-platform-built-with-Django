from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="eapp/auth_form.html", extra_context={"title": "Login", "button": "Login"}), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:item_id>/", views.remove_cart, name="remove_cart"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist/toggle/<int:product_id>/", views.toggle_wishlist, name="toggle_wishlist"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_history, name="order_history"),
    path("profile/", views.profile, name="profile"),
    path("profile/address/<int:address_id>/delete/", views.delete_address, name="delete_address"),
    path("seller/", views.dashboard, name="dashboard"),
    path("seller/products/", views.manage_products, name="manage_products"),
    path("seller/products/add/", views.product_form, name="add_product"),
    path("seller/products/<int:product_id>/edit/", views.product_form, name="edit_product"),
    path("seller/products/<int:product_id>/delete/", views.delete_product, name="delete_product"),
    path("seller/categories/", views.manage_categories, name="manage_categories"),
    path("seller/brands/", views.manage_brands, name="manage_brands"),
    path("seller/orders/", views.manage_orders, name="manage_orders"),
    path("seller/orders/<int:order_id>/status/", views.update_order_status, name="update_order_status"),
]
