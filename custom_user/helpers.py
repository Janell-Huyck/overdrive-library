from random import randint
from datetime import datetime


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


def greeting():
    current_hour = datetime.now().hour
    if current_hour >= 5 and current_hour < 12:
        return 'Morning'
    elif current_hour >= 12 and current_hour < 18:
        return 'Afternoon'
    else:
        return 'Evening'
