from django.urls import path
from .views import *

urlpatterns = [
    path('all/', users_all, name='users_all'),
    path('my/', my_user, name='my_user'),
    path('update/', user_update, name='user_update'),
    path('change-password/', change_password, name='change_password'),
    path('delete/', user_delete, name='user_delete'),
    path('<int:id>/', user_by_id, name='user_by_id'),
    path('<int:id>/update', su_user_update, name='su_user_update'),
    path('<int:id>/delete', su_user_delete, name='su_user_delete'),
    path('create/', su_user_create, name='su_user_create'),
    path('registration/', custom_registration, name='custom_registration'),
    path('login/', custom_login, name='custom_login'),
    path('logout/', custom_logout, name='custom_logout'),
]



