import re
from bs4 import BeautifulSoup
import requests


def scrap_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser').text
    title = re.search(r'[tT]itle: ([ \S]+)', soup)
    author = re.search(r'[aA]uthor: ([ \S]+)', soup)
    release_date = re.search(r'[rR]elease [dD]ate: ([ \S]+)', soup)
    language = re.search(r'[lL]anguage: ([ \S]+)', soup)
    description = re.search(
        r"(\b(The )?Project Gutenberg('s| [eE][bB]ook)[\w\W]*(gutenberg.org(\/license)?|gutenberg.net|before using this ebook.))[\w\W\n]*Title:", soup)

    if not title or not author or not release_date or not language or not description:
        raise ValueError(
            'Sorry, but the page or book you tried to access is unavailable.')
    else:
        return (title.group(1), author.group(1), release_date.group(1), language.group(1), description.group(1))
