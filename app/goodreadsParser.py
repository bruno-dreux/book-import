from bs4 import BeautifulSoup
import requests
import pandas as pd
class GoodreadsParser():
    def __init__(self,params):
        self.booksDf = pd.DataFrame()
        self.params = params

    def getParsedBooks(self):
        return self.booksDf

    def parseGoodreads(self):
        for name, URL in self.params['goodreadsURLs'].items():
            print("Parsing shelf "+name+"...")
            self.parseShelf(URL, name)
            print('Parsed ' + str(len(self.booksDf[self.booksDf['shelf']==name].index)) + ' books in shelf '+name)
        print('Parsed a total of ' + str(len(self.booksDf.index)) + ' books from Goodreads.')


    def parseShelf(self,shelfURL, shelfName):
        continueParsing = True
        page=1

        while continueParsing:
            shelfURL = shelfURL + '&page='+str(page)
            # print("Parsing page " + str(page) + ' in shelf ' + shelfName)
            continueParsing = self.parsePage(shelfURL,shelfName)
            page+=1

        return

    def parsePage(self,pageURL,shelfName):
        pageHasBooks = False
        r = requests.get(pageURL)
        htmlDoc = r.text

        soup = BeautifulSoup(htmlDoc, 'html.parser')

        booksBody = soup.find("tbody",id="booksBody")
        for book in booksBody.find_all("tr"):
            pageHasBooks = True
            dict = parseBook(book, shelfName)
            self.booksDf = self.booksDf.append(dict, ignore_index=True)
        return pageHasBooks

def parseBook(book, shelfName):
    dict = {}
    dict['title'] = str(book.find("td", attrs={"class": "field title"}).div.a.get_text())
    dict['author'] = str(book.find("td", attrs={"class": "field author"}).div.a.get_text())
    dict['avgRating'] = str(book.find("td", attrs={"class": "field avg_rating"}).div.get_text())
    dict['dateStarted'] = str(book.find("td", attrs={"class": "field date_started"}).div.div.div.span.get_text())
    dict['dateRead'] = str(book.find("td", attrs={"class": "field date_read"}).div.div.div.span.get_text())
    dict['dateAdded'] = str(book.find("td", attrs={"class": "field date_added"}).div.span.get_text())
    dict['cover'] = str(book.find("td", attrs={"class": "field cover"}).div.div.a.img['src'])
    dict['shelf'] = shelfName

    return dict


  

    





