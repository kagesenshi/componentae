import grokcore.component as grok
from chameleon.zpt import loader
import os
from componentae.interfaces import ITemplateLoader

template_path = os.path.join(os.path.dirname(__file__), '..', "templates")
template_loader = loader.TemplateLoader(template_path,
                        auto_reload=os.environ['SERVER_SOFTWARE'].startswith('Dev'))

grok.global_utility(factory=template_loader, provides=ITemplateLoader,
                            direct=True)

