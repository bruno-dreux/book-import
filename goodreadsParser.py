from bs4 import BeautifulSoup
import requests
import codecs
import pandas as pd
class GoodreadsParser():
    def __init__(self,params):
        self.booksDf = pd.DataFrame()
        self.params = params

    def getParsedBooks(self):
        return self.booksDf

    def parse(self):
        
        #Code to get the page from the URL
        url = self.params['goodreadsURL']
        # r = requests.get(url)
        # html_doc = r.text
        
        #Temporary code, loading from a saved html
        html_doc = codecs.open("example.html", 'r')

        soup = BeautifulSoup(html_doc, 'html.parser')
        # print(soup.prettify())

        booksBody = soup.find("tbody",id="booksBody")
        for book in booksBody.find_all("tr"):
            # print(book.prettify())
            dict = parseBook(book)
            self.booksDf = self.booksDf.append(dict, ignore_index=True)
        return

def parseBook(book):
    dict = {}
    dict['title'] = str(book.find("td", attrs={"class": "field title"}).div.a.get_text())
    dict['author'] = str(book.find("td", attrs={"class": "field author"}).div.a.get_text())
    dict['avgRating'] = str(book.find("td", attrs={"class": "field avg_rating"}).div.get_text())
    dict['shelf'] = str(book.find("td", attrs={"class": "field shelves"}).div.span.a.get_text())
    dict['dateStarted'] = str(book.find("td", attrs={"class": "field date_started"}).div.div.div.span.get_text())
    dict['dateRead'] = str(book.find("td", attrs={"class": "field date_read"}).div.div.div.span.get_text())
    dict['dateAdded'] = str(book.find("td", attrs={"class": "field date_added"}).div.span.get_text())
    dict['cover'] = str(book.find("td", attrs={"class": "field cover"}).div.div.a.img['src'])

    return dict


  

    





# TO DO
# Get larger images for book covers. There may be a way of changing the URL (example below):
# https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1598580480l/55148500._SY75_.jpg
# https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1598580480l/55148500._SY475_.jpg