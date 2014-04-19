# -*- coding: utf-8 -*-
import traceback
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid_beaker import session_factory_from_settings
from sqlalchemy.pool import StaticPool
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from phdb.cache import Cache
from phdb.models.common import initialize_sql
from phdb.security import CheckPermissions, MyAuthorisationPolicy

__author__ = 'Victor Poluksht'

def funcPrint(obj = None):
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
    authentication_policy = SessionAuthenticationPolicy(callback=CheckPermissions)
    authorization_policy = MyAuthorisationPolicy()
    session_factory = session_factory_from_settings(settings)
    ## caches
    settings['cache.example'] = Cache(settings['cache.example'], 'example')
    ## end
    config = Configurator(settings=settings, authentication_policy=authentication_policy, authorization_policy=authorization_policy)
    config.set_session_factory(session_factory)

    config.add_static_view('static', 'phdb:static')

    # Index (main page)
    #config.add_route('Index', '/')
    #config.add_view('phdb.views.Index', route_name = 'Index', renderer='phdb:templates/Index.mako')

    return config.make_wsgi_app()