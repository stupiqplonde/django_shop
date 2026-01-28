from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart


@require_POST  # Разрешаем только POST-запросы
def cart_add(request, product_id):
    """Добавить товар в корзину"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # Получаем количество из формы
    quantity = int(request.POST.get('quantity', 1))

    cart.add(product=product, quantity=quantity)
    return redirect('cart_detail')


def cart_remove(request, product_id):
    """Удалить товар из корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    """Показать содержимое корзины"""
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})