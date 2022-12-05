from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=32)


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
