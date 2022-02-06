import goodreadsParser
import yaml
import notionWriter


def main():
    #Reading params
    paramsFile = open("params.yml")
    parsedParams = yaml.load(paramsFile, Loader = yaml.FullLoader)
    goodreadsParserParams = parsedParams['goodreadsParserParams']

    #Reading secrets
    secretsFile = open("secrets.yml")
    parsedSecrets = yaml.load(secretsFile, Loader = yaml.FullLoader)
    notionToken = parsedSecrets['notion_token']
    notionDatabaseID = parsedSecrets['notion_databaseID']

    #Fetching and parsing books
    parser = goodreadsParser.GoodreadsParser(goodreadsParserParams)
    parser.parseGoodreads()
    df = parser.getParsedBooks()
    # print(df)

    #Writing to Notion
    notion = notionWriter.NotionWriter(notionToken,notionDatabaseID)
    notion.setGoodreadsDb(df)
    notion.convert()
    notion.updateNotion()

    # Test code
    # rowDict = {
    #     'Title': 'Teste pra ir dormir',
    #     'Author': 'Teste autor',
    #     'Status': 'Read',
    #     'Rating': 5,
    #     'Date Started': '2022-02-03',
    #     'Date Finished': '2022-02-04',
    #     'Date Added': '2022-02-05',
    #     'Cover': 'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1598580480l/55148500._SY475_.jpg'
    # }

    # notion.addRow(rowDict)



if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()


#TODO

#Fix lengths > 100 characters issue in goodreadsAPI
#Adjust goodreadsParser to look in more pages for each shelf
#Converter could get the image in higher-res (nice to have)
#Adjust notionWriter to verify if title is already in library before writing
    #If in library, just update the status
#Add a column type to the DB, and always fill it with "Book"


# Get larger images for book covers. There may be a way of changing the URL (example below):
# https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1598580480l/55148500._SY75_.jpg
# https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1598580480l/55148500._SY475_.jpg