import requests
import json
import pandas as pd
from pyshorteners import Shortener

class NotionWriter():
    def __init__(self, token, databaseID):
        self.token = token
        self.databaseID = databaseID
        self.headers = {"Authorization": "Bearer " + token,
                        "Content-Type": "application/json",
                        "Notion-Version": "2021-08-16"}
        self.notionDb = pd.DataFrame()
        self.goodreadsDb = pd.DataFrame()
        self.addedBooks = 0
        self.updatedBooks = 0
        self.noChangeBooks = 0

    def getDatabase(self):
        url = 'https://api.notion.com/v1/databases/'+self.databaseID+'/query'
        dbJson = self.callNotionAPI(url,None)
        
        rowJson = dbJson['results'][0]
        print(rowJson)
    
    def setGoodreadsDb(self,goodreadsDb):
        self.goodreadsDb = goodreadsDb

    def convert(self):
        # print(self.goodreadsDb)
        nDb = self.goodreadsDb # nDb will later become self.notionDb
        
        #Applying conversions
        nDb['Author'] = nDb.apply(lambda row: invertAuthor(row['author']),axis=1)
        nDb['Rating'] = nDb.apply(lambda row: float(row['avgRating'].replace('\n',"")),axis=1)
        nDb['Cover'] = nDb.apply(lambda row: getImprovedPictureURL(row['cover']),axis=1)
        nDb['Date Added'] = nDb.apply(lambda row: convertDate(row['dateAdded']),axis=1)
        nDb['Date Started'] = nDb.apply(lambda row: convertDate(row['dateStarted']),axis=1)
        nDb['Date Finished'] = nDb.apply(lambda row: convertDate(row['dateRead']),axis=1)
        nDb['Status'] = nDb.apply(lambda row: convertStatus(row['shelf']),axis=1)
        nDb['Title'] = nDb.apply(lambda row: row['title'].replace('\n',"").strip(),axis=1)
        
        nDb = nDb.drop(['author','avgRating','cover','dateAdded','dateRead','dateStarted','shelf','title'],axis=1)
        # print (nDb)
        self.notionDb = nDb
        
    def updateNotion(self):
        listOfDicts = self.notionDb.to_dict(orient='records')
        print("Starting to push books to Notion...")
        for book in listOfDicts:
            # print("     Pushing book: "+book['Title'])
            self.updateOrAddRow(book)
        print("Update complete! Total of "+str(self.addedBooks+self.noChangeBooks+self.updatedBooks)+" books processes from Goodreads.")
        print("Added "+str(self.addedBooks)+" books. Updated "+str(self.updatedBooks)+" books. Did not change "+str(self.noChangeBooks)+" books in DB.")
        
    def updateOrAddRow(self,rowDict):
        isInNotionDb = self.findAndUpdate(rowDict)

        if isInNotionDb == False:
            self.addRow(rowDict)

    def findAndUpdate(self,rowDict):
        url = 'https://api.notion.com/v1/databases/'+self.databaseID+'/query'
        requestBody = self.createFindRequestBody(rowDict)
        
        dbJson = self.callNotionAPI(url,requestBody)
        pageJson = dbJson['results']

        if (len(pageJson)==0):
            #Book not found in Notion DB
            # print("Book not in DB. Adding...")
            return False

        else:
            #Book is in DB
            pageJson = pageJson[0] #Gets the first element of the 1-sized list
            
            if self.checkNeedForUpdate(rowDict,pageJson):
                #Update
                # print("Update needed!")
                self.updateBook(pageJson['id'],rowDict)
                return True

            else:  #No need to update, everything up to date
                # print("Everything up to date, moving on...")
                self.noChangeBooks += 1
                return True
        
        return False

    def checkNeedForUpdate(self,rowDict,pageJson):
        #Get properties to see if an update is needed
        notionDbDict = {}
        notionDbDict['Status'] = pageJson['properties']['Status']['select']['name']
        try:
            notionDbDict['Date Started'] = pageJson['properties']['Date Started']['date']['start']
        except:
            notionDbDict['Date Started'] = None
        try:
            notionDbDict['Date Finished'] = pageJson['properties']['Date Finished']['date']['start']
        except:
            notionDbDict['Date Finished'] = None
        try:
            notionDbDict['Date Added'] = pageJson['properties']['Date Added']['date']['start']
        except:
            notionDbDict['Date Added'] = None

        needUpdate = False
        for key, value in notionDbDict.items():
            # print(rowDict[key])
            # print(notionDbDict[key])
            if notionDbDict[key] != rowDict[key]:
                needUpdate = True
        return needUpdate

    def addRow(self,rowDict):
        url = "https://api.notion.com/v1/pages/"
        jsonRow = self.rowToJson(rowDict)
        self.callNotionAPI(url,jsonRow)
        self.addedBooks += 1

    def updateBook(self,bookID,rowDict):
        # print(bookID)
        propertiesPayload = self.createJsonForUpdate(rowDict)
        url = "https://api.notion.com/v1/pages/"+bookID
        self.callNotionAPI(url,propertiesPayload,"PATCH")
        self.updatedBooks += 1
        # print("Book updated!")
        return

    def callNotionAPI(self, url, body,requestType="POST"):
        res = requests.request(requestType,url,data=body,headers=self.headers)
        if res.status_code == 200:
            response = json.loads(res.text)
            return response
        else:
            print("Error calling Notion API. Error code: "+str(res.status_code))
            print(res.text)
            return

    def rowToJson(self, rowDict):
        propertiesDict = {
            'Title': {
                'title': [
                    {
                        'text': {
                            'content': rowDict['Title']
                        }
                    }
                ]
            },
            "Author": {
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": rowDict['Author'],
                            "link": None
                        }
                    }
                ]
            },
            "Status": {
                "type": "select",
                "select": {
                    "name": rowDict['Status']
                }
            },
            "Type": {
                "type": "select",
                "select": {
                    "name": "Book"
                }
            },
            "Rating": {
                "type": "number",
                "number": rowDict['Rating']
            },
            "Cover": {
                "type": "files",
                "files": [
                    {
                        "name": rowDict['Title'][0:99],
                        "type": "external",
                        "external": {
                            "url": rowDict['Cover']
                        }
                    }
                ]
            }
        }

        if rowDict['Date Started'] != None:
            propertiesDict["Date Started"] = {
                "type": "date",
                "date": {
                    "start": rowDict['Date Started'],
                    "end": None,
                    "time_zone": None
                }
            }

        if rowDict['Date Added'] != None:
            propertiesDict["Date Added"] = {
                "type": "date",
                "date": {
                    "start": rowDict['Date Added'],
                    "end": None,
                    "time_zone": None
                }
            }

        if rowDict['Date Finished'] != None:
            propertiesDict["Date Finished"] = {
                "type": "date",
                "date": {
                    "start": rowDict['Date Finished'],
                    "end": None,
                    "time_zone": None
                }
            }
        
        newDict = {
            'parent': {
                'database_id': self.databaseID
            },
            'properties': propertiesDict
        }

        jsonRow = json.dumps(newDict)
        # print(jsonRow)
        return(jsonRow)

    def createJsonForUpdate(self, rowDict):
        propertiesDict = {
            "Status": {
                "type": "select",
                "select": {
                    "name": rowDict['Status']
                }
            },
            "Rating": {
                "type": "number",
                "number": rowDict['Rating']
            }
        }

        if rowDict['Date Started'] != None:
            propertiesDict["Date Started"] = {
                "type": "date",
                "date": {
                    "start": rowDict['Date Started'],
                    "end": None,
                    "time_zone": None
                }
            }

        if rowDict['Date Added'] != None:
            propertiesDict["Date Added"] = {
                "type": "date",
                "date": {
                    "start": rowDict['Date Added'],
                    "end": None,
                    "time_zone": None
                }
            }

        if rowDict['Date Finished'] != None:
            propertiesDict["Date Finished"] = {
                "type": "date",
                "date": {
                    "start": rowDict['Date Finished'],
                    "end": None,
                    "time_zone": None
                }
            }
        
        newDict = {
            'properties': propertiesDict
        }

        jsonForUpdate = json.dumps(newDict)
        # print(jsonRow)
        return(jsonForUpdate)

    def createFindRequestBody(self, rowDict):
        filterDict = {
            "filter": {
                "and": [
                    {
                        "property": "Title",
                        "text": {
                            "equals": rowDict['Title']
                        }
                    },
                    {
                        "property": "Author",
                        "text": {
                            "equals": rowDict['Author']
                        }
                    }
                ]
            }
        }

        jsonRow = json.dumps(filterDict)
        # print(jsonRow)
        return(jsonRow)

