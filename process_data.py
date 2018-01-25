#!/usr/bin/env python3
"""
Process data from queue.
"""
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, DateTime, Text
from sqlalchemy.orm import sessionmaker

import config as conf
from data_mining import InQueue

Base = declarative_base()

def db_connection_url():
    return 'postgresql://localhost/queue_archive'

# model
class Archive(Base):
    __tablename__ = 'archive'

    id = Column(Integer, primary_key=True)
    section = Column(Text)
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def create_db_schema():
    engine = create_engine(db_connection_url(), echo=True) 
    Base.metadata.create_all(engine) # create db schema


def add_to_archive(message):
    engine = create_engine(db_connection_url(), echo=False) # hide sql commands 
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(Archive(section=message['section'], body=message['body']))
    session.commit()

def show_message(message):
    #print(message)
    print("---\nsection: {section}\nbody: {body}".format_map(message)) #.format(**message)

# helpers
def choose_handler_for(section_name, sections):
    handler = next((section['handler'] for section in sections if section['name'] == section_name), None) # default: None
    return handler
    # handler = None
    # for section in sections:
    #     if section['name'] == section_name:
    #         handler = section['handler']
    # return handler

class Handlers():
    """ Message handlers: same names as handler param from config """
    
    def add_to_archive(self, message):
        engine = create_engine(db_connection_url(), echo=False) # hide sql commands 
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(Archive(section=message['section'], body=message['body']))
        session.commit()
    
    def show_message(self, message):
        print("---\nsection: {section}\nbody: {body}".format_map(message)) #.format(**message)

    def elastice_search_bansai(self, message):
        pass
    
    def handler_function_not_defined(self, message):
        """ executed when handler in config but not in Handlers """
        pass


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
#    create_db_schema()
