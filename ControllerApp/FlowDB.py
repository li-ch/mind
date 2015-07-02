__author__ = 'li'

import datetime

class Flow(dict):
    def __init__(self,
                 fid=0,
                 srcIP='10.0.0.1',
                 dstIP='10.0.0.2',
                 srcPort=8008,
                 dstPort=8009):
        self['id'] = fid
        self['srcIP'] = srcIP
        self['dstIP'] = dstIP
        self['srcPort'] = srcPort
        self['dstPort'] = dstPort
        self['size'] = -1
        self['cid'] = -1
        self['path'] = 0
        self['stime'] = datetime.datetime.now()

class FlowDB(object):
    def __init__(self):
        self.sampleFlow = Flow()
        self.flowDB = []
        self.flowDB.append(self.sampleFlow)

    # flow management
    def reg(self, fid, flow):
        exist = filter(lambda f: f['id'] == fid, self.flowDB)
        if exist:
            print 'flow {} already in FlowDB'.format(fid)
        else:
            self.flowDB.append(flow)

    def remove(self, fid):
        exist = filter(lambda f: f['id'] == fid, self.flowDB)
        if exist:
            self.flowDB.remove(exist[0])
        else:
            print 'cannot find flow {}'.format(fid)

    # getter
    def get(self, fid):
        exist = filter(lambda f: f['id'] == fid, self.flowDB)
        if len(exist) <= 1:
            return exist
        else:
            print 'too many flows with same id {}'.format(fid)

    def getAllFlowId(self):
        flowids = [f['id'] for f in self.flowDB]
        return flowids

    def getFlowsOnPath(self, path):
        onpath = filter(lambda f: f['path'] == path, self.flowDB)
        return onpath

    def getSizeOnPath(self, path):
        flows = self.getFlowsOnPath(path)
        size = sum([f['size'] for f in flows])
        return size

    def getNumFlowsOnpath(self, path):
        flows = self.getFlowsOnPath(path)
        num = len(flows)
        return num

    def getAllInCoflow(self, cid):
        if cid < 0:
            print 'illegal cid input'
            return []
        coflow = filter(lambda f: f['cid'] == cid, self.flowDB)
        return coflow

    def getAllCoflow(self):
        coflowids = [f['cid'] for f in self.flowDB if f['cid'] >= 0]
        return coflowids

    # setter
    def setFlowSize(self, fid, size):
        exist = filter(lambda f: f['id'] == fid, self.flowDB)
        if len(exist) == 1:
            self.remove(exist[0]['id'])
            exist[0]['size'] = size
            self.flowDB.append(exist[0])
        else:
            print 'flow {} not found'.format(fid)

    def setCoflowId(self, fid, cid):
        exist = filter(lambda f: f['id'] == fid, self.flowDB)
        if len(exist) == 1:
            self.remove(exist[0]['id'])
            exist[0]['cid'] = cid
            self.flowDB.append(exist[0])
        else:
            print 'flow {} not found'.format(fid)

    def setPath(self, fid, path):
        exist = filter(lambda f: f['id'] == fid, self.flowDB)
        if len(exist) == 1:
            self.remove(exist[0]['id'])
            exist[0]['path'] = path
            self.flowDB.append(exist[0])
        else:
            print 'flow {} not found'.format(fid)
