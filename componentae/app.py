import grokcore.component as grok
from componentae.interfaces import IContext

class Application(object):
    grok.implements(IContext)
    def __init__(self, request, response):
        self.request = request
        self.response = response
