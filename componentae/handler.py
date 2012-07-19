from componentae.interfaces import ITraverser, ITemplateLoader
from componentae.app import Application
from zope.component import getUtility
import grokcore.component as grok
import webapp2

class Traverse(webapp2.RequestHandler):

    def get(self, path):
        app = Application(self.request, self.response)
        traverser = ITraverser(app)
        obj = traverser.traverse(self.request, self.response, path.split('/'))
        if getattr(obj, 'render', None):
            self.response.out.write(obj.render())
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write(obj)
