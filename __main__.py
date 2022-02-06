import goodreadsParser
import yaml
import notionWriter


def main():
    #Reading secrets
    secretsFile = open("secrets.yml")
    parsedSecrets = yaml.load(secretsFile, Loader = yaml.FullLoader)
    notionToken = parsedSecrets['notion_token']
    notionDatabaseID = parsedSecrets['notion_databaseID']
    goodreadsParserParams = parsedSecrets['goodreadsParserParams']

    #Fetching and parsing books
    parser = goodreadsParser.GoodreadsParser(goodreadsParserParams)
    parser.parseGoodreads()
    df = parser.getParsedBooks()
    # print(df)

    #Writing to Notion
    notion = notionWriter.NotionWriter(notionToken, notionDatabaseID)
    notion.setGoodreadsDb(df)
    notion.convert()
    notion.updateNotion()



if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
