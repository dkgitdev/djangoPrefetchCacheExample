Django Prefetch Cache Pitfall

Setup
=====

Make a python 3.6+ venv (I used 3.8).

```shell
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Test case:
=========

When you freeze some django entity with prefetches to the cache and then un-freeze it, 
the prefetches contain old data.

Example
=======
This is a simple app. It has one book and one author after the data migration passes.

First, query the current book views:

```shell
curl -X GET --location "http://127.0.0.1:8000/book_author_view/"
curl -X GET --location "http://127.0.0.1:8000/book_author_view_initial_prefetch/"
```

They both should return `book Author is: some name` and cache resulting `book` entity. 
But the first will save a prefetched author instance as well.

Then, change author name:

```shell
curl -X POST --location "http://127.0.0.1:8000/change_author_name/" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "name=newName"
```

Now the author's name is `newName`, but only one of the endpoints will return it correctly:

```shell
curl -X GET --location "http://127.0.0.1:8000/book_author_view/"
```

This one returns nicely, but the other fails:

```shell
curl -X GET --location "http://127.0.0.1:8000/book_author_view_initial_prefetch/"
```
