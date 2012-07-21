import grokcore.component as grok
from componentae.interfaces import (IContext, 
                                    ITemplateLoader, 
                                    IView, ISession,
                                    IViewLookup)
from webapp2 import Request, Response, redirect
from zope.component import getUtility, getAdapter, ComponentLookupError

class ViewLookup(grok.Adapter):
    grok.implements(IViewLookup)
    grok.context(IContext)

    def __init__(self, context):
        self.context = context

    def __getitem__(self, key):
        try:
            return getAdapter(self.context, IView, name=key)
        except ComponentLookupError:
            raise KeyError(key)

class View(grok.Adapter):
    grok.implements(IView)
    grok.baseclass()
    permission_required = 'cae.View'

    def __init__(self, context):
        self.context = context

    def update(self):
        pass

    def render(self):
        self.update()
        getUtility(ISession).commit()
        if getattr(self, 'template', None):
            views = IViewLookup(self.context)
            return self.template(
                    context=self.context, request=self.request,
                    response=self.response, views=views, view=self)
        self.response.headers['Content-Type'] = 'text/plain'
        return repr(self)

    def redirect(self, uri, permanent=False, abort=False, code=None,
                 body=None):
        """Issues an HTTP redirect to the given relative URI.

        The arguments are described in :func:`redirect`.
        """
        uri = str(uri)
        return redirect(uri, permanent=permanent, abort=abort, code=code,
                        body=body, request=self.request,
                        response=self.response)
