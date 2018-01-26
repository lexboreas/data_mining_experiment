Experimenting with data mining, Twitter API ...
Do not use any part of this app in production.  It's not threadsafe, not fast and full of bugs.


config.py example:
---------
# Twitter config
CONSUMER_KEY = "..." 
CONSUMER_SECRET = "..."
ACCESS_TOKEN = "..."
ACCESS_TOKEN_SECRET = "..."

SECTIONS = [
    {
        'name': 'presidents',
        'search_terms' : ['merkel', 'trump', 'putin'],
        'handler' : 'handle_presidents',
    },
    {
        'name': 'bitcoins',
        'search_terms' : ['btc', 'bitcoin', 'ltc', 'litecoin', 'eth', 'cryptocurrency'],
        'handler' : 'handle_cryptocurrency',
    },
]

# Db to archive data
DATABASE_URL = 'postgresql://localhost/queue_archive'


Testing with unittest
---------
Run a single test:
$ python -m unittest test.test_handlers

Run all the tests:
$ python -m unittest discover