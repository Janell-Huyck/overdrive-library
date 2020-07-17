import re
from bs4 import BeautifulSoup
import requests
import random
import smtplib
from email.message import EmailMessage


def scrap_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser').text
    title = re.search(r'[tT]itle: ([ \S]+)', soup)
    author = re.search(r'[aA]uthor: ([ \S]+)', soup)
    release_date = re.search(r'[rR]elease [dD]ate: ([ \S]+)', soup)
    language = re.search(r'[lL]anguage: ([ \S]+)', soup)
    description = re.search(
        r"(\b(The )?Project Gutenberg('s| EBook)[\w\W]*(gutenberg.org(\/license)?|gutenberg.net|before using this ebook.))[\w\W\n]*Title:", soup)

    if not description and title and author:
        new_description = '''The Project Gutenberg EBook of {title}, by {author}

        This eBook is for the use of anyone anywhere at no cost and with
        almost no restrictions whatsoever.  You may copy it, give it away or
        re-use it under the terms of the Project Gutenberg License included
        with this eBook or online at www.gutenberg.org/license'''.format(title=title.group(1), author=author.group(1))

    # breakpoint()
    if not title or not author or not release_date or not language:
        raise ValueError(
            'Sorry, but the page or book you tried to access is unavailable.')
    else:
        return (title.group(1), author.group(1), release_date.group(1), language.group(1), description.group(1) if description else new_description)


def random_color():
    colors = ['#FF0000', '#8b0000', '##FFA500', '#ffffbf', '#fcbe11', '#008000',
              '#0000FF', '#00008B', '#966fd6', '#301934', '#808080', '#FFC0CB', '#000000']
    return random.choice(colors)


def get_sort_title(title):
    small_words = ["A", "An", "The"]
    title = list(title.split(" "))
    if title[0] in small_words:
        title = title[1:]
    return " ".join(title)

def hold_notification_email(user, book):
# MOVE TO ENVIRONMENT VARIABLES!!!!!!!!!!
    address = 'EbookLibraryDemo@gmail.com'
    password = 'OneTwo(12)'
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    msg = EmailMessage()
    msg['Subject'] = 'Your book is available' 
    msg['To'] = user.email
    msg['From'] = address

    msg.set_content('{},\n\nyour copy of {} is ready.\nread it now at {}'.format(user.username,book.title, book.URL))
    # VVV can add html to email if we want to get fancy VVV
    # msg.add_alternative("""\
    # <!DOCTYPE html>
    # <html>
    #     <body>
    #         <h1 style="color:Green;">your copy of {} is ready. read it now at {}</h1>
    #     </body>
    # </html>
    # """.format(book.title, book.URL), subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(address, password)
        smtp.send_message(msg)