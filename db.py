from sqlalchemy import create_engine, Table, Column, Integer, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import unidb

engine = create_engine('postgresql://pgsql@localhost/paste')

dbSession = sessionmaker(bind=engine)
Base = declarative_base()

class Paste(Base):
	__tablename__ = 'paste'

	id = Column(Integer, primary_key=True)
	paste = Column(unidb.CoerceUTF8)

