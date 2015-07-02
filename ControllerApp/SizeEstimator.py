__author__ = 'li'

class SizeEstimator(object):
    def estimate(self, flowdb):
        for f in flowdb:
            size = self.flowSizeEstimator(f)
            flowdb.setFlowSize(f['id'], size)
        return flowdb

    def flowSizeEstimator(self, flow):
        # this method does not modify flowdb
        size = 0
        # interface with size estimation
        return size
