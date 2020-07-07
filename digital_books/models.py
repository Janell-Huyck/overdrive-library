from django.db import models
from custom_user.models import CustomUser
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
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    limit = models.IntegerField(default = 3)
    checked_out = models.ManyToManyField(CustomUser, related_name='checked_out')
    holds = models.ManyToManyField(CustomUser, related_name='holds')
    # , through='HoldOrder'
    URL = models.URLField(max_length=200)


class HoldOrder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)