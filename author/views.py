from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Author
from .forms import AuthorForm


def author_exist(id):
    try:
        get_object_or_404(Author, id=id)
    except Author.DoesNotExist:
        raise Http404('Author does not exist')
        # return redirect('authors_all')


def authors_all(request):
    authors = Author.get_all()
    return render(request, 'authors_all_.html', context={'authors': authors})


def author_by_id(request, id):
    author_exist(id)  # validation

    author = Author.get_by_id(author_id=id)
    books = list(author.books.all())
    numbers_of_books = len(books)
    books_three = books[:3]
    return render(request, 'author_by_id_.html', context={'author': author,
                                                         'books': books_three,
                                                         'number_of_books': numbers_of_books})


def author_create(request):
    author_form = AuthorForm()
    if request.method == 'POST':
        author_form = AuthorForm(request.POST, request.FILES)
        if author_form.is_valid():  # check if form is valid
            author = Author.create(**author_form.cleaned_data)  # Use create method add clean data
            return redirect(author)
    return render(request, 'author_create_.html', context={'form': author_form})


def author_update(request, id):
    author_exist(id)  # validation

    author = Author.get_by_id(author_id=id)
    author_form = AuthorForm(instance=author)
    if request.method == 'POST':
        author_form = AuthorForm(request.POST, request.FILES, instance=author)
        if author_form.is_valid():
            author.update(**author_form.cleaned_data)
            return redirect('author_by_id', id)
    return render(request, 'author_update_.html', context={'form': author_form})


def author_delete(request, id):
    author_exist(id)  # validation

    Author.delete_by_id(author_id=id)
    return redirect('authors_all')
