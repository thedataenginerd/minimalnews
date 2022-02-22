# minimalnews

Summarized news content for you to consume.

## Running
### Setting up database
```shell
$ flask shell
>>> db.create_all()
```


Running the news spider: `flask scrape`

Running the API: `flask run`

### Querying
Provide the required categories as query string.
Example:
```
http://127.0.0.1:5000/news?category=politics+sports+opinion+art-culture
```
__Available categories__: politics, opinion, money, sports, art-culture
