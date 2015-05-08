from zope.interface import Interface
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName
from plone.dexterity.content import Container
from Products.Five import BrowserView

from fhf.metrics import MessageFactory as _

import dashboard
import metric

class ITopic(Interface):
    """marker interface for dashboard view"""


class Topic(Container):
    """A folder-type that contains topics which contain metrics"""
    pass


class TopicView(BrowserView):
    """returns the parent container that is a Dashboard-type"""

    def dashboard(self):

        obj = aq_inner(self.context)
        while obj is not None:
            if dashboard.IDashboard.providedBy(obj):
                break
            else:
                obj = getattr(obj, 'aq_parent', None)

        if not obj:
            raise RuntimeError('Unable to locate Dashboard container')
        else:
            return obj


    def metrics(self):
        #import pdb; pdb.set_trace()

        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        results = catalog(object_provides=metric.IMetric.__identifier__,
                path={'query': path, 'depth':1},
                sort_on='getObjPositionInParent')

        return [b.getObject() for b in results]

