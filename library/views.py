from django.shortcuts import redirect, render


def main_page(request):
    return redirect('books_main', permanent=True)


def not_found(request):
    return render(request, '404.html')
