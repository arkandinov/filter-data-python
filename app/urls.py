from django.urls import path
from .views import transaksi_view

urlpatterns = [
    path('', transaksi_view, name='transaksi'),
]
