from google.appengine.api.users import User
import grokcore.component as grok
from componentae.interfaces import IContext, IRoleManager, IRole
from google.appengine.ext import db
from zope.component import getUtility
from zope.interface import Interface
from google.appengine.api import users

class UserRole(db.Model):
    user = db.StringProperty()
    role = db.StringProperty()


class RoleManager(grok.Adapter):
    grok.context(Interface)
    grok.implements(IRoleManager)

    def getRolesFor(self, user):
        if user:
            userroles = UserRole.all()
            userroles.filter('user =', user.email()).get()
            if userroles:
                return [getUtility(IRole, name=userrole.role) for userrole in userroles]
        return [getUtility(IRole, name='Anonymous')]


def checkPermission(context, user, permission):
    if users.is_current_user_admin():
        return True
    rolemanager = IRoleManager(context)
    roles = rolemanager.getRolesFor(user)
    for role in roles:
        if permission in role.permissions:
            return True
    return False

class AnonymousRole(grok.GlobalUtility):
    grok.implements(IRole)
    grok.name('Anonymous')
    permissions = ['cae.View']
