#!/usr/bin/env python3
"""
Collect data from twitter.
Send data to queue. I use file queue.txt to simplify/for demonstration.
In production use services like Amazon SQS.
"""

import json
import time
import logging
import sys

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

import config as conf
from data_mining import OutQueue

DEBUG = False # False - do not show log_debug() messages

def log_debug(message):
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(message)

def log_error(message):
    logging.error(message)
    

class MyStreamListener(StreamListener):
    """ Handles tweets that are received from the stream. """

    def __init__(self, queue, name='', time_limit_seconds=None, number_limit=None): 
        """ Send twitts to queue. Queue instance must have send_message(message) method
            None in parameters means unlimited """
        super().__init__()
        self.queue = queue
        self.section_name = name
        self.start_time = time.time()
        self.time_limit = time_limit_seconds
        self.number_limit = number_limit
        self.collected = 0

    def on_data(self, raw_data):
        current_time = time.time()
        # if both params is None -> unlimited
        # if one param is none then use limit for other param
        if (self.time_limit is None and self.number_limit is None) or \
           (self.time_limit is None and self.collected < self.number_limit) or \
           (self.number_limit is None and current_time - self.start_time < self.time_limit):
#        if (current_time - self.start_time) < self.time_limit:
            data = json.loads(raw_data)
            try:
                message = {'section': self.section_name, 'body': data['text']}
                self.queue.send_message(message)
            except KeyError: # no data['text'], maybe limit reached?
                log_error("Limit reached; {}".format(data))
                print(data)
                return False
            self.collected += 1
            log_debug(message)
            return True
        else:
            return False # trigger closing the connection

    def on_error(self, status_code):
        log_error(status_code)
    
    def twitts_collected(self):
        return self.collected

def collect_data(conf_section, time_limit=None, number_limit=None):
    """ return how many twtts was collected """
    auth = OAuthHandler(conf.CONSUMER_KEY, conf.CONSUMER_SECRET)
    auth.set_access_token(conf.ACCESS_TOKEN, conf.ACCESS_TOKEN_SECRET)
    
    stream_listener = MyStreamListener(queue=OutQueue(), name=conf_section['name'], \
                                       time_limit_seconds=time_limit, number_limit=number_limit)
    stream = Stream(auth, stream_listener)
    stream.filter(languages=["en"], track=conf_section['search_terms'])
    return stream_listener.twitts_collected()

if __name__ == '__main__':
    try:
        conf_section = next((section for section in conf.SECTIONS if section["name"] == sys.argv[1]))
    except (IndexError, StopIteration):
        conf_section = conf.SECTIONS[0] #default: first config section
 
    print("Collecting twitts for {}: {}".format(conf_section['name'], conf_section['search_terms']))
    twitts_collected = collect_data(conf_section=conf_section, number_limit=30) # or limit by time
    print("Collected: {}".format(twitts_collected))
