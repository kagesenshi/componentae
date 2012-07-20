from componentae.interfaces import ITraverser, IView, IContext
from webob.exc import HTTPNotFound
import grokcore.component as grok
from zope.component import ComponentLookupError, getMultiAdapter, getAdapter
import traject

class Traverser(grok.Adapter):
    grok.context(IContext)
    grok.implements(ITraverser)

    def __init__(self, context):
        self.context = context

    def traverse(self, request, response, stack):
        unconsumed, consumed, obj = traject.consume_stack(
                self.context, stack, object)
        if obj != self.context and not(unconsumed):
            return obj
        if obj != self.context and unconsumed:
            return ITraverser(obj).traverse(request, response, unconsumed)

        try:
            name = '/'.join(stack) if stack else 'index'
            if name == '/':
                name = 'index'
            view = getAdapter(self.context, IView, name=name)
            view.request = request
            view.response = response
            return view
        except ComponentLookupError:
            raise HTTPNotFound
