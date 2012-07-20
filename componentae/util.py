from StringIO import StringIO
from zope.configuration.xmlconfig import xmlconfig
from zope.component import getUtility, getGlobalSiteManager
from zope.interface import directlyProvides
from componentae.interfaces import IConfig
from componentae.interfaces import ITemplateLoader
from chameleon.zpt import loader
import os

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

def set_config(key, value):
    config = getUtility(IConfig)
    config[key] = value

def get_config(key):
    config = getUtility(IConfig)
    return config[key]
