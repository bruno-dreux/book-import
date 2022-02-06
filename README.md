# Book import
Script to import list of books from Goodreads to Notion using scraping and the Notion API.


## Usage
1) Add secrets to the repository (follow the template in secrets_template.yml)
2) Install any needed dependencies using `pip install` (list of dependencies below)
3) Run using `make run` or `python book-import` (from outside the directory) or using `python __main__.py` from inside the directory.

## Detailed functioning
- Accesses the goodreads lists using the list in secrets.yml
- Scrapes it (no need for a login) and gathers book information
- Pushes items to a notion DB using its API (need to configure a token and database ID in secrets.yml)
  - If item already exists in Notion, checks if an update is needed (status or read dates)
  - If an update is needed, pushes the updated book to Notion

## Dependencies
- Python 3.9.0
- yaml
- requests
- json
- pandas
- pyshorteners
- Beautiful Soup (bs4)
- codecs

## Points of improvement for the future
- Create a retry mechanism for the Notion API (has showed some 500 errors during testing)
- Use the Goodreads API instead of scraping (need to confirm if possible)
- Refactor code to reduce the number of API calls and do most of the filtering locally (to improve performance)
- The name of the lists in Goodreads is not configurable, if lists are named differently it will take some refactoring