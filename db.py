from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import unidb

engine = create_engine('postgresql://{dbuser}@{dbserver}/{dbname}'.format(dbserver='172.16.32.1', dbname='paste', dbuser='paste'))  # FIXME :: server, dbname

dbSession = sessionmaker(bind=engine)
Base = declarative_base()


class Paste(Base):
    __tablename__ = 'paste'

    id = Column(Integer, primary_key=True)  # FIXME :: must be the same as in postgres
    paste = Column(unidb.CoerceUTF8)


def initdb():
    Base.metadata.create_all(engine)
    session = dbSession()
    with open('README.md', 'r') as f:
        paste = f.read()
    new_paste = Paste(paste=u'{0}'.format(paste))
    session.add(new_paste)
    session.commit()


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


if __name__ == '__main__':
    initdb()
