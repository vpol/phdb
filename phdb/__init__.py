# -*- coding: utf-8 -*-
import logging
import traceback
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid_beaker import session_factory_from_settings
from sqlalchemy.pool import StaticPool
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from phdb.cache import Cache
from phdb.loader import file_loader, reindex
from phdb.models.common import initialize_sql
# from phdb.security import CheckPermissions, MyAuthorisationPolicy

__author__ = 'Victor Poluksht'

log = logging.getLogger(__name__)

def funcname(obj = None):
    '''Вывод текущего метода'''
    stack = traceback.extract_stack()
    scriptName, lineNum, funcName, lineOfCode = stack[-2]
    if obj:
        return '%s.%s()' % (obj.__class__.__name__, funcName)
    else:
        return '%s()' % funcName

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.', connect_args={'check_same_thread':False}, poolclass=StaticPool)
    initialize_sql(engine)
    # authentication_policy = SessionAuthenticationPolicy(callback=CheckPermissions)
    # authorization_policy = MyAuthorisationPolicy()
    session_factory = session_factory_from_settings(settings)
    ## caches

    ## end
    config = Configurator(settings=settings)
    config.set_session_factory(session_factory)

    config.add_settings({'cache.example': Cache(settings['cache.example'], 'example')})

    config.add_static_view('static', 'phdb:static')

    files = file_loader(config.get_settings()['links'], config.get_settings()['data_path'])
    log.debug('in {0}: finished loading stage'.format(funcname()))
    ix = reindex(files, config.get_settings()['ix_path'])
    config.add_settings({'index': ix})

    # Index (main page)
    #config.add_route('Index', '/')
    #config.add_view('phdb.views.Index', route_name = 'Index', renderer='phdb:templates/Index.mako')

    return config.make_wsgi_app()