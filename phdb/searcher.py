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
        tstr1 = ' and '.join(['operator:*%s*' % x for x in s])
        query = parser.parse(tstr1)
        for res in ix.searcher().search(query, limit=None):
            id = res['id']
            r = meta.session.query(Record).filter(Record.id == id).one()
            results.append(r)
        return [r.asDict() for r in results], time.time() - start_time
    if not code and number and operator:
        ix = request.registry.settings['ix']
        parser = QueryParser('operator', schema=ix.schema)
        results1 = []
        full_number = int(number + ''.join(['0' for c in range(0, 7 - len(number))]))
        query = meta.session.query(Record).filter(and_(Record.nfrom <= full_number, Record.nto >= full_number))
        for r in query:
            results1.append(r)
        results2 = []
        s = re.sub(r'[,-/;\'.*:@!#$%^&?()№{}\[\]+=]', ' ', operator).split(' ')
        tstr1 = ' and '.join(['operator:*%s*' % x for x in s])
        query = parser.parse(tstr1)
        for res in ix.searcher().search(query, limit=None):
            id = res['id']
            r = meta.session.query(Record).filter(Record.id == id).one()
            results2.append(r)
        results = []
        results.extend(set(results1).intersection(set(results2)))
        return [r.asDict() for r in results], time.time() - start_time
    if not code and number and not operator:
        results = []
        full_number = int(number + ''.join(['0' for c in range(0, 7 - len(number))]))
        query = meta.session.query(Record).filter(and_(Record.nfrom <= full_number, Record.nto >= full_number))
        for r in query:
            results.append(r)
    if code and not number and operator:
        ix = request.registry.settings['ix']
        parser = QueryParser('operator', schema=ix.schema)
        results1 = []
        query = meta.session.query(Record).filter(Record.code == code).filter(Record.nfrom.like(number + '%'))
        for r in query:
            results1.append(r)
        results2 = []
        s = re.sub(r'[,-/;\'.*:@!#$%^&?()№{}\[\]+=]', ' ', operator).split(' ')
        tstr1 = ' and '.join(['operator:*%s*' % x for x in s])
        query = parser.parse(tstr1)
        for res in ix.searcher().search(query, limit=None):
            id = res['id']
            r = meta.session.query(Record).filter(Record.id == id).one()
            results2.append(r)
        return [r.asDict() for r in [val for val in results1 if val in results2]], time.time - start_time
    if code and number and operator:
        if number.find('*') >= 1:
            results1 = []
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
                        results1.append(c)
            results2 = []
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
            results = set(results1 + results2)
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
            log.debug('in {0}: len(results)={1}'.format(funcname(), len(results)))
            # return [r.asDict() for r in results], time.time() - start_time
        ix = request.registry.settings['ix']
        parser = QueryParser('operator', schema=ix.schema)
        results3 = []
        s = re.sub(r'[,-/;\'.*:@!#$%^&?()№{}\[\]+=]', ' ', operator).split(' ')
        tstr1 = ' and '.join(['operator:*%s*' % x for x in s])
        query = parser.parse(tstr1)
        for res in ix.searcher().search(query, limit=None):
            id = res['id']
            r = meta.session.query(Record).filter(Record.id == id).one()
            results3.append(r)
        log.debug('in {0}: len(results3)={1}'.format(funcname(), len(results3)))
        return [r.asDict() for r in [val for val in results if val in results3]], time.time() - start_time
    return [], time.time() - start_time