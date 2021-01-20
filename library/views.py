from django.shortcuts import redirect, render, HttpResponse


def main_page(request):
    return redirect('books_main', permanent=True)


def about_page(request):
    # return HttpResponse('OK')
    return render(request, 'about_page.html')