def invertAuthor(author):
    lastName = author[0:author.find(",")].strip()
    firstName = author[author.find(",")+1:].strip()
    
    return firstName + ' ' + lastName
    
def getImprovedPictureURL(pictureURL):
        pictureURL = pictureURL.replace("._SY75_","")
        pictureURL = pictureURL.replace("._SX50_","")

        if len(pictureURL) > 100:
            print(pictureURL)
            urlShortener = Shortener()
            pictureURL = urlShortener.tinyurl.short(pictureURL)
            print(pictureURL)

        return pictureURL


def convertStatus(shelf):
    dict = {
        'read': 'Read',
        'toRead': 'To Read',
        'dropped': 'Dropped',
        'reading': 'Reading'
    }
    
    if shelf.find(",") != -1:  # Protection against multiple statuses, using the first one
        shelf = shelf[0:shelf.find(",")]
    
    return dict[shelf]

def convertDate(date):
    convertedDate = date
    if date == "not set":
        convertedDate = None
    else:
        year = date.strip()[-4:]
        month = monthToNumerical(date.strip()[0:3])
        day = date.strip()[4:6]
        convertedDate = year+'-'+month+'-'+day
        # print(convertedDate)
    return convertedDate

def monthToNumerical(month):
    dict = {
        'Jan':'01',
        'Feb':'02',
        'Mar':'03',
        'Apr':'04',
        'May':'05',
        'Jun':'06',
        'Jul':'07',
        'Aug':'08',
        'Sep':'09',
        'Oct':'10',
        'Nov':'11',
        'Dec':'12',
    }
    return dict[month]