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
    parser.parse()
    df = parser.getParsedBooks()
    print(df)

    #Writing to Notion
    notion = notionWriter.NotionWriter(notionToken,notionDatabaseID)

    rowDict = {
        'Title': 'Teste pra ir dormir',
        'Author': 'Teste autor',
        'Status': 'Read',
        'Rating': 5,
        'Date Started': '2022-02-03',
        'Date Finished': '2022-02-04',
        'Date Added': '2022-02-05',
        'Cover': 'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1598580480l/55148500._SY475_.jpg'
    }

    notion.addRow(rowDict)



if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()


#TODO
#Write a converter that takes in a goodreads format df and create a Notion format df
    #Converter needs to handle dates
    #Converter could get the image in higher-res (nice to have)
#Adjust main to convert output and send to Notion
#Adjust goodreadsParser to look in more pages
#Adjust notionWriter to verify if title is already in library before writing