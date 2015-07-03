__author__ = 'li'

from FlowDB import FlowDB

class Allocator(object):
    def __init__(self):
        pass

    def placeFlow(self, fid, paths, flowdb):
        path = self.findPath(fid, paths, flowdb)
        flowdb.setPath(fid, path)
        return flowdb

    def findPath(self, paths, flowdb):
        # global first fit algorithm
        pathScore = self.pathScorer(flowdb, paths)
        minScorePath = min(pathScore, key=pathScore.get)
        return minScorePath

    def pathScorer(self, flowdb, paths):
        pathScore = dict(zip(paths, len(paths) * [0]))
        for p, s in pathScore:
            pathScore[p] = flowdb.getNumFlowsOnpath(p) + flowdb.getSizeOnPath(p)
        return pathScore

    def placeAllCoflows(self, paths, flowdb):
        cids = flowdb.getAllCoflow()
        for c in cids:
            coflow = flowdb.getAllInCoflow(c)
            pathCount = dict(zip(paths, len(paths)*[0]))
            for f in coflow:
                path = self.findPath(paths, flowdb)
                pathCount[path] += 1
            mostChosenPath = max(pathCount, key=pathCount.get)
            for f in coflow:
                return self.placeFlow(f['id'], mostChosenPath, flowdb)

    def genCandidatePaths(self, paths, flowdb):
        # use reinforcement learning to generate candidate paths
        # interface with RL module
        # TODO: add RL support
        return paths


