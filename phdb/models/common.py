# -*- coding: utf-8 -*-
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from zope.sqlalchemy.datamanager import ZopeTransactionExtension
#from phdb.models.filldata import populate

__author__ = 'Victor Poluksht'

Session = scoped_session(sessionmaker(extension=ZopeTransactionExtension(), expire_on_commit=False))
meta = declarative_base()

def initialize_sql(engine):
    Session.configure(bind=engine)
    meta.engine = engine
    meta.metadata.bind = engine
    meta.metadata.create_all(engine)
    meta.session = Session()
    try:
        pass
#        populate()
    except IntegrityError:
        Session.rollback()