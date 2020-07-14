from django.contrib import admin
from digital_books.models import Book, HoldOrder


class BookAdmin(admin.ModelAdmin):
    """
    This BookAdmin class courtesy of Dmitry Mugtasimov at
    https://code.djangoproject.com/ticket/12203
    Its purpose is to allow the admin page to display the
    holds field which is a many-to-many field and would
    normally not be displayed because it uses a "through" table.
    This is an issue with Django currently being worked on
    and tracked through the ticket linked above.  Note written: 7/9/2020
    """

    def formfield_for_manytomany(self, *args, **kwargs):
        # We trick Django here to avoid `./manage.py makemigrations`
        # produce unneeded migrations
        HoldOrder._meta.auto_created = True  # pylint: disable=protected-access
        return super().formfield_for_manytomany(*args, **kwargs)


admin.site.register(Book, BookAdmin)
