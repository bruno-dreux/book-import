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
    notion.getDatabase()





if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()