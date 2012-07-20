import grokcore.component as grok
from componentae.interfaces import (IContext, 
                                    ITemplateLoader, 
                                    IView,
                                    IViewLookup)
from webapp2 import Request, Response
from zope.component import getUtility, getAdapter, ComponentLookupError

class ViewLookup(grok.Adapter):
    grok.implements(IViewLookup)
    grok.context(IContext)

    def __init__(self, context):
        self.context = context

    def __getitem__(self, key):
        try:
            return getAdapter(self.context, IView, name=key).template
        except ComponentLookupError:
            raise KeyError(key)

class View(grok.Adapter):
    grok.implements(IView)
    grok.baseclass()

    def __init__(self, context):
        self.context = context

    def render(self):
        if getattr(self, 'template', None):
            views = IViewLookup(self.context)
            return self.template(
                    context=self.context, request=self.request,
                    response=self.response, views=views)
        self.response.headers['Content-Type'] = 'text/plain'
        return repr(self)
