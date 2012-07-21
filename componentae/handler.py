from componentae.interfaces import ITraverser, ITemplateLoader, ISession
from componentae.model import Application
from componentae.security import checkPermission
from zope.component import getUtility
import grokcore.component as grok
import webapp2
from zope.component import createObject
from zope.component.hooks import setSite
from zope.globalrequest import setRequest, clearRequest
from google.appengine.api import users

class Traverse(webapp2.RequestHandler):

    def get(self, path):
        if path == '/logout':
            if users.get_current_user():
                self.redirect(users.create_logout_url('/'))
            else:
                self.redirect(self.request.relative_url('/'))
            return
        setRequest(self.request)
        app = createObject('Application', self.request, self.response)
        setSite(app)
        traverser = ITraverser(app)
        stack = path.split('/')
        if stack[-1] == '':
            stack = stack[:-1]
        if stack[0] == '':
            stack = stack[1:]
        obj = traverser.traverse(self.request, self.response, stack)

        requires = getattr(obj, 'permission_required', None)
        if requires:
            user = users.get_current_user()
            if not checkPermission(obj, user, requires):
                self.redirect(users.create_login_url(self.request.uri))
                return

        if getattr(obj, 'render', None):
            self.response.out.write(obj.render())
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write(obj)
        getUtility(ISession).commit()
        clearRequest()

    def post(self, path):
        return self.get(path)
