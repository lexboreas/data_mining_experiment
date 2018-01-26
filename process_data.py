#!/usr/bin/env python3
"""
Process data from queue.
"""

import config
from data_mining import InQueue
from data_mining import Handlers

# helpers
def choose_handler_for(section_name, sections):
    handler = next((section['handler'] for section in sections if section['name'] == section_name), None)
    return handler
    # handler = None
    # for section in sections:
    #     if section['name'] == section_name:
    #         handler = section['handler']
    # return handler

class QueueRunner:

    def __init__(self, queue, conf, default_handler=lambda m: print("-->>", m)):
        self.queue = queue
        self.conf = conf
        self.default_handler = default_handler # function when handler not in config
        self.processed = 0
        self.handlers = Handlers(self.conf)

    def process_all_messages(self):
        for message in self.queue.receive_message():
            handler = choose_handler_for(message['section'], self.conf.SECTIONS)
            if handler is None: # this handler not in config
                self.default_handler(message) # 
            else:
                # call handler, better than eval()
                getattr(self.handlers, handler, self.handlers.handle_not_defined_handler)(message) 
            self.processed += 1
        return self.processed


if __name__ == '__main__':
    my_queue = InQueue()
    print("Items in queue: {}".format(my_queue.size()), end=", ")
    qrunner = QueueRunner(my_queue, config)
    processed = qrunner.process_all_messages()
    print("Processed:", processed)

    def presidents_popularity_in_media(votes):
        if bool(votes):
            print("Votes: {}".format(votes))
            winner = max(votes, key=votes.get)
            print("{} win this round".format(winner.capitalize()))

    presidents_popularity_in_media(qrunner.handlers.votes)

    def print_crypto_urls(urls):
        if urls:
            urls = list(set(urls)) # remove dubs
            print("Crypto urls:", "\n".join(urls))

    print_crypto_urls(qrunner.handlers.urls)
