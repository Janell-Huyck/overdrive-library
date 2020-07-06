from random import randint
# from .models import CustomUser


def makenumber():
    """Returns a new library card number.  Library cards are 10 digits (0 - 9)
    long.  These digits are random - there is no special generation process.
    No duplicates between users are allowed. They will be assigned to the user
    on creation of the user account.
    """

    # all_users = CustomUser.objects.all()
    # all_numbers = [custom_user.card_number for custom_user in all_users]

    new_number = "".join([str(randint(0, 10)) for i in range(10)])

    print("new number is:", new_number)
    return new_number
