from django.urls import path, include
from products import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]