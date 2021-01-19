from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('books_main')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def user_is_staff(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.role:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('books_main')
    return wrapper_func


def if_user_auth(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('custom_login')
    return wrapper_func
