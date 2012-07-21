from componentae.interfaces import ITraverser, ITemplateLoader, ISession
from componentae.model import Application
from zope.component import getUtility
import grokcore.component as grok
import webapp2
from zope.component import createObject
from zope.globalrequest import setRequest, clearRequest

class Traverse(webapp2.RequestHandler):

    def get(self, path):
        setRequest(self.request)
        app = createObject('Application', self.request, self.response)
        traverser = ITraverser(app)
        stack = path.split('/')
        if stack[-1] == '':
            stack = stack[:-1]
        if stack[0] == '':
            stack = stack[1:]
        obj = traverser.traverse(self.request, self.response, stack)
        if getattr(obj, 'render', None):
            self.response.out.write(obj.render())
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write(obj)
        getUtility(ISession).commit()
        clearRequest()

    def post(self, path):
        return self.get(path)
