from django.db import models
from django.contrib.auth.models import AbstractUser

from .helpers import makenumber


class CustomUser(AbstractUser):
    library_card_number = models.PositiveIntegerField(
        null=True, blank=True,)
    email = models.EmailField(max_length=254, unique=True)
    signup_date = models.DateField(auto_now_add=True, null=True, blank=True)
    is_librarian = models.BooleanField(default=False)
    display_name = models.CharField(max_length=50)
    REQUIRED_FIELDS = ['email', 'display_name']

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """Custom save function allows for creation of a library card
        number if one has not yet been created for the user."""

        if self.is_superuser:
            self.is_librarian = True

        while not self.library_card_number:
            new_number = makenumber()
            all_numbers = [custom_user.library_card_number
                           for custom_user
                           in CustomUser.objects.all()
                           ]
            if new_number not in all_numbers:
                self.library_card_number = new_number
        super(CustomUser, self).save(*args, **kwargs)
