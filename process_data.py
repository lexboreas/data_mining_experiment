#!/usr/bin/env python3
"""
Process data from queue.
"""

import config as conf
from data_mining import InQueue
from data_mining import Handlers

# helpers
def choose_handler_for(section_name, sections):
    handler = next((section['handler'] for section in sections if section['name'] == section_name), None) # default: None
    return handler
    # handler = None
    # for section in sections:
    #     if section['name'] == section_name:
    #         handler = section['handler']
    # return handler

class MessageProcessor:

    def __init__(self, queue, sections, default_handler=lambda m: print("-->>", m)):
        self.queue = queue
        self.sections = sections
        self.default_handler = default_handler # function when handler not in config
        self.processed = 0

    def process_all_messages(self):
        myhandlers = Handlers()
        for message in self.queue.receive_message():
            handler = choose_handler_for(message['section'], self.sections)
            if handler is None: # this handler not in config
                self.default_handler(message) # 
            else:
                # call handler, better than eval()
                getattr(myhandlers, handler, 'handler_function_not_defined')(message) 
            self.processed += 1
        return self.processed


if __name__ == '__main__':
    my_queue = InQueue()
    print("Items in queue: {}".format(my_queue.size()))
    mp = MessageProcessor(my_queue, conf.SECTIONS)
    processed = mp.process_all_messages()
    print("Processed:", processed)