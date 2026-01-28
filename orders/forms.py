from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    """Форма оформления заказа"""
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email',
                  'address', 'postal_code', 'city']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }