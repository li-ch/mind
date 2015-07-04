__author__ = 'li'

from ControllerApp.FlowDB import FlowDB
from ControllerApp.Allocator import Allocator
from ControllerApp.CoflowID import CoflowID
from ControllerApp.SizeEstimator import SizeEstimator

# Spine leaf testbed topology constants
NUMCORE = 2
NUMRACK = 8
NUMSERVERPRACK = 4
NUMSERVER = NUMCORE * NUMRACK * NUMSERVERPRACK

class Controller(object):
    # ryu handler interacts with different components directly
    def __init__(self,
                 ncore=NUMCORE,
                 nrack=NUMRACK,
                 nserverPerRack=NUMSERVERPRACK):
        self.flowDB = FlowDB()
        self.allocator = Allocator()
        self.coflowid = CoflowID()
        self.flowSizeEstm = SizeEstimator()
        self.cores = self.setCores(ncore)
        self.racks = self.setRacks(nrack)
        self.servers = self.setServers(nrack, nserverPerRack)

    def setServers(self, nrack, nserverPerRack):
        return range(nrack * nserverPerRack)

    def setRacks(self, nrack):
        return range(nrack)

    def setCores(self, ncore):
        return range(ncore)

    def addNewRack(self, rack):
        self.rackList.append(rack)

    def removeRack(self, rack):
        if rack in self.rackList:
            self.rackList.remove(rack)
        else:
            print 'rack not found'

    def addServer(self, server, rack):
        pass

    def removeServer(self, server):
        pass

    def addCore(self, core):
        pass

    def removeCore(self, core):
        pass

    def getServers(self):
        return self.servers

    def getServerId(self, ip):
        return [s.id for s in self.servers if s.ip == ip]

    def getFlows(self):
        return self.flowDB

    def getRacks(self):
        return self.racks

    def getCores(self):
        return self.cores

    def getRackNum(self, server):
        return server/len(self.racks)  # integer division

    def getPaths(self, srcServer, dstServer):
        # srcRack = self.getRackNum(srcServer)
        # dstRack = self.getRackNum(dstServer)
        return self.cores

    # TODO: Integrate with Ryu
    # TODO: testcases for controller components
