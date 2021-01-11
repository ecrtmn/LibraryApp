from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', orders_all, name='orders_all'),
    path('not-returned', orders_not_returned, name='orders_not_returned'),
    path('<int:id>', order_by_id, name='order_by_id'),
    path('create', order_create, name='order_create'),
    path('<int:id>/update', order_update, name='order_update'),
    path('<int:id>/delete', order_delete, name='order_delete'),
]