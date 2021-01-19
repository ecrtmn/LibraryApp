from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, logout, authenticate
from .decorators import unauthenticated_user, user_is_staff, if_user_auth

from .models import CustomUser
from book.models import Book
from .forms import UserForm, UserUpdate, UserPasswordChange


@unauthenticated_user
def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('books_main')
        else:
            messages.info(request, "Email or password is incorrect")

    return render(request, 'login_.html')


@unauthenticated_user
def custom_registration(request):
    user_form = UserForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = CustomUser.create(**user_form.cleaned_data)
            messages.success(request, f"Profile created for {user.email}!")
            return redirect('custom_login')

    return render(request, 'registration_.html', context={'form': user_form})


@if_user_auth
def custom_logout(request):
    logout(request)
    return redirect('custom_login')


@user_is_staff
def users_all(request):
    users = CustomUser.get_all()
    return render(request, 'users_all_.html', context={'users': users})


@if_user_auth
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


@if_user_auth
def my_user(request):
    user = request.user
    orders_query = list(user.order.values().order_by('-id'))[:5]
    orders = []
    for order in orders_query:
        book = Book.get_by_id(book_id=order['book_id'])
        new_dict = order
        new_dict['book_name'] = book.name  # make a new dict and add a book name to order dictionary
        orders.append(new_dict)
    return render(request, 'username.html', context={'user': user, 'orders': orders})


@if_user_auth
@user_is_staff
def user_by_id(request, id):
    user = CustomUser.get_by_id(user_id=id)
    orders_query = list(user.order.values().order_by('-id'))[:5]
    orders = []
    for order in orders_query:
        book = Book.get_by_id(book_id=order['book_id'])
        new_dict = order
        new_dict['book_name'] = book.name  # make a new dict and add a book name to order dictionary
        orders.append(new_dict)
    return render(request, 'username.html', context={'user': user, 'orders': orders})


@if_user_auth
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


@if_user_auth
def user_delete(request):
    user_queryset = CustomUser.objects.filter(email=request.user.email)
    user = list(user_queryset)[0]
    logout(request)
    user.delete_by_id(user_id=user.id)
    return redirect('custom_login')


@if_user_auth
@user_is_staff
def su_user_update(request, id):
    user = CustomUser.get_by_id(user_id=id)
    user_form = UserUpdate(instance=user)
    if request.method == 'POST':
        user_form = UserUpdate(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user.update(**user_form.cleaned_data)
            return redirect('user_by_id', user.id)
    return render(request, 'user_update_.html', context={'form': user_form})


@if_user_auth
@user_is_staff
def su_user_delete(request, id):
    CustomUser.delete_by_id(user_id=id)
    return redirect('books_main')


@if_user_auth
@user_is_staff
def su_user_create(request):
    user_form = UserForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = CustomUser.create(**user_form.cleaned_data)
            messages.success(request, f"Profile created for {user.email}!")
            return redirect('users_all')
    return render(request, 'registration_su.html', context={'form': user_form})
