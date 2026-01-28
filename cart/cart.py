from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:
    """
    Класс для управления корзиной покупок.
    Использует сессии Django для хранения данных.
    """

    def __init__(self, request):
        """Инициализация корзины"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        # Если корзины нет в сессии - создаем пустую
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Добавить товар в корзину или обновить количество"""
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)  # Храним как строку
            }

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """Сохранить изменения в сессии"""
        self.session.modified = True

    def remove(self, product):
        """Удалить товар из корзины"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Итератор по товарам в корзине"""
        product_ids = self.cart.keys()
        # Получаем объекты товаров из базы
        products = Product.objects.filter(id__in=product_ids)

        # Создаем копию корзины для безопасной модификации
        cart = self.cart.copy()

        # Добавляем объекты товаров в корзину
        for product in products:
            cart[str(product.id)]['product'] = product

        # Проходим по товарам и рассчитываем суммы
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Общее количество товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Общая стоимость корзины"""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        """Очистить корзину"""
        del self.session[settings.CART_SESSION_ID]
        self.save()