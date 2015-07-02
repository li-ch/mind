__author__ = 'li'

import FlowDB
import Allocator
import CoflowID
import SizeEstimator

class Controller(object):
    # ryu handler interacts with different components directly
    def __init__(self):
        self.flowDB = FlowDB()
        self.allocator = Allocator()
        self.coflowid = CoflowID()
        self.flowSizeEstm = SizeEstimator()

    # TODO: Integrate with Ryu
    # TODO: testcases for controller components
