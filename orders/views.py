from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    """Оформление заказа из корзины"""
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            # Привязываем заказ к пользователю, если он авторизован
            if request.user.is_authenticated:
                order.user = request.user

            order.save()

            # Создаем позиции заказа
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Очищаем корзину
            cart.clear()

            return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 'orders/create.html', {'cart': cart, 'form': form})