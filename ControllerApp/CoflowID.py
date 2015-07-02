__author__ = 'li'

from FlowDB import FlowDB

class CoflowID(object):
    def coflowid(self, flowdb):
        fids = flowdb.getAllFlowId()
        # flowdb is just a list of flows
        fcids = dict(zip(fids, [-1]*len(fids)))
        # algorithm fills out fcid
        fcids = self.cider(fcids, flowdb)
        for fid, cid in fcids:
            flowdb.setCoflowId(fid,cid)
        return flowdb

    def cider(self, results, flowdb):
        # cider does not modify flowdb
        return results