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

        res = requests.request("POST",url,headers=self.headers)
        data = res.json
        print(res.status_code)
        print(res.text)