from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', main_page, name='books_main'),
    path('<int:id>/', book_by_id, name='book_by_id'),
    path('<int:id>/update/', book_update, name='book_update'),
    path('create/', book_create, name='book_create'),
    path('<int:id>/delete/', book_delete, name='book_delete'),
]
