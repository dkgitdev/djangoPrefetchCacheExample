from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app1.models import Book, Author

CACHE_PREFETCH_KEY = 'book_with_prefetches'
CACHE_NO_PREFETCH_KEY = 'book_with_no_prefetches'


# Create your views here.
def book_author_view_initial_prefetch(request):
    b = cache.get(CACHE_PREFETCH_KEY)
    if b is None:
        b = Book.objects.prefetch_related('author').first()

        cache.set(CACHE_PREFETCH_KEY, b, 1800)

    return HttpResponse(f'book Author is: {b.author.name}')


def book_author_view(request):
    b = cache.get(CACHE_NO_PREFETCH_KEY)
    if b is None:
        b = Book.objects.first()

        cache.set(CACHE_NO_PREFETCH_KEY, b, 1800)

    return HttpResponse(f'book Author is: {b.author.name}')


@csrf_exempt
def change_author_name(request):
    if request.method.upper() != "POST":
        return HttpResponse("send post-request", status=405)
    a = Author.objects.first()
    prev_name = a.name
    a.name = request.POST["name"]
    a.save()
    return HttpResponse(f"book author's name changed: {prev_name} -> {a.name}")