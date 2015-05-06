from zope.interface import Interface
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName
from plone.dexterity.content import Container
from Products.Five import BrowserView

from fhf.metrics import MessageFactory as _

from fhf.metrics.metric import IMetric

class ITopic(Interface):
    """marker interface for dashboard view"""


class Topic(Container):
    """A folder-type that contains topics which contain metrics"""
    pass


class TopicView(BrowserView):
    """a dashboard that presents links to all metrics in the folder"""

    def dashboard(self):

        # seems hardcoded but plone container content restrictions 
        # should enforce correctness to always return a dashboard
        dashboard = aq_parent(aq_inner(self.context))
        return dashboard.contents()


    def metrics(self):
        #import pdb; pdb.set_trace()

        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        return catalog(object_provides=IMetric.__identifier__,
                path={'query': path, 'depth':1},
                sort_on='getObjPositionInParent')

