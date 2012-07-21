import grokcore.component as grok
from zope.component.interfaces import IFactory
from componentae.interfaces import (
    IContext, IApplication, ICommitable, ISession
)
from componentae import exc
from zope.component import getUtility, getGlobalSiteManager
from google.appengine.ext import db
from zope.interface import implementedBy
from zope.globalrequest import getRequest
from zope.interface.declarations import Implements

_marker = []

class Node(db.Model):
    name = db.StringProperty(required=True)
    title = db.StringProperty()
    container = db.SelfReferenceProperty()
    portal_type = db.StringProperty()

    def items(self):
        nodes = self.node_set
        if nodes:
            return [(node.name, node) for node in nodes]
        return []

    def values(self):
        nodes = self.node_set
        if nodes:
            return [node for node in nodes]
        return []

    def keys(self):
        nodes = self.node_set
        if nodes:
            return [node.name for node in nodes]
        return []

    def __setitem__(self, key, value):
        if self.get(key, None):
            raise exc.NameConflictError()
        value.name = key
        value.container = self

    def __getitem__(self, key):
        for k, v in self.items():
            if k == key:
                return v
        raise KeyError(key)

    def get(self, key, default=_marker):
        try:
            return self[key]
        except KeyError, e:
            if default is not _marker:
                return default
            raise e

    def getPath(self):
        if getattr(self, '_path', None) is None:
            stack = [self.name]
            parent = self.container
            while parent:
                stack.append(parent.name)
                parent = parent.container
            stack = stack[:-1] # get rid of the root node
            stack.append('')
            self._path = list(reversed(stack))
        return self._path

class Committer(grok.Adapter):
    grok.implements(ICommitable)
    grok.context(db.Model)

    def __init__(self, context):
        self.context = context

    def put(self):
        self.context.put()



class Context(grok.Adapter):
    """
        This is the main context class. Magics we do here:

        1) Create annotation and map setter/getter to to the annotation
        2) provide some utility functions to help in using the context

        Inherit this class for your contenttype
    """
    grok.implements(IContext)
    grok.context(Node)
    grok.baseclass()

    annotation_model = None

    def __init__(self, node):
        self._node = node

        # if annotation_model is set, means we want to use annotation
        if self.annotation_model:
            # create the annotation
            annotation = self.annotation_model.all().filter(
                'node =', node.key()).get()
            if not annotation:
                annotation = self.annotation_model(node=node)
            getUtility(ISession).add(annotation)
            self._annotation = annotation

    def __setitem__(self, key, value):
        self._node[key] = value

    def __getitem__(self, key):
        node = self._node[key]
        factory = getUtility(IFactory, name=node.portal_type)
        adapteriface = list(factory.getInterfaces())[0]
        return adapteriface(self._node[key])

    def items(self):
        result = []
        for key, node in self._node.items():
            result.append((key, self[key]))
        return result

    def values(self):
        return [v for k, v in self.items()]

    def keys(self):
        return [k for k, v in self.items()]

    def __setattr__(self, key, value):
        if key in ['_node', '_path']:
            self.__dict__[key] = value
            return

        # set values on the annotation if the fields are from there
        if self.annotation_model and key in self.annotation_model.fields():
            setattr(self._annotation, key, value)

        return setattr(self._node, key, value)

    def __getattr__(self, key):
        # get values from the annotation if the fields are from there
        if self.annotation_model and key in self.annotation_model.fields():
            return getattr(self._annotation, key)

        return getattr(self._node, key)

    def get(self, key, default=_marker):
        try:
            return self._node[key]
        except KeyError, e:
            if default is not _marker:
                return default
            raise e

    def absolute_url(self):
        request = getRequest()
        return request.relative_url(
                '/'.join(self._node.getPath()),
                to_application=True
        )

class Application(Context):
    grok.implements(IApplication)
    grok.provides(IApplication)
    grok.context(Node)


    def getSiteManager(self):
        return getGlobalSiteManager()


class ApplicationFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('Application')

    def __call__(self, *args, **kwargs):
        # get the root node
        nodes = Node.all().fetch(1)
        if not len(nodes):
            node = Node(name='root', portal_type='Application')
            node.put()
        else:
            node = nodes[0]
        getUtility(ISession).add(node)
        return IApplication(node)

    def getInterfaces(self):
        return implementedBy(Application)

class Factory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.baseclass()

    def __call__(self, name, *args, **kwargs):
        portal_type = getattr(self, 'grokcore.component.directive.name')
        node = Node(name=name, portal_type=portal_type)
        getUtility(ISession).add(node)
        node.put()
        return self.iface(node)

    def getInterfaces(self):
        return Implements([self.iface])


class Session(grok.GlobalUtility):
    grok.implements(ISession)

    def __init__(self):
        self._models = []

    def add(self, context):
        model = ICommitable(context)
        if model not in self._models:
            self._models.append(model)

    def commit(self):
        for model in self._models:
            model.put()
        self._models = []
