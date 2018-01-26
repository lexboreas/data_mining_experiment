from datetime import datetime, timedelta
import os
import re

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, DateTime, Text
from sqlalchemy.orm import sessionmaker

def db_connection_url(db_url=None):
    return os.getenv('DATABASE_URL', db_url)

Base = declarative_base()
# model
class Archive(Base):
    __tablename__ = 'archive'

    id = Column(Integer, primary_key=True)
    section = Column(Text)
    body = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def create_db_schema():
    engine = create_engine(db_connection_url(), echo=True) 
    Base.metadata.create_all(engine)

def add_to_archive(message, db_url):
    engine = create_engine(db_connection_url(db_url), echo=False) # hide sql commands 
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(Archive(section=message['section'], body=message['body']))
    session.commit()

# helpers
def get_section_by_name(section_name, sections):
    return next((section for section in sections if section['name'] == section_name), None)

def count_word_in_text(word, text):
    lword = word.lower()
    return sum(lword in word for word in text.lower().split())

def collect_urls_from(text):
    # url_regex stolen from the internet
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_regex, text)
    return urls

class Handlers():
    """ Message handlers: function names same as handler param in config.py """
    def __init__(self, conf):
        self.conf = conf
        self.votes = {} # handle_presidents 
        self.urls = []  # handle_cryptocurrency
    
    def handle_presidents(self, message):
        section = get_section_by_name(message['section'], self.conf.SECTIONS)
        for name in section['search_terms']:
            self.votes[name] = self.votes.get(name, 0) + count_word_in_text(name, message['body'])
 
    def handle_cryptocurrency(self, message):
        self.urls = collect_urls_from(message['body']) + self.urls 
        add_to_archive(message, self.conf.DATABASE_URL)

    def handle_not_defined_handler(self, message):
        """ executed when handler in config but not in Handlers """
        self.show_message(message, 'Handler not defined >>')
    
    def show_message(self, message, prefix='---\n'):
        print(prefix, "Section: {section}\nbody: {body}".format_map(message)) #.format(**message)
