__author__ = 'li'

from ControllerApp.FlowDB import FlowDB
from ControllerApp.Allocator import Allocator
from ControllerApp.CoflowID import CoflowID
from ControllerApp.SizeEstimator import SizeEstimator

class Controller(object):
    # ryu handler interacts with different components directly
    def __init__(self):
        self.flowDB = FlowDB()
        self.allocator = Allocator()
        self.coflowid = CoflowID()
        self.flowSizeEstm = SizeEstimator()
        self.rackList = []
        self.serverList = []
        self.spineList = []

    # TODO: Integrate with Ryu
    # TODO: testcases for controller components
