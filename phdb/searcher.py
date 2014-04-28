# -*- coding: utf-8 -*-
import Stemmer
import logging
import os
import re
import gc
from sqlalchemy.sql.expression import and_
import transaction
# from whoosh. import store
from whoosh.fields import Schema, ID, TEXT
from whoosh.index import create_in, Index, open_dir
from whoosh.qparser.default import QueryParser
from phdb.models import Record
from phdb.models.common import meta

__author__ = 'Victor Poluksht'

log = logging.getLogger(__name__)

def search(self, code = None, number= None, operator=None):
    results = []
    try:
        if code and not number and not operator:
            '''введен код, номер и оператор'''
            query = meta.session.query(Record).filter(Record.code.like(code + '%'))
            for r in query:
                results.append(r)
        elif code and number and not operator:
            if number.find('*') >= 1:
                tmpnum = number[0:number.find('*')]
                full_number = number.replace('*', '.') + ''.join(['.' for c in range(0, 7 - len(number))])
                query = meta.session.query(Record).filter(Record.code == code).filter(Record.nfrom.like(tmpnum + '%'))
                for r in query:
                    log.debug((r.nfrom, r.nto))
                    for x in range(r.nfrom, r.nto):
                        n = re.match(r'%s' % full_number, str(x))
                        if n:
                            c = Record()
                            c.code = r.code
                            c.nfrom = str(x)
                            c.nto = str(x)
                            c.region = r.region
                            c.operator = r.operator
                            results.append(c)
                            c = None
                        n = None
                tmpnum = int(tmpnum + ''.join(['0' for z in range(0, 7 - len(tmpnum))]))
                results1 = []
                log.debug(tmpnum)
                query = None
                query1 = meta.session.query(Record).filter(Record.code == code).filter(and_(Record.nfrom <= tmpnum, Record.nto >= tmpnum))
                for r in query1:
                    log.debug((r.nfrom, r.nto))
                    log.debug(full_number)
                    for x in range(r.nfrom, r.nto):
                        n = re.match(r'%s' % full_number, str(x))
                        if n:
                            c = Record()
                            c.code = r.code
                            c.nfrom = str(x)
                            c.nto = str(x)
                            c.region = r.region
                            c.operator = r.operator
                            results1.append(c)
                            c = None
                        n = None
                    log.debug(results1)
                query1 = None
                gc.collect()
                return list(sorted(set(results + results1)))
            query = meta.session.query(Record).filter(Record.code == code).filter(Record.nfrom.like(number + '%'))
            for r in query:
                results.append(r)
            full_number = int(number + ''.join(['0' for c in range(0, 7 - len(number))]))
            query = meta.session.query(Record).filter(Record.code == code).filter(and_(Record.nfrom <= full_number, Record.nto >= full_number))
            for r in query:
                if not r in results:
                    results.append(r)
        elif code and number and operator:
            results1 = []
            query = meta.session.query(Record).filter(Record.code == code).filter(Record.nfrom.like(number + '%'))
            for r in query:
                results1.append(r)
            full_number = int(number + ''.join(['0' for c in range(0, 7 - len(number))]))
            query = meta.session.query(Record).filter(Record.code == code).filter(and_(Record.nfrom <= full_number, Record.nto >= full_number))
            for r in query:
                if not r in results1:
                    results1.append(r)
            log.debug([r.id for r in results1])
            results2 = []
            s = re.sub(r'[,-/;\'.*:@!#$%^&?()№{}\[\]+=]', ' ', operator).split(' ')
            tstr1 = ' and '.join(['operator:%s*' % x for x in s])
            query = self.parser.parse(tstr1)
            for res in self.ix.searcher().search(query, limit=None):
                id = res['id']
                r = meta.session.query(Record).filter(Record.id == id).one()
                results2.append(r)
            log.debug([r.id for r in results2])
            resu = []
            resu.extend(set(results1).intersection(set(results2)))
            log.debug(resu)
            return resu
        elif not code and not number and operator:
            log.debug(operator)
            s = re.sub(r'[,-/;\'.*:@!#$%^&?()№{}\[\]+=]', ' ', operator).split(' ')
            #s = operator.split(' ')
            tstr1 = ' and '.join(['operator:%s*' % x for x in s])
            query = self.parser.parse(tstr1)
            for res in self.ix.searcher().search(query, limit=None):
                id = res['id']
                r = meta.session.query(Record).filter(Record.id == id).one()
                results.append(r)
        elif not code and number and operator:
            results1 = []
            full_number = int(number + ''.join(['0' for c in range(0, 7 - len(number))]))
            query = meta.session.query(Record).filter(and_(Record.nfrom <= full_number, Record.nto >= full_number))
            for r in query:
                results1.append(r)
            results2 = []
            s = re.sub(r'[,-/;\'.*:@!#$%^&?()№{}\[\]+=]', ' ', operator).split(' ')
            tstr1 = ' and '.join(['operator:%s*' % x for x in s])
            query = self.parser.parse(tstr1)
            for res in self.ix.searcher().search(query, limit=None):
                id = res['id']
                r = meta.session.query(Record).filter(Record.id == id).one()
                results2.append(r)
            resu = []
            resu.extend(set(results1).intersection(set(results2)))
            return resu
        elif not code and number and not operator:
            full_number = int(number + ''.join(['0' for c in range(0, 7 - len(number))]))
            query = meta.session.query(Record).filter(and_(Record.nfrom <= full_number, Record.nto >= full_number))
            for r in query:
                results.append(r)
        elif code and not number and operator:
            results1 = []
            query = meta.session.query(Record).filter(Record.code == code).filter(Record.nfrom.like(number + '%'))
            for r in query:
                results1.append(r)
            results2 = []
            s = re.sub(r'[,-/;\'.*:@!#$%^&?()№{}\[\]+=]', ' ', operator).split(' ')
            tstr1 = ' and '.join(['operator:%s*' % x for x in s])
            query = self.parser.parse(tstr1)
            for res in self.ix.searcher().search(query, limit=None):
                id = res['id']
                r = meta.session.query(Record).filter(Record.id == id).one()
                results2.append(r)
            resu = self.intersect(results1, results2)
            return resu
        return results
    except Exception:
        return results


