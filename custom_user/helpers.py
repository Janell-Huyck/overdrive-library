from random import randint


def makenumber():
    """Returns a new library card number.  Library cards are 10 digits (0 - 9)
    long.  These digits are random - there is no special generation process.
    No duplicates between users are allowed. They will be assigned to the user
    on creation of the user account.
    """
    new_number = str(randint(1, 9))
    new_number += "".join([str(randint(0, 9)) for i in range(9)])

    print("new number is:", new_number)
    return new_number
