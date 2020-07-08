Here's how I was picturing the book thing going:

From search page:
    returns some list of book titles & authors.
    next to each book, there is a button "Read This!" (or something)
    onClick, the following happens:
        do a search in Books.objects.filter where author = author and title = title.
        if that search results in nothing:
            create a new Book with the appropriate parameters
        if the Book.checked_out length >= 3
            add the user to the Book.holds list using the first() function (see Mike)
        else:
            add the user to the Book.checked_out property.
        Give a confirmation message to the user: checked out or placed on hold.
        DO NOTHING ELSE.

        

From the custom_user page:
    returns a list of all books the user has on hold and all books the user has checked out.
        to get this, do a Book.objects.filter(checked_out contains user)
    next to each checked out book, there is a button "Download HTML" (or something)
    onClick, the following happens:
        create a JSON "fetch" request and send it to Project Gutenburg's API asking for the HTML
        Download the HTML
        Process the data, and open it in a new page.
    next to each checked out book there is a button "Return book" (or something)
    onClick, the following happens:
        remove this user from the checked_out field on that book
        look for any names on the holds field.
        if there are names:
            determine the first one (there is a date field somewhere)
            add that first user's name to the checked_out field
            possibly: create a notification message to be displayed on the other user's page?
        the book should automatically disappear from the user's "checked_out" list.
    