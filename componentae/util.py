from StringIO import StringIO
from zope.configuration.xmlconfig import xmlconfig

def load_components(packages):

    snippet = '\n'.join(
        ['<grok:grok package="%s" />' % p for p in packages]
    )
    xmlconfig(StringIO('''
        <configure xmlns="http://namespaces.zope.org/zope"
               xmlns:grok="http://namespaces.zope.org/grok">
        <include package="grokcore.component" file="meta.zcml"/>
        %s
        </configure>''' % snippet
    ))
