from datetime import datetime, timedelta
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, DateTime, Text
from sqlalchemy.orm import sessionmaker



Base = declarative_base()

def db_connection_url():
    return os.getenv('DATABASE_URL', 'postgresql://localhost/queue_archive' )

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

    def elastic_search_bansai(self, message):
        pass
    
    def handler_function_not_defined(self, message):
        """ executed when handler in config but not in Handlers """
        pass
