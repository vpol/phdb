# -*- coding: utf-8 -*-
import logging
from pyramid.interfaces import IAuthorizationPolicy
from sqlalchemy.orm.exc import NoResultFound
import transaction
from zope.interface.declarations import implements
#from phdb.models.common import Session
#from phdb.models import User, Role

log = logging.getLogger(__name__)

__author__ = 'Victor Poluksht'

#def ReloadPermissions(userid, request):
#
#    print 'reloading permissions for user'
#
#    permissions_cache = request.registry.settings['cache.permissions']
#
#    if not userid in permissions_cache:
#        permissions_cache[userid] = []
#
#
#    try:
#        user = meta.session.query(User).filter(User.us_id == userid).one()
#    except NoResultFound:
#        return False
#    else:
#        p = list()
#        for role in user.roles:
#            for permission in role.permissions:
#                p.append(str(permission.pm_name))
##                p.append(str(role.ro_name) + ":" + str(permission.pm_name))
#        permissions_cache[userid] = p
#        print permissions_cache[userid]
#        return True
#
#def ManageRole(userid, action, role):
#
#
#    try:
#        user = meta.session.query(User).filter(User.us_id == userid).one()
#        role = meta.session.query(Roles).filter(Role.ro_name == role).one()
#    except NoResultFound:
#        return False
#    else:
#        if action == 'add':
#            user.roles.append(role)
#            session.add(user)
#            transaction.commit()
#        if action == 'remove':
#            try:
#                user.roles.remove(role)
#            except ValueError:
#                pass
#            else:
#                session.add(user)
#                transaction.commit()
#
#def CheckPermissions(userid, request):
#
#    print 'checking for permissions'
#
#    permissions_cache = request.registry.settings['cache.permissions']
#
#    if not userid in permissions_cache:
#        print 'no userid in permissions cache'
#        return []
#
#    return permissions_cache[userid]
#
#    try:
#        user = meta.session.query(User).filter(User.us_id == userid).one()
#    except NoResultFound:
#        return []
#    else:
#        p = set()
#        for role in user.roles:
#            for permission in role.permissions:
#                p.add(permission.pm_name)
#        return list(p)
def CheckPermissions(userid, request):
    return

class MyAuthorisationPolicy(object):

    implements(IAuthorizationPolicy)

    def permits(self, context, principals, permission):
        if permission in principals:
            return True
        return False

    def principals_allowed_by_permission(self, context, permission):
        return