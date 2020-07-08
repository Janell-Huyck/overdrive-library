import re
from bs4 import BeautifulSoup
import requests


def scrap_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = re.search(r'[tT]itle: ([ \S]+)', soup.text)
    author = re.search(r'[aA]uthor: ([ \S]+)', soup.text)

    if not title and not author:
        return ("Unknown", "Unknown")
    elif not title:
        return ("Unknown", author.group(1))
    elif not author:
        return (title.group(1), "Unknown")
    else:
        return (title.group(1), author.group(1))
