from .cart import Cart

def cart(request):
    """Добавляет корзину во все шаблоны"""
    return {'cart': Cart(request)}