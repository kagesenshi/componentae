from componentae.interfaces import ITraverser, IView, IContext
from webob.exc import HTTPNotFound
import grokcore.component as grok
from zope.component import ComponentLookupError, getMultiAdapter, getAdapter

class Traverser(grok.Adapter):
    grok.context(IContext)
    grok.implements(ITraverser)

    def __init__(self, context):
        self.context = context

    def traverse(self, request, response, stack):
        if stack:
            if self.context.get(stack[0], None):
                obj = self.context[stack[0]]
                return ITraverser(obj).traverse(request, response, stack[1:])

        try:
            name = '/'.join(stack) if stack else 'index'
            if name in ['/', '']:
                name = 'index'
            view = getAdapter(self.context, IView, name=name)
            view.request = request
            view.response = response
            return view
        except ComponentLookupError:
            if name == 'index':
                return self.context
            raise HTTPNotFound
