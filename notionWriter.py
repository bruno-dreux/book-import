import requests
import json
import pandas as pd

class NotionWriter():
    def __init__(self, token, databaseID):
        self.token = token
        self.databaseID = databaseID
        self.headers = {"Authorization": "Bearer " + token,
                        "Content-Type": "application/json",
                        "Notion-Version": "2021-08-16"}
        self.notionDb = pd.DataFrame()
        self.goodreadsDb = pd.DataFrame()

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
            print("     Pushing book: "+book['Title'])
            self.addRow(book)
        

    def addRow(self,rowDict):
        url = "https://api.notion.com/v1/pages/"
        jsonRow = self.rowToJson(rowDict)
        self.callNotionAPI(url,jsonRow)

    def callNotionAPI(self, url, body):
        res = requests.request("POST",url,data=body,headers=self.headers)
        if res.status_code == 200:
            response = json.loads(res.text)
            return response
        else:
            print("Error calling Notion API. Error code: "+str(res.status_code))
            print(res.text)
            return

    def rowToJson(self, rowDict):
        newDict = {
            'parent': {
                'database_id': self.databaseID
            },
            'properties': {
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
                "Rating": {
                    "type": "number",
                    "number": rowDict['Rating']
                },
                "Date Started": {
                    "type": "date",
                    "date": {
                        "start": rowDict['Date Started'],
                        "end": None,
                        "time_zone": None
                    }
                },
                "Date Finished": {
                    "type": "date",
                    "date": {
                        "start": rowDict['Date Finished'],
                        "end": None,
                        "time_zone": None
                    }
                },
                "Date Added": {
                    "type": "date",
                    "date": {
                        "start": rowDict['Date Added'],
                        "end": None,
                        "time_zone": None
                    }
                },
                "Cover": {
                    "type": "files",
                    "files": [
                        {
                            "name": rowDict['Title'],
                            "type": "external",
                            "external": {
                                "url": rowDict['Cover']
                            }
                        }
                    ]
                }
            }
        }

        jsonRow = json.dumps(newDict)
        # print(jsonRow)
        return(jsonRow)

def invertAuthor(author):
    lastName = author[0:author.find(",")].strip()
    firstName = author[author.find(",")+1:].strip()
    
    return firstName + ' ' + lastName
    
def getImprovedPictureURL(pictureURL):
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
        convertedDate = ""
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