from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Book, Category
from .forms import BookForm


def index(request):
    books = Book.objects.select_related('author', 'category').order_by('-created_at')[:6]
    return render(request, 'library/index.html', {'books': books})


def catalog(request):
    books = Book.objects.select_related('author', 'category')
    categories = Category.objects.all()

    q = request.GET.get('q', '').strip()
    active_category = request.GET.get('category', '')

    if q:
        books = books.filter(title__icontains=q) | books.filter(author__name__icontains=q)

    if active_category:
        books = books.filter(category__slug=active_category)

    books = books.distinct()

    return render(request, 'library/catalog.html', {
        'books': books,
        'categories': categories,
        'q': q,
        'active_category': active_category,
    })


def book_detail(request, pk):
    book = get_object_or_404(Book.objects.select_related('author', 'category'), pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'"{book.title}" has been added.')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form})


def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{book.title}" has been updated.')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form, 'book': book})


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'"{title}" has been deleted.')
        return redirect('catalog')
    return render(request, 'library/book_confirm_delete.html', {'book': book})


def handler404(request, exception):
    return render(request, '404.html', status=404)


# ── API ──────────────────────────────────────────────────────────

def api_books(request):
    books = Book.objects.select_related('author', 'category')

    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    if q:
        books = books.filter(title__icontains=q) | books.filter(author__name__icontains=q)
        books = books.distinct()

    if category:
        books = books.filter(category__slug=category)

    data = [
        {
            'id':        b.id,
            'title':     b.title,
            'author':    b.author.name,
            'category':  b.category.name if b.category else None,
            'year':      b.year,
            'available': b.available,
        }
        for b in books
    ]
    return JsonResponse(data, safe=False)


def api_book_detail(request, pk):
    try:
        book = Book.objects.select_related('author', 'category').get(pk=pk)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    data = {
        'id':          book.id,
        'title':       book.title,
        'author':      book.author.name,
        'category':    book.category.name if book.category else None,
        'description': book.description,
        'year':        book.year,
        'available':   book.available,
        'cover_url':   book.cover.url if book.cover else None,
    }
    return JsonResponse(data)
