from five import grok

from z3c.form import group, field
from zope import schema
from Acquisition import aq_inner
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable


from fhf.metrics import MessageFactory as _


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


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Metric(Container):
    grok.implements(IMetric)


# View class
# The view will automatically use a similarly named template in
# metric_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IMetric)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
    def css(self):
        """return all contained CSS files as a set of link tags"""

        context = aq_inner(self.context)
        links = []
        for l in context.listFolderContents():
            if l.id.endswith('.css'):
                links.append('<link rel="stylesheet" href="%s">' \
                             % l.absolute_url())
        return '\n'.join(links)

