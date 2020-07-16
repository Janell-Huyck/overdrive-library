# Overdrive - Library

Overdrive-Library is a Python/Django project that recreates an online library's backend.  

The library backend is a database of books, with Title, Author, description, languange, and link to the online HTML-version books from [Project Gutenberg](https://www.gutenberg.org/) added, modified, and deleted by Librarians.

Patrons (regular users) and Librarians may browse books, check them out to gain access to the HTML link, or place a hold on the book if more than three users have checked it out already.

## Installation

Use the package manager Poetry to install and run Overdrive-Library.

1. $ poetry install     // Installs dependencies for virtual environment.
2. $ poetry shell       // Activates virtual environment.

Then, you will need to create a superuser account.

3. $ python manage.py createsuperuser   //Fill out all required fields at the prompts.

Optional: pre-populate your library with a given number of random books from the over 60,000 available at Project Gutenberg.  Use this custom-made command to do so:

4. $ python manage.py populate_books <20>     //substitue in any number of books (< 60,000) to preload that many books to your database.

Start the server:

5. $ python manage.py runserver --insecure  //note - starting the server in "insecure" mode will allow it to properly display the CSS and images contained.  The program will function without it but looses much of its visual appeal.


## Usage

Navigate to your local port on your browser at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Use the navbar buttons at the top of the page to take you to either the login page or to create an account.  Once you are signed in, it's time to look for some books to check out!


## Contributing

This was a capstone project for the fourth quarter at Kenzie Academy.  It was built in two and a half weeks by a team of four:  [Earth Mobley](https://github.com/EarthHadjo), [Luis Fuentes](https://github.com/luisfff29), [Michael Gabbard](https://github.com/zanvoy), and [Janell Huyck](https://github.com/Janell-Huyck).  

## License
[MIT](https://choosealicense.com/licenses/mit/)