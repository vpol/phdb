# -*- coding: utf-8 -*-
import logging
from phdb.searcher import search
from phdb import funcname

__author__ = 'Victor Poluksht'

log = logging.getLogger(__name__)

def index(request):
    # log.debug('in {0}: request is {1}'.format(funcname(), request.registry.settings))
    # res, tsec = search(request, code='812', number='123456*')
    res, tsec = search(request, operator='мфорт')
    return {'result': res, 'time': tsec}