# -*- coding: utf-8 -*-
import logging
from phdb.searcher import search
from phdb import funcname

__author__ = 'Victor Poluksht'

log = logging.getLogger(__name__)

def index(request):
    if not 'code' in request.params:
        return {'result': [], 'time': 0, 'error': 'No code'}
    if not 'number' in request.params:
        return {'result': [], 'time': 0, 'error': 'No number'}
    if not 'operator' in request.params:
        return {'result': [], 'time': 0, 'error': 'No operator'}
    # log.debug('in {0}: request is {1}'.format(funcname(), request.registry.settings))
    # res, tsec = search(request, code='812', number='123456*')
    res, tsec = search(request, code=request.params['code'], number=request.params['number'], operator=request.params['operator'])
    return {'result': res, 'time': tsec}