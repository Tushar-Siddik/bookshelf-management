from .models import Book, Bookshelf, BookshelfToBook
from django.http import HttpResponse
from django.shortcuts import render, redirect



from .forms import NewBookForm
from django.views import generic

# class BookListView(generic.ListView):
#     model = Book

    
def insertBookToBookshelf(bookId, bookshelfId):
    existing = BookshelfToBook.objects.filter(fk_books=bookId, fk_bookshelves=bookshelfId)
    if existing.count() > 0:
        print('attempted duplicate insert')
        return
    book = Book.objects.get(id=bookId)
    bookshelf = Bookshelf.objects.get(id=bookshelfId)
    if book != None and bookshelf != None:
        newEntry = BookshelfToBook(fk_books=book, fk_bookshelves=bookshelf)
        newEntry.save()


def booksInBookshelf(request, bookshelfId):
    bookshelfName = Bookshelf.objects.get(id=bookshelfId).bookshelf
    idList = BookshelfToBook.objects.filter(fk_bookshelves=bookshelfId).values_list('fk_books', flat=True) 
    books = Book.objects.filter(id__in=idList)

    context = {
        'books': books,
        'total': len(books),
        'bookshelf': bookshelfName,
        'bookshelfId': bookshelfId
    }

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = (request.POST)
        # print(form)
        # check whether it's valid:
        if form.get('bookid') != None:
            insertBookToBookshelf(form.get('bookid'), bookshelfId)
            # redirect to a new URL:
            return redirect(request.META['HTTP_REFERER'])

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewBookForm()
        context['form'] = form
    
    return render(request, 'bookshelf.html', context=context)


def bookshelfList(request):
    bookshelves = Bookshelf.objects.all()

    context = {
        'bookshelves': bookshelves,
        'total': len(bookshelves),
    }


    return render(request, 'bookshelfList.html', context=context)


def get_name(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = (request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return 

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewBookForm()

    return render(request, 'name.html', {'form': form})
