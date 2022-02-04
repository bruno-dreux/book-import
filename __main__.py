import goodreadsParser
import yaml


def main():
    #Reading params
    paramsFile = open("params.yml")
    parsedParams = yaml.load(paramsFile, Loader = yaml.FullLoader)
    goodreadsParserParams = parsedParams['goodreadsParserParams']

    #Fetching and parsing books
    parser = goodreadsParser.GoodreadsParser(goodreadsParserParams)
    parser.parse()
    df = parser.getParsedBooks()
    print(df)





if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()