from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse

from .models import CustomUser
from book.models import Book
from .forms import UserForm, UserUpdate, UserPasswordChange


def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
        else:
            messages.info(request, "Email or password is incorrect")

    return render(request, 'login_.html')


def custom_registration(request):
    user_form = UserForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = CustomUser.create(**user_form.cleaned_data)
            messages.success(request, f"Profile created for {user.email}!")
            return redirect('custom_login')

    return render(request, 'registration_.html', context={'form': user_form})


def custom_logout(request):
    logout(request)
    return redirect('custom_login')


def users_all(request):
    users = CustomUser.get_all()
    return render(request, 'users_all_.html', context={'users': users})


def user_by_email(request, email):
    pass


def user_update(request):
    user_queryset = CustomUser.objects.filter(email=request.user.email)
    user = list(user_queryset)[0]
    user_form = UserUpdate(instance=user)

    if request.method == 'POST':
        user_form = UserUpdate(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user.update(**user_form.cleaned_data)
            return redirect('my_user')
    return render(request, 'user_update_.html', context={'form': user_form})


def my_user(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    if user:
        orders_query = list(user.order.values())
        orders = []
        for order in orders_query:
            book = Book.get_by_id(book_id=order['book_id'])
            new_dict = order
            new_dict['book_name'] = book.name  # make a new dict and add a book name to order dictionary
            orders.append(new_dict)
    return render(request, 'username.html', context={'user': user, 'orders': orders})


def user_by_id(request, id):
    user = CustomUser.get_by_id(user_id=id)
    orders_query = list(user.order.values())
    orders = []
    for order in orders_query:
        book = Book.get_by_id(book_id=order['book_id'])
        new_dict = order
        new_dict['book_name'] = book.name  # make a new dict and add a book name to order dictionary
        orders.append(new_dict)
    return render(request, 'user_by_id.html', context={'user': user, 'orders': orders})


def change_password(request):
    pass_form = UserPasswordChange(request.user)
    if request.method == 'POST':
        pass_form = UserPasswordChange(request.user, request.POST)
        if pass_form.is_valid():
            user = pass_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password successfully updated!')
            return redirect('my_user')
        else:
            messages.error(request, 'Password didnt change. Please fix errors.')
    return render(request, 'user_password_change.html', context={'form': pass_form})


def user_delete(request):
    user_queryset = CustomUser.objects.filter(email=request.user.email)
    user = list(user_queryset)[0]
    logout(request)
    user.delete_by_id(user_id=user.id)
    return redirect('custom_login')
