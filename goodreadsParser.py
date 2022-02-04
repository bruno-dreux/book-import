from bs4 import BeautifulSoup
import requests
import codecs

def parse():

    #Code to get the page from the URL
    # url = 'https://www.goodreads.com/review/list/75444766-bruno-dreux?utf8=%E2%9C%93&ref=nav_mybooks&per_page=20'
    # r = requests.get(url)
    # html_doc = r.text

    #Temporary code, loading from a saved html
    html_doc = codecs.open("example.html", 'r')

    soup = BeautifulSoup(html_doc, 'html.parser')
    # print(soup.prettify())

    booksBody = soup.find("tbody",id="booksBody")
    for book in booksBody.find_all("tr"):
        # print(book.prettify())
        parseBook(book)

def parseBook(book):
    title = book.find("td", attrs={"class": "field title"}).div.a.get_text()
    author = book.find("td", attrs={"class": "field author"}).div.a.get_text()
    avgRating = book.find("td", attrs={"class": "field avg_rating"}).div.get_text()
    shelf = book.find("td", attrs={"class": "field shelves"}).div.span.a.get_text()
    dateStarted = book.find("td", attrs={"class": "field date_started"}).div.div.div.span.get_text()
    dateRead = book.find("td", attrs={"class": "field date_read"}).div.div.div.span.get_text()
    dateAdded = book.find("td", attrs={"class": "field date_added"}).div.span.get_text()
    cover = book.find("td", attrs={"class": "field cover"}).div.div.a.img['src']



# TO DO
# Get larger images for book covers. There may be a way of changing the URL (example below):
# https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1598580480l/55148500._SY75_.jpg
# https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1598580480l/55148500._SY475_.jpg