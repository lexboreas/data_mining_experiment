Experimenting with data mining, Twitter API, feeds ...
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
        'name': 'bitcoins',
        'search_terms' : ['#btc', '#bitcoin', '#ltc', '#litecoin', '#eth', '#cryptocurrency'],
        'handler' : 'add_to_archive',
    },
    {
        'name:': 'elections',
        'search_terms' : ['trump', 'clinton'],
        'handler' : 'show_message',
    },
]
---------


Local Postgresql:
pg_ctl -D /usr/local/var/postgres start
pg_ctl -D /usr/local/var/postgres stop

