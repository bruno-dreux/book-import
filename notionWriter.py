import requests
import json

class NotionWriter():
    def __init__(self, token, databaseID):
        self.token = token
        self.databaseID = databaseID
        self.headers = {"Authorization": "Bearer " + token,
                        "Content-Type": "application/json",
                        "Notion-Version": "2021-08-16"}

    def getDatabase(self):
        url = 'https://api.notion.com/v1/databases/'+self.databaseID+'/query'
        dbJson = self.callNotionAPI(url,None)
        
        rowJson = dbJson['results'][0]
        print(rowJson)

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
