from django.urls import path
from .import views
from .views import *


urlpatterns = [
    path('', authors_all, name='authors_all'),
    path('<int:id>/', author_by_id, name='author_by_id'),
    path('create/', author_create, name='author_create'),
    path('<int:id>/update/', author_update, name='author_update'),
    path('<int:id>/delete/', author_delete, name='author_delete'),
]
