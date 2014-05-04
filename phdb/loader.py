# -*- coding: utf-8 -*-
import logging
import traceback
import urllib
import shutil
import transaction
import whoosh
from whoosh.fields import Schema, ID, TEXT, NUMERIC
from phdb.models import Record
from phdb.models.common import Session
import os.path
from whoosh.index import create_in


__author__ = 'vpol'

log = logging.getLogger(__name__)


def funcname(obj=None):
    '''Вывод текущего метода'''
    stack = traceback.extract_stack()
    scriptName, lineNum, funcName, lineOfCode = stack[-2]
    if obj:
        return '%s.%s()' % (obj.__class__.__name__, funcName)
    else:
        return '%s()' % funcName


def file_loader(links, data_path, simulate):
    if simulate:
        return []
    files = []
    for l in links.split(','):
        log.debug('In {0}: processing file {1}'.format(funcname(), l))
        url = l.strip()
        file_name = url.split('/')[-1]
        try:
            urllib.request.urlretrieve(url, data_path + '/' + file_name)
        except Exception as e:
            log.error('in {0}: error {1}'.format(funcname(), e.__traceback__))
            continue
        else:
            files.append(data_path + '/' + file_name)
    return files


def dbload(files, simulate):
    if simulate:
        return
    session = Session()
    to_add = []
    for f in files:
        log.debug('in {0}: processing file {1}'.format(funcname(), f))
        with open(f, encoding='cp1251') as data_file:
            counter = 0
            for d_line in data_file:
                counter += 1
                if counter == 1:
                    continue
                r = Record()
                r.code, r.nfrom, r.nto, r.amount, r.operator, r.region = d_line.rstrip().split(';')
                # log.debug('in {0}: r.code = {1}, r.nfrom = {2}, r.nto = {3}, r.amount = {4}, r.operator = {5}, r.region = {6}'.format(funcname(), r.code, r.nfrom, r.nto, r.amount, r.operator, r.region))
                if len(to_add) > 1000:
                    session.add_all(to_add)
                    transaction.commit()
                    to_add = []
                to_add.append(r)
            session.add_all(to_add)
            transaction.commit()
            to_add = []
    return


def reindex(files, ix_path, simulate):
    if simulate:
        ix = whoosh.index.open_dir(ix_path)
        return ix
    schema = Schema(id=NUMERIC(stored=True), operator=TEXT(stored=True), region=TEXT(stored=True))
    if not os.path.exists(ix_path):
        os.mkdir(ix_path)
    else:
        shutil.rmtree(ix_path)
        os.mkdir(ix_path)
    ix = create_in(ix_path, schema)
    writer = ix.writer()
    session = Session()
    q = session.query(Record).all()
    for r in q:
        try:
            # log.debug('in {0}: adding {1}, {2}, {3}'.format(funcname(), r.id, r.operator, r.region))
            writer.add_document(id=r.id, operator=r.operator, region=r.region)
        except whoosh.writing.IndexingError as index_error:
            log.error('in {0}: error adding document {1}'.format(funcname(), index_error))
            continue
    writer.commit()
    return ix