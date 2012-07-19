import grokcore.component as grok
from componentae.interfaces import IConfig

class ConfigRegistry(grok.GlobalUtility):
    grok.implements(IConfig)

    _config = {}

    def __setitem__(self, key, value):
        self.config[key] = value

    def __getitem__(self, key):
        return self.config[key]
