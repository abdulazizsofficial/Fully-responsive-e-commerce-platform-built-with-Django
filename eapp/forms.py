from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Address, Brand, Category, Color, Order, Product, ProductType, Size


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=80, required=False)
    last_name = forms.CharField(max_length=80, required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "street", "city", "postal_code", "country", "is_default"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "product_type",
            "brand",
            "name",
            "description",
            "price",
            "offer_price",
            "purchase_cost",
            "stock",
            "sizes",
            "colors",
            "main_image",
            "image_url",
            "is_featured",
            "is_new_arrival",
            "popularity",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "sizes": forms.CheckboxSelectMultiple,
            "colors": forms.CheckboxSelectMultiple,
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "is_active"]


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name"]


class ProductTypeForm(forms.ModelForm):
    class Meta:
        model = ProductType
        fields = ["name"]


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ["name"]


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ["name", "hex_code"]


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
