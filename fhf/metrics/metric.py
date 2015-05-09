from zope import schema
from Acquisition import aq_inner
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form import group, field
from Products.Five.browser import BrowserView

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable


from fhf.metrics import MessageFactory as _

import dashboard


# Interface class; used to define content-type schema.

class IMetric(form.Schema, IImageScaleTraversable):
    """
    Flint Hills Frontiers regional metrics
    """

    overview = RichText(
            title = _(u'Overview'),
            description = _(u'overview of the metric'),
            required = False,
            )

    script = NamedBlobFile(
            title = _(u'Script'),
            description = _(u'javascript for graphing the data'),
            required = True,
            )

    uri = schema.URI(
            title = _(u'External Data Source'),
            description = _(u'Link to external data source.'),
            required = False,
            )

    attribution = RichText(
            title = _(u'Attribution'),
            description = _(u'source, related items, etc'),
            required = False,
            )

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Metric(Container):


    def dashboard(self):

        obj = aq_inner(self)
        while obj is not None:
            if dashboard.IDashboard.providedBy(obj):
                break
            else:
                obj = getattr(obj, 'aq_parent', None)

        if not obj:
            raise RuntimeError('Unable to locate Dashboard container')
        else:
            return obj


    def css(self):
        """return all contained CSS files as a set of link tags"""

        context = aq_inner(self)
        links = []
        for l in context.listFolderContents():
            if l.id.endswith('.css'):
                links.append('<link rel="stylesheet" class="required plugin" '
                        'href="%s/@@download/file">' % l.absolute_url())
        return '\n'.join(links)


class EmbeddedView(BrowserView):
    """ a simple template to embed multiple metrics on a page """
    pass


class ScriptView(BrowserView):
    """ utility view to return script with proper mime-type """

    def __call__(self):
        context = aq_inner(self.context)
        init = "\nmetric_init('%s', '%s', '%s');\n" % (context.id,
                context.uri, context.absolute_url())
        self.request.response.setHeader('content-type', 
                'application/javascript')
        return context.script._getData() + init


# View class
# The view will automatically use a similarly named template in
# metric_templates.
class MetricView(BrowserView):
    """ default view class """

    # Add view methods here
