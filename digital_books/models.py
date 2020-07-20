from django.db import models
from custom_user.models import CustomUser
from django.core.exceptions import ValidationError
"""
Books

Title : charfield
limit: 3
URL : URL link field
Description : text
author: Charfield
Who has it on hold: one to many
Who has it checked out -one to many field

"""


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    limit = models.IntegerField(default=3)
    checked_out = models.ManyToManyField(
        CustomUser, related_name='checked_out')
    holds = models.ManyToManyField(
        CustomUser, related_name='holds', blank=True, through='HoldOrder')
    URL = models.URLField(max_length=200)
    language = models.CharField(max_length=50)
    sort_title = models.CharField(max_length=200)
    author_last = models.CharField(max_length=200)
    author_first = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    @property
    def available(self):
        return self.limit > len(self.checked_out.all())


class HoldOrder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('time_created',)


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
