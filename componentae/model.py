import grokcore.component as grok
from componentae.interfaces import IContext, IApplication

class Application(object):
    grok.implements(IContext, IApplication)
    grok.provides(IApplication)
    def __init__(self, request, response):
        self.request = request
        self.response = response
