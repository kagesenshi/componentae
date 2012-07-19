import grokcore.component as grok
from componentae.interfaces import IContext, ITemplateLoader, IView
from webapp2 import Request, Response
from zope.component import getUtility

class View(grok.MultiAdapter):
    grok.implements(IView)
    grok.baseclass()
    grok.adapts(IContext, Request, Response)

    def __init__(self, context, request, response):
        self.context = context
        self.request = request
        self.response = response

    def render(self):
        if getattr(self, 'template', None):
            templateloader = getUtility(ITemplateLoader)
            template = templateloader.load(self.template)
            return template(context=self.context, request=self.request)
        self.response.headers['Content-Type'] = 'text/plain'
        return repr(self)
