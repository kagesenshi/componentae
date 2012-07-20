import grokcore.component as grok
from componentae.interfaces import IContext, ITemplateLoader, IView
from webapp2 import Request, Response
from zope.component import getUtility

class View(grok.Adapter):
    grok.implements(IView)
    grok.baseclass()

    def __init__(self, context):
        self.context = context

    def render(self):
        if getattr(self, 'template', None):
            templateloader = getUtility(ITemplateLoader)
            template = templateloader.load(self.template)
            return template(context=self.context, request=self.request,
                    response=self.response)
        self.response.headers['Content-Type'] = 'text/plain'
        return repr(self)
