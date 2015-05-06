from plone import api
from zope.interface import Interface
from Acquisition import aq_inner
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone.dexterity.content import Container

from fhf.metrics import MessageFactory as _

from fhf.metrics.topic import ITopic
from fhf.metrics.metric import IMetric

class IDashboard(Interface):
    """marker interface for dashboard view"""

class Dashboard(Container):
    """A folder-type that contains topics which contain metrics"""

    def contents(self):
        """ returns a list of dictionaries one for each topic
            the topic dictionary contains the following keys:
            topic: brain for a topic content type
            metics: list of brains for metrics in each topic
        """

        context = aq_inner(self)
        catalog = getToolByName(context, 'portal_catalog')

        path = '/'.join(context.getPhysicalPath())
        topics = catalog(object_provides=ITopic.__identifier__, 
                path={'query': path, 'depth':1},
                sort_on='getObjPositionInParent')

        results = []
        for t in topics:
            metrics = catalog(object_provides=IMetric.__identifier__,
                    path={'query': '/'.join(t.getPhysicalPath()), 'depth': 1},
                    sort_on='getObjPositionInParent')
            results.append({'topic': t, 'metrics': metrics})
            
        return results


class DashboardView(BrowserView):
    """a dashboard that presents links to all metrics in the folder"""

    def topics(self):
        #import pdb; pdb.set_trace()
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        return catalog(object_provides=ITopic.__identifier__, 
                path={'query': path, 'depth':1},
                sort_on='getObjPositionInParent')

    def metrics(self):
        import pdb; pdb.set_trace()

        results = []
        for t in self.topics():
            metrics = catalog(object_provides=IMetric.__identifier__,
                    path={'query': '/'.join(t.getPhysicalPath()), 'depth': 1},
                    sort_on='getObjPositionInParent')
            results.append({'topic': t, 'metrics': metrics})
            
        return results