class Searcher():

    # def __init__(self, index_path=None):
    #     self.stemmer = Stemmer.Stemmer('russian')
    #     schema = Schema(id = ID(stored = True), code=TEXT, nfrom=TEXT, nto=TEXT, operator=TEXT(stored=True), region=TEXT(stored=True))
    #     if not os.path.exists(index_path):
    #         log.debug('path doesn\'t exists')
    #         os.mkdir(index_path)
    #         self.ix = create_in(index_path, schema)
    #     else:
    #        for f in os.listdir(index_path):
    #            os.remove(index_path + '/' + f)
    #        self.ix = create_in(index_path, schema)
    #     self.ix = open_dir(index_path)
    #     self.parser = QueryParser('operator', schema = self.ix.schema)
    #     # self.reload()
    #
    # def __index__(self, path, **args):
    #     Index(store.FileStorage(path), schema = schema, **args)


    def add(self, **kwargs):
        if self.ix:
            writer = self.ix.writer()
            writer.add_document(code = kwargs.get('code'), status = kwargs.get('status'), nfrom = kwargs.get('nfrom'), nto = kwargs.get('nto'), operator = kwargs.get('operator'), region = kwargs.get('region'))
            writer.commit()
            writer = None
        self.ix.commit()

    def intersect(self, l1, l2):
        res = []                     # start empty
        for x in l1:               # scan seq1
            if x in l2:            # common item?
                res.append(x)        # add to end
        return res

    def index_records(self):
        log.debug('processing index_records()')
        records = meta.Session.query(Record).all()
        writer = self.ix.writer()
        for a in records:
            writer.add_document(id = unicode(a.id), code = unicode(a.code), nfrom= unicode(a.nfrom), nto = unicode(a.nto), operator = re.sub(r'[,-/;\'.*:@!#$%^&?()№{}\[\]+=]', ' ', a.operator), region = a.region)
            log.debug('added %i' % a.id)
        writer.commit()