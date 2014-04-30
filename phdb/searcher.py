# -*- coding: utf-8 -*-
import logging
import re
import time

from sqlalchemy.sql.expression import and_

# from whoosh. import store
from whoosh.qparser.default import QueryParser
from phdb import funcname
from phdb.models import Record
from phdb.models.common import meta

__author__ = 'Victor Poluksht'

log = logging.getLogger(__name__)


def search(request, code=None, number=None, operator=None):
    log.debug('in {0}: code={1}, number={2}, operator={3}'.format(funcname(), code, number, operator))
    start_time = time.time()
    ix = request.registry.settings['ix']
    if code and not number and not operator:
        query = meta.session.query(Record).filter(Record.code.like(code + '%'))
        return [r.asDict() for r in query], time.time() - start_time
    if code and number and not operator:
        if number.find('*') >= 1:
            results = []
            tmpnum = number[0:number.find('*')]
            full_number = number.replace('*', '.') + ''.join(['.' for c in range(0, 7 - len(number))])
            query = meta.session.query(Record).filter(Record.code == code).filter(Record.nfrom.like(tmpnum + '%'))
            for r in query:
                for x in range(r.nfrom, r.nto):
                    n = re.match(r'%s' % full_number, str(x))
                    if n:
                        c = Record()
                        c.code = r.code
                        c.nfrom = x
                        c.nto = x
                        c.region = r.region
                        c.operator = r.operator
                        results.append(c)
            # log.debug('in {0}: results = {1}'.format(funcname(), results))
            results1 = []
            tmpnum = int(tmpnum + ''.join(['0' for z in range(0, 7 - len(tmpnum))]))
            query = meta.session.query(Record).filter(Record.code == code).filter(
                and_(Record.nfrom <= tmpnum, Record.nto >= tmpnum))
            for r in query:
                for x in range(r.nfrom, r.nto):
                    n = re.match(r'%s' % full_number, str(x))
                    if n:
                        c = Record()
                        c.code = r.code
                        c.nfrom = x
                        c.nto = x
                        c.region = r.region
                        c.operator = r.operator
                        results1.append(c)
            # log.debug('in {0}: results1 = {1}'.format(funcname(), results))
            return [r.asDict() for r in set(results + results1)], time.time() - start_time
        else:
            results = []
            query = meta.session.query(Record).filter(Record.code == code).filter(Record.nfrom.like(number + '%'))
            for r in query:
                results.append(r)
            full_number = int(number + ''.join(['0' for c in range(0, 7 - len(number))]))
            query = meta.session.query(Record).filter(Record.code == code).filter(
                and_(Record.nfrom <= full_number, Record.nto >= full_number))
            for r in query:
                if not r in results:
                    results.append(r)
            return [r.asDict() for r in results], time.time() - start_time
    if not code and not number and operator:
        parser = QueryParser('operator', schema=ix.schema)
        results = []
        s = re.sub(r'[,-/;\'.*:@!#$%^&?()№{}\[\]+=]', ' ', operator).split(' ')
        tstr1 = ' and '.join(['operator:%s*' % x for x in s])
        query = parser.parse(tstr1)
        log.debug(query)
        log.debug(ix.searcher().search(query))
        for res in ix.searcher().search(query, limit=None):
            log.debug('in {0}: res = {1}'.format(funcname(), res))
            id = res['id']
            r = meta.session.query(Record).filter(Record.id == id).one()
            results.append(r)
        return [r.asDict() for r in results], time.time() - start_time
    elif not code and number and operator:
        ix = request.registry.settings['ix']
        parser = QueryParser('operator', schema=ix.schema)
        results1 = []
        full_number = int(number + ''.join(['0' for c in range(0, 7 - len(number))]))
        query = meta.session.query(Record).filter(and_(Record.nfrom <= full_number, Record.nto >= full_number))
        for r in query:
            results1.append(r)
        results2 = []
        s = re.sub(r'[,-/;\'.*:@!#$%^&?()№{}\[\]+=]', ' ', operator).split(' ')
        tstr1 = ' and '.join(['operator:%s*' % x for x in s])
        query = parser.parse(tstr1)
        for res in ix.searcher().search(query, limit=None):
            id = res['id']
            r = meta.session.query(Record).filter(Record.id == id).one()
            results2.append(r)
        results = []
        results.extend(set(results1).intersection(set(results2)))
        return [r.asDict() for r in results], time.time() - start_time
        #     elif not code and number and not operator:
        #         full_number = int(number + ''.join(['0' for c in range(0, 7 - len(number))]))
        #         query = meta.session.query(Record).filter(and_(Record.nfrom <= full_number, Record.nto >= full_number))
        #         for r in query:
        #             results.append(r)
        #     elif code and not number and operator:
        #         results1 = []
        #         query = meta.session.query(Record).filter(Record.code == code).filter(Record.nfrom.like(number + '%'))
        #         for r in query:
        #             results1.append(r)
        #         results2 = []
        #         s = re.sub(r'[,-/;\'.*:@!#$%^&?()№{}\[\]+=]', ' ', operator).split(' ')
        #         tstr1 = ' and '.join(['operator:%s*' % x for x in s])
        #         query = self.parser.parse(tstr1)
        #         for res in self.ix.searcher().search(query, limit=None):
        #             id = res['id']
        #             r = meta.session.query(Record).filter(Record.id == id).one()
        #             results2.append(r)
        #         resu = self.intersect(results1, results2)
        #         return resu
        #     return results
        # except Exception:
        # return results


        # class Searcher():
        #
        #     # def __init__(self, index_path=None):
        #     #     self.stemmer = Stemmer.Stemmer('russian')
        #     #     schema = Schema(id = ID(stored = True), code=TEXT, nfrom=TEXT, nto=TEXT, operator=TEXT(stored=True), region=TEXT(stored=True))
        #     #     if not os.path.exists(index_path):
        #     #         log.debug('path doesn\'t exists')
        #     #         os.mkdir(index_path)
        #     #         self.ix = create_in(index_path, schema)
        #     #     else:
        #     #        for f in os.listdir(index_path):
        #     #            os.remove(index_path + '/' + f)
        #     #        self.ix = create_in(index_path, schema)
        #     #     self.ix = open_dir(index_path)
        #     #     self.parser = QueryParser('operator', schema = self.ix.schema)
        #     #     # self.reload()
        #     #
        #     # def __index__(self, path, **args):
        #     #     Index(store.FileStorage(path), schema = schema, **args)
        #
        #
        #     def add(self, **kwargs):
        #         if self.ix:
        #             writer = self.ix.writer()
        #             writer.add_document(code = kwargs.get('code'), status = kwargs.get('status'), nfrom = kwargs.get('nfrom'), nto = kwargs.get('nto'), operator = kwargs.get('operator'), region = kwargs.get('region'))
        #             writer.commit()
        #             writer = None
        #         self.ix.commit()
        #
        #     def intersect(self, l1, l2):
        #         res = []                     # start empty
        #         for x in l1:               # scan seq1
        #             if x in l2:            # common item?
        #                 res.append(x)        # add to end
        #         return res
        #
        #     def index_records(self):
        #         log.debug('processing index_records()')
        #         records = meta.Session.query(Record).all()
        #         writer = self.ix.writer()
        #         for a in records:
        #             writer.add_document(id = unicode(a.id), code = unicode(a.code), nfrom= unicode(a.nfrom), nto = unicode(a.nto), operator = re.sub(r'[,-/;\'.*:@!#$%^&?()№{}\[\]+=]', ' ', a.operator), region = a.region)
        #             log.debug('added %i' % a.id)
        #         writer.commit()