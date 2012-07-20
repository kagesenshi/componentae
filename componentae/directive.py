import sys, os
from chameleon.zpt import loader

def template(name):
    frame = sys._getframe(1)
    template_path = os.path.join(
        os.path.dirname(
        frame.f_globals['__file__'])
    )
    template_loader = loader.TemplateLoader(
        template_path,
        auto_reload=os.environ['SERVER_SOFTWARE'].startswith('Dev')
    )
    frame.f_locals['template'] = template_loader.load(name)
