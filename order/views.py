from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Order
from .forms import OrderForm, OrderUpdateForm, OrderOnClick
from book.models import Book
from datetime import datetime


def order_exist(id):
    try:
        get_object_or_404(Order, id=id)
    except Order.DoesNotExist:
        raise Http404('Order does not exist')


def orders_all(request):
    orders = Order.get_all()
    return render(request, 'orders_all_.html', context={'orders': orders})


def orders_not_returned(request):
    orders = Order.get_not_returned_books()
    return render(request, 'orders_all.html', context={'orders': orders})


def order_by_id(request, id):
    order_exist(id)

    order = Order.get_by_id(order_id=id)
    return render(request, 'order_by_id.html', context={'order': order})


def order_on_click(request, id):
    user = request.user
    book = Book.get_by_id(book_id=id)
    order_form = OrderOnClick()
    if request.method == 'POST':
        order_form = OrderOnClick(request.POST)
        print('HEY')
        if order_form.is_valid():
            print('VALID_HEY')
            temp_order = Order.create(user=user, book=book, planned_end_at=datetime.now())
            order = temp_order.update(**order_form.cleaned_data)
            return redirect('orders_all')
    return render(request, 'order_confirm_.html', context={'form': order_form, 'user': user, 'book': book})


def order_create(request):
    order_form = OrderForm()
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = Order.create(**order_form.cleaned_data)
            return redirect(order)
    return render(request, 'order_create.html', context={'form': order_form})


def order_update(request, id):
    order_exist(id)

    order = Order.get_by_id(order_id=id)
    order_form = OrderUpdateForm(instance=order)
    if request.method == 'POST':
        order_form = OrderUpdateForm(request.POST, instance=order)
        if order_form.is_valid():
            order = order.update(**order_form.cleaned_data)
            return redirect('order_by_id', id)
    return render(request, 'order_update_.html', context={'form': order_form})


def order_delete(request, id):
    order_exist(id)

    Order.delete_by_id(order_id=id)
    return redirect('orders_all')
