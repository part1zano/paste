from sqlalchemy import create_engine, Table, Column, Integer, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import unidb

engine = create_engine('postgresql://pgsql@{server}/{dbname}'.format(server='172.16.32.1', dbname='paste')) # FIXME :: server, dbname

dbSession = sessionmaker(bind=engine)
Base = declarative_base()

class Paste(Base):
	__tablename__ = 'paste'

	id = Column(Integer, primary_key=True) # FIXME :: must be the same as in postgres
	paste = Column(unidb.CoerceUTF8)

def initdb():
	pass # FIXME :: initdb() and push initial page to table

def new_paste(paste):
	session = dbSession()
	new_paste = Paste(paste=u'{0}'.format(paste))
	session.add(new_paste)
	session.commit()
	return new_paste.id

def get_paste(id):
	session = dbSession()
	for paste in session.query(Paste).filter(Paste.id.in_([id])).all():
		return paste.paste
	return 'oops, no such paste'
