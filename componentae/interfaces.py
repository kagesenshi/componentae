from zope.interface import Interface
import grokcore.component.interfaces as grokiface

class IContext(grokiface.IContext):
    pass

class IApplication(IContext):
    pass

class IModel(IContext):
    pass

class IContainer(IContext):
    pass

class IView(Interface):

    def render():
        """
        Renders the page and return the html
        """
        pass

class ITraverser(Interface):
    pass

class ITemplateLoader(Interface):
    pass

class IConfig(Interface):
    pass

class IViewLookup(Interface):
    pass
