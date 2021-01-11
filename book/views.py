from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Book
from .forms import BookForm


def book_exist(id):
    try:
        get_object_or_404(Book, id=id)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')
        # return redirect('books_main')


def main_page(request):
    books = Book.get_all()
    # books_by_three = [books[x: x + 3] for x in range(0, len(books), 3)]  # test feature
    return render(request, 'books_.html', context={'books': books})


def book_by_id(request, id):
    book_exist(id)

    book = Book.get_by_id(book_id=id)
    authors = ', '.join([author.patronymic for author in book.authors.all()])  # add authors like string
    return render(request, 'book_by_id_.html', context={'book': book, 'authors': authors})


def book_create(request):
    book_form = BookForm()
    if request.method == 'POST':
        book_form = BookForm(request.POST, request.FILES)
        if book_form.is_valid():  # check if form is valid
            book = Book.create(**book_form.cleaned_data)  # Use create method add clean data
            return redirect(book)
    return render(request, 'book_create_.html', context={'form': book_form})


def book_update(request, id):
    book = Book.get_by_id(book_id=id)
    book_form = BookForm(instance=book)
    if request.method == 'POST':
        book_form = BookForm(request.POST, request.FILES, instance=book)
        if book_form.is_valid():
            book = book.update(**book_form.cleaned_data)
            return redirect('book_by_id', id)
    return render(request, 'book_update_.html', context={'form': book_form})


def book_delete(request, id):
    book_exist(id)

    Book.delete_by_id(book_id=id)
    return redirect('books_main')

    pass